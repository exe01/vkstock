package backend_api

import (
	"vkstock/stock_worker/models"
	"vkstock/stock_worker/utils"
)

func (api *StockAPI) GetSources() ([]models.Source, error)  {
	sourceURL := api.URL + "/sources"

	resp, err := api.client.Get(sourceURL)
	if err != nil {
		return nil, err
	}

	var setSources models.SetSources

	err = utils.ParseResponseBody(resp, &setSources)
	if err != nil {
		return nil, err
	}

	return setSources.Results, nil
}
