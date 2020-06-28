package backend_api

import (
	"vkstock/stock_worker/models"
	"vkstock/stock_worker/utils"
)

func (api *StockAPI) GetPosts(params map[string]string) ([]models.Post, error) {
	resp, err := api.GetModels("posts", params)
	if err != nil {
		return nil, err
	}

	var setPosts models.SetPosts
	err = utils.ParseResponseBody(resp, &setPosts)
	if err != nil {
		return nil, err
	}

	return setPosts.Results, nil
}

func (api *StockAPI) SavePost(post models.Post) (models.Post, error) {
	comments := post.Comments
	//images := post.Images

	post.Comments = nil
	post.Images = nil

	savedPost, err := api.savePost(post)
	if err != nil {
		return post, err
	}

	savedComments := make([]models.Comment, 0, len(comments))
	for _, comment := range comments {
		comment.PostId = savedPost.Id
		savedComment, err := api.saveComment(comment)
		if err != nil {
			continue
		}
		savedComments = append(savedComments, savedComment)
	}

	savedPost.Comments = savedComments

	return savedPost, nil
}

func (api *StockAPI) savePost(post models.Post) (models.Post, error) {
	resp, err := api.SaveModel("posts", post)
	if err != nil {
		return post, nil
	}

	err = utils.ParseResponseBody(resp, &post)
	if err != nil {
		return post, err
	}

	return post, nil
}

func (api *StockAPI) saveComment(comment models.Comment) (models.Comment, error) {
	resp, err := api.SaveModel("comments", comment)
	if err != nil {
		return comment, nil
	}

	err = utils.ParseResponseBody(resp, &comment)
	if err != nil {
		return comment, err
	}

	return comment, nil
}
