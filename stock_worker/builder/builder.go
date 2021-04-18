package builder

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"strconv"
	"strings"
	"vkstock/stock_worker/requester"
	"vkstock/stock_worker/utils"
)

type VKWallUploadServer struct {
	Response struct {
		UploadURL string `json:"upload_url"`
	} `json:"response"`
}

type VKUploadResponse struct {
	Server int    `json:"server"`
	Photo  string `json:"photo"`
	Hash   string `json:"hash"`
}

type VKSaveWallResponse struct {
	Photos []VKPhoto `json:"response"`
}

type VKPhoto struct {
	Id      int    `json:"id"`
	AlbumId int    `json:"album_id"`
	OwnerId int    `json:"owner_id"`
	UserId  int    `json:"user_id"`
	Text    string `json:"text"`
	Date    int    `json:"date"`
}

type VKPostBuilder struct {
	*requester.VKRequester
	post map[string]string
}

func NewVKPostBuilder(vkRequester *requester.VKRequester) *VKPostBuilder {
	vkPostBuilder := &VKPostBuilder{
		vkRequester,
		make(map[string]string),
	}

	return vkPostBuilder
}

func (b *VKPostBuilder) Reset() {
	b.post = make(map[string]string)
}

func (b *VKPostBuilder) SetText(text string) {
	b.post["message"] = text
}

func (b *VKPostBuilder) FromGroup(k bool) {
	if k {
		b.post["from_group"] = "1"
	} else {
		b.post["from_group"] = "0"
	}
}

func (b *VKPostBuilder) SetAttachments(attachments []string) {
	attachmentsParam := strings.Join(attachments, ",")
	b.post["attachments"] = attachmentsParam
}

func (b *VKPostBuilder) DownloadAndSetImg(url, toOwner string) error {
	uploadServerURL, err := b.getWallUploadServerURL(toOwner)
	if err != nil {
		return err
	}

	uploadResponse, err := b.loadPhoto(uploadServerURL, url)
	if err != nil {
		return err
	}

	vkPhoto, err := b.saveWallPhoto(toOwner, uploadResponse)
	if err != nil {
		return err
	}

	attachment := fmt.Sprintf("photo%d_%d", vkPhoto.OwnerId, vkPhoto.Id)
	attachments := b.post["attachments"]
	if len(attachments) > 0 {
		attachments = attachments + "," + attachment
	} else {
		attachments = attachment
	}
	b.post["attachments"] = attachments

	return nil
}

func (b *VKPostBuilder) GetPost() map[string]string {
	return b.post
}

func (b *VKPostBuilder) getWallUploadServerURL(groupId string) (string, error) {
	params := map[string]string{
		"group_id": groupId,
	}

	req, err := b.CreatePrivilegedVKRequest("GET", "method/photos.getWallUploadServer", params, nil)
	if err != nil {
		return "", err
	}

	resp, err := b.Client.Do(req)
	if err != nil {
		return "", err
	}

	var vkUploadServer VKWallUploadServer
	err = utils.ParseResponseBody(resp, &vkUploadServer)
	if err != nil {
		return "", err
	}

	return vkUploadServer.Response.UploadURL, nil
}

func (b *VKPostBuilder) loadPhoto(uploadServerURL, imageUrl string) (*VKUploadResponse, error) {
	photo, format, err := utils.DownloadImage(imageUrl)
	if err != nil {
		return nil, err
	}

	photoName := utils.GenerateRandomString("."+format)

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	part, _ := writer.CreateFormFile("photo", photoName)
	io.Copy(part, photo)
	photo.Close()

	err = writer.Close()
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", uploadServerURL, body)
	if err != nil {
		return nil, err
	}
	req.Header.Add("Content-Type", writer.FormDataContentType())

	resp, err := b.Client.Do(req)
	if err != nil {
		return nil, err
	}

	var uploadResponse VKUploadResponse
	err = utils.ParseResponseBody(resp, &uploadResponse)
	if err != nil {
		return nil, err
	}

	return &uploadResponse, nil
}

func (b *VKPostBuilder) saveWallPhoto(groupId string, uploadResponse *VKUploadResponse) (*VKPhoto, error) {
	params := map[string]string{
		"server":   strconv.Itoa(uploadResponse.Server),
		"hash":     uploadResponse.Hash,
		"photo":    uploadResponse.Photo,
		"group_id": groupId,
	}

	req, err := b.CreatePrivilegedVKRequest("GET", "method/photos.saveWallPhoto", params, nil)
	if err != nil {
		return nil, err
	}

	resp, err := b.Client.Do(req)
	if err != nil {
		return nil, err
	}

	var vkSaveWallResponse VKSaveWallResponse
	err = utils.ParseResponseBody(resp, &vkSaveWallResponse)
	if err != nil {
		return nil, err
	}

	if len(vkSaveWallResponse.Photos) == 0 {
		return nil, errors.New("photo isn't saved (empty array returned)")
	}

	return &vkSaveWallResponse.Photos[0], nil
}
