package backend_api

import (
	"bytes"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"strconv"
	"time"
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

func (api *StockAPI) GetLastPost(sourceId int) (models.Post, error) {
	var post models.Post
	params := map[string]string {
		"ordering": "-date",
		"source_id": strconv.Itoa(sourceId),
		"count": "1",
	}

	posts, err := api.GetPosts(params)
	if err != nil {
		return post, nil
	}
	if len(posts) == 0 {
		return post, ModelNotFound{
			When: time.Now(),
			What: "post not found",
		}
	}

	return posts[0], nil
}

func (api *StockAPI) SavePost(post models.Post) (models.Post, error) {
	comments := post.Comments
	images := post.Images

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

	savedImages := make([]models.PostImage, 0, len(images))
	for _, image := range images {
		image.PostId = savedPost.Id
		savedImage, err := api.downloadAndSavePostImage(image)
		if err != nil {
			continue
		}
		savedImages = append(savedImages, savedImage)
	}

	savedPost.Comments = savedComments
	savedPost.Images = savedImages

	return savedPost, nil
}

func (api *StockAPI) savePost(post models.Post) (models.Post, error) {
	var savedPost models.Post

	resp, err := api.SaveModel("posts", post)
	if err != nil {
		return post, nil
	}

	err = utils.ParseResponseBody(resp, &savedPost)
	if err != nil {
		return post, err
	}

	return savedPost, nil
}

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
		return comment, nil
	}

	err = utils.ParseResponseBody(resp, &savedComment)
	if err != nil {
		return comment, err
	}

	if len(comment.Image) != 0 {
		patchedComment, err := api.downloadAndPatchCommentImage(savedComment.Id, comment.Image)
		if err != nil {
			return savedComment, nil
		}
		savedComment.Image = patchedComment.Image
	}

	return savedComment, nil
}

func (api *StockAPI) downloadAndSavePostImage(image models.PostImage) (models.PostImage, error) {
	var savedImage models.PostImage

	downloadedImg, format, err := utils.DownloadImage(image.Image)
	if err != nil {
		return savedImage, err
	}

	body, contType, err := api.createImageBody(downloadedImg, "post_id", image.PostId, format)
	if err != nil {
		return savedImage, err
	}

	savedImage, err = api.savePostImage(body, contType)
	if err != nil {
		return savedImage, err
	}

	return savedImage, nil
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


func (api *StockAPI) createImageBody(image io.Reader, idName string, id int, format string) (io.Reader, string, error) {
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	part, err := writer.CreateFormFile("image", "stockApiLoader."+format)
	if err != nil {
		return nil, "", err
	}

	_, err = io.Copy(part, image)
	if err != nil {
		return nil, "", err
	}

	err = writer.WriteField(idName, strconv.Itoa(id))
	if err != nil {
		return nil, "", err
	}

	err = writer.Close()
	if err != nil {
		return nil, "", err
	}

	contentType := writer.FormDataContentType()

	return body, contentType, nil
}

func (api *StockAPI) savePostImage(body io.Reader, contentType string) (models.PostImage, error) {
	var image models.PostImage

	imageURL := api.URL + "/post_images/"
	req, err := http.NewRequest("POST", imageURL, body)
	if err != nil {
		return image, err
	}
	req.Header.Add("Content-Type", contentType)

	resp, err := api.client.Do(req)
	if err != nil {
		return image, err
	}

	err = utils.ParseResponseBody(resp, &image)
	if err != nil {
		return image, err
	}

	return image, nil
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
