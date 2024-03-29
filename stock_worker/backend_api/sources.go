package backend_api

import (
	"vkstock/stock_worker/models"
	"vkstock/stock_worker/utils"
)

func (api *StockAPI) GetSources(params map[string]string) ([]models.Source, error) {
	if params == nil {
		params = map[string]string {
			"count": "100",
		}
	} else {
		params["count"] = "100"
	}

	resp, err := api.GetModels("sources", params)
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
