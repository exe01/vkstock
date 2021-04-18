package backend_api

import (
	"bytes"
	"encoding/json"
	"strconv"
	"time"
	"vkstock/stock_worker/models"
	"vkstock/stock_worker/utils"
)

type RenderPostConfig struct {
	OriginalPostId int `json:"original_post_id"`
}

func (api *StockAPI) RenderPost(originalPostId int) (models.RenderedPost, error) {
	var renderedPost models.RenderedPost
	config := RenderPostConfig{originalPostId}

	body, err := json.Marshal(config)
	if err != nil {
		return renderedPost, err
	}
	bodyReader := bytes.NewReader(body)

	resp, err := api.client.Post(api.URL+"/render_post", "application/json", bodyReader)
	if err != nil {
		return renderedPost, err
	}

	err = utils.ParseResponseBody(resp, &renderedPost)
	if err != nil {
		return renderedPost, err
	}

	return renderedPost, nil
}

func (api *StockAPI) GetFirstAcceptedPost(projectId int) (models.RenderedPost, error) {
	var renderedPost models.RenderedPost

	params := map[string]string{
		"count": "1",
		"status": "AC",
		"ordering": "id",
		"project_id": strconv.Itoa(projectId),
	}

	renderedPosts, err := api.GetRenderedPosts(params)
	if err != nil {
		return renderedPost, err
	}
	if len(renderedPosts) == 0 {
		return renderedPost, ModelNotFound{
			When: time.Now(),
			What: "rendered post not fount",
		}
	}

	return renderedPosts[0], nil
}

func (api *StockAPI) GetLastPostedPost(projectId int) (models.RenderedPost, error) {
	var renderedPost models.RenderedPost

	params := map[string]string{
		"count": "1",
		"status": "PO",
		"ordering": "-posted_date",
		"project_id": strconv.Itoa(projectId),
	}

	renderedPosts, err := api.GetRenderedPosts(params)
	if err != nil {
		return renderedPost, err
	}
	if len(renderedPosts) == 0 {
		return renderedPost, ModelNotFound{
			When: time.Now(),
			What: "rendered post not fount",
		}
	}

	return renderedPosts[0], nil
}

func (api *StockAPI) GetRenderedPosts(params map[string]string) ([]models.RenderedPost, error) {
	resp, err := api.GetModels("rendered_posts", params)
	if err != nil {
		return nil, err
	}

	var setRenderedPosts models.SetRenderedPosts
	err = utils.ParseResponseBody(resp, &setRenderedPosts)
	if err != nil {
		return nil, err
	}

	return setRenderedPosts.Results, nil
}

func (api *StockAPI) PatchRenderedPost(renderedPost models.RenderedPost) (models.RenderedPost, error) {
	var patchedPost models.RenderedPost

	renderedPost.Images = nil
	renderedPostId := strconv.Itoa(renderedPost.Id)

	resp, err := api.PatchModel("rendered_posts", renderedPostId, renderedPost)
	if err != nil {
		return patchedPost, nil
	}

	err = utils.ParseResponseBody(resp, &patchedPost)
	if err != nil {
		return patchedPost, err
	}

	return patchedPost, nil
}
