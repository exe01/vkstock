package backend_api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

type StockAPI struct {
	URL string
	client *http.Client
}

func NewStockAPI (URL string) *StockAPI {
	stockAPI := &StockAPI{
		URL,
		&http.Client{},
	}

	return stockAPI
}

func (api *StockAPI) SaveModel (modelName string, model interface{}) (*http.Response, error) {
	modelURL := fmt.Sprintf("%s/%s/", api.URL, modelName)

	modelBytes, err := json.Marshal(model)
	if err != nil {
		return nil, err
	}
	modelReader := bytes.NewReader(modelBytes)
	resp, err := api.client.Post(modelURL, "application/json", modelReader)
	if err != nil {
		return nil, err
	}

	return resp, nil
}

func (api *StockAPI) GetModels (modelName string, params map[string]string) (*http.Response, error) {
	modelURL := fmt.Sprintf("%s/%s/", api.URL, modelName)

	req, err := http.NewRequest("GET", modelURL, nil)
	if err != nil {
		return nil, err
	}

	query := req.URL.Query()

	if params != nil {
		for key, value := range params {
			query.Add(key, value)
		}
	}

	req.URL.RawQuery = query.Encode()

	resp, err := api.client.Do(req)
	if err != nil {
		return nil, err
	}

	return resp, nil
}
