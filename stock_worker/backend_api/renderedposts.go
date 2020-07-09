package backend_api

import (
	"bytes"
	"encoding/json"
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
