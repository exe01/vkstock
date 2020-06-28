package builder

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"
	"strconv"
	"strings"
	"vkstock/stock_worker/requester"
	"vkstock/stock_worker/utils"
)

type VKWallUploadServer struct {
	Response struct {
		UploadURL string	`json:"upload_url"`
	}					`json:"response"`
}

type VKUploadResponse struct {
	Server      int    `json:"server"`
	Photo  		string `json:"photo"`
	Hash        string `json:"hash"`
}

type VKSaveWallResponse struct {
	Photos []VKPhoto `json:"response"`
}

type VKPhoto struct {
	Id 		int		`json:"id"`
	AlbumId int		`json:"album_id"`
	OwnerId int		`json:"owner_id"`
	UserId 	int		`json:"user_id"`
	Text 	string	`json:"text"`
	Date 	int		`json:"date"`
}

type PostBuilder interface {
	Reset()
	SetText(text string)
	SetAttachments(attachments []string)
	GetPost() map[string]string
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

func (b *VKPostBuilder) Reset () {
	b.post = make(map[string]string)
}

func (b *VKPostBuilder) SetText(text string) {
	b.post["message"] = text
}

func (b *VKPostBuilder) SetAttachments(attachments []string) {
	attachmentsParam := strings.Join(attachments, ",")
	b.post["attachments"] = attachmentsParam
}

func (b *VKPostBuilder) SetPhotoByFile(file, groupId string) error {
	uploadServerURL, err := b.getWallUploadServerURL(groupId)
	if err != nil {
		return err
	}

	uploadResponse, err := b.loadPhoto(uploadServerURL, file)
	if err != nil {
		return err
	}

	vkPhoto, err := b.saveWallPhoto(groupId, uploadResponse)
	if err != nil {
		return err
	}

	b.post["attachments"] = "photo" + strconv.Itoa(vkPhoto.OwnerId) + "_" + strconv.Itoa(vkPhoto.Id)
	return nil
}

func (b *VKPostBuilder) GetPost() map[string]string {
	return b.post
}

func (b *VKPostBuilder) getWallUploadServerURL(groupId string) (string, error) {
	params := map[string]string{
		"group_id": groupId,
	}

	req, err := b.CreateVKRequest("GET", "method/photos.getWallUploadServer", params, nil)
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

func (b *VKPostBuilder) loadPhoto(uploadServerURL, path string) (*VKUploadResponse, error) {
	size, err := utils.GetFileSizeMB(path)
	if err != nil {
		return nil, err
	}
	if size > 50 {
		errorMessage := fmt.Sprintf("size of file > 50 MB (%d MB)", size)
		return nil, errors.New(errorMessage)
	}

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	file, _ := os.Open(path)
	fileInfo, _ := file.Stat()
	part, _ := writer.CreateFormFile("photo", fileInfo.Name())
	io.Copy(part, file)
	file.Close()

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
		"server": strconv.Itoa(uploadResponse.Server),
		"hash": uploadResponse.Hash,
		"photo": uploadResponse.Photo,
		"group_id": groupId,
	}

	req, err := b.CreateVKRequest("GET", "method/photos.saveWallPhoto", params, nil)
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
