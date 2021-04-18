package backend_api

import (
	"bytes"
	"io"
	"mime/multipart"
	"strconv"
)

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
