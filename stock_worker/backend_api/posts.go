package backend_api

import (
	"bytes"
	"io"
	"mime/multipart"
	"net/http"
	"strconv"
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

//func (api *StockAPI) DownloadAndSaveImage(image models.PostImage) (models.PostImage, error) {
//	resp, err := http.Get(image.Image)
//	if err != nil {
//		return image, err
//	}
//
//	mimeType := resp.Header.Get("Content-Type")
//	typeAndFormat := strings.Split(mimeType, "/")
//	if len(typeAndFormat) < 2 {
//		return image, errors.New("format of image is undefined")
//	}
//	format := typeAndFormat[1]
//
//	body := &bytes.Buffer{}
//	writer := multipart.NewWriter(body)
//
//	part, _ := writer.CreateFormFile("image", "randomname." + format)
//	io.Copy(part, resp.Body)
//	resp.Body.Close()
//
//	err = writer.WriteField("post_id", strconv.Itoa(image.PostId))
//	if err != nil {
//		return image, err
//	}
//
//	err = writer.Close()
//	if err != nil {
//		return image, err
//	}
//
//	// Load image
//	imgUrl := api.URL + "/post_images/"
//	req, err := http.NewRequest("POST", imgUrl, body)
//	if err != nil {
//		return image, nil
//	}
//	req.Header.Add("Content-Type", writer.FormDataContentType())
//
//	resp, err = api.client.Do(req)
//
//	if err != nil {
//		return image, nil
//	}
//
//	err = utils.ParseResponseBody(resp, &image)
//	if err != nil {
//		return image, err
//	}
//
//	return image, nil
//}

func (api *StockAPI) DownloadAndSaveImage(image models.PostImage) (models.PostImage, error) {
	downloadedImg, format, err := utils.DownloadImage(image.Image)
	if err != nil {
		return image, err
	}

	body, contType,  err := api.createPostImageBody(downloadedImg, image.PostId, format)
	if err != nil {
		return image, err
	}

	savedImage, err := api.saveImage(body, contType)
	if err != nil {
		return image, err
	}

	return savedImage, nil
}

func (api *StockAPI) createPostImageBody(image io.Reader, postId int, format string) (io.Reader, string, error) {
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	part, err := writer.CreateFormFile("image", "stockApiLoader." + format)
	if err != nil {
		return nil, "", err
	}

	_, err = io.Copy(part, image)
	if err != nil {
		return nil, "", err
	}

	err = writer.WriteField("post_id", strconv.Itoa(postId))
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

func (api *StockAPI) saveImage(body io.Reader, contentType string) (models.PostImage, error) {
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

