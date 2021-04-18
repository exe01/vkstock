package backend_api

import (
	"fmt"
	"io"
	"net/http"
	"vkstock/stock_worker/models"
	"vkstock/stock_worker/utils"
)

func (api *StockAPI) saveComment(comment models.Comment) (models.Comment, error) {
	var savedComment models.Comment

	commentWithoutImage := models.CommentWithoutImage{
		Username: comment.Username,
		Text:     comment.Text,
		PostId:   comment.PostId,
		RefText:  comment.RefText,
		Rating:   comment.Rating,
	}

	resp, err := api.SaveModel("comments", commentWithoutImage)
	if err != nil {
		return comment, err
	}

	err = utils.ParseResponseBody(resp, &savedComment)
	if err != nil {
		return comment, err
	}

	if len(comment.Image) != 0 {
		patchedComment, err := api.downloadAndPatchCommentImage(savedComment.Id, comment.Image)
		if err != nil {
			return savedComment, err
		}
		savedComment.Image = patchedComment.Image
	}

	return savedComment, nil
}

func (api *StockAPI) downloadAndPatchCommentImage(commentId int, imageUrl string) (models.Comment, error) {
	var patchedComment models.Comment

	downloadedImg, format, err := utils.DownloadImage(imageUrl)
	if err != nil {
		return patchedComment, err
	}

	body, contType, err := api.createImageBody(downloadedImg, "id", commentId, format)
	if err != nil {
		return patchedComment, err
	}

	patchedComment, err = api.patchCommentImage(commentId, body, contType)
	if err != nil {
		return patchedComment, err
	}

	return patchedComment, nil
}


func (api *StockAPI) patchCommentImage(commentId int, body io.Reader, contentType string) (models.Comment, error) {
	var patchedComment models.Comment

	imageURL := fmt.Sprintf("%s/comments/%d/", api.URL, commentId)
	req, err := http.NewRequest("PATCH", imageURL, body)
	if err != nil {
		return patchedComment, err
	}
	req.Header.Add("Content-Type", contentType)

	resp, err := api.client.Do(req)
	if err != nil {
		return patchedComment, err
	}

	err = utils.ParseResponseBody(resp, &patchedComment)
	if err != nil {
		return patchedComment, err
	}

	return patchedComment, nil
}
