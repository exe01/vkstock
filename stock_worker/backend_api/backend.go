package backend_api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type ModelNotFound struct {
	When time.Time
	What string
}

func (e ModelNotFound) Error() string {
	return fmt.Sprintf("%v: %v", e.When, e.What)
}

type StockAPI struct {
	Address string
	Version string
	URL    string
	client *http.Client
}

func NewStockAPI(address, version string) *StockAPI {
	URL := fmt.Sprintf("%s/api/%s", address, version)

	stockAPI := &StockAPI{
		address,
		version,
		URL,
		&http.Client{},
	}

	return stockAPI
}

func (api *StockAPI) SaveModel(modelName string, model interface{}) (*http.Response, error) {
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

func (api *StockAPI) GetModels(modelName string, params map[string]string) (*http.Response, error) {
	modelURL := fmt.Sprintf("%s/%s/", api.URL, modelName)

	req, err := http.NewRequest("GET", modelURL, nil)
	if err != nil {
		return nil, err
	}

	query := req.URL.Query()
	query.Add("media_url", api.Address+"/media")

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

func (api *StockAPI) GetModelById(modelName string, id string) (*http.Response, error) {
	modelURL := fmt.Sprintf("%s/%s/%s/", api.URL, modelName, id)

	req, err := http.NewRequest("GET", modelURL, nil)
	if err != nil {
		return nil, err
	}

	query := req.URL.Query()
	query.Add("media_url", api.Address+"/media")
	req.URL.RawQuery = query.Encode()

	resp, err := api.client.Get(modelURL)
	if err != nil {
		return nil, err
	}

	return resp, nil
}

func (api *StockAPI) PatchModel(modelName string, id string, model interface{}) (*http.Response, error) {
	modelURL := fmt.Sprintf("%s/%s/%s/", api.URL, modelName, id)

	modelBytes, err := json.Marshal(model)
	if err != nil {
		return nil, err
	}
	modelReader := bytes.NewReader(modelBytes)

	req, err := http.NewRequest("PATCH", modelURL, modelReader)
	if err != nil {
		return nil, err
	}
	req.Header.Add("Content-Type", "application/json")

	resp, err := api.client.Do(req)
	if err != nil {
		return nil, err
	}

	return resp, nil
}
