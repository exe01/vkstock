package backend_api

import (
	"strconv"
	"time"
	"vkstock/stock_worker/models"
	"vkstock/stock_worker/utils"
)

func (api *StockAPI) GetTypeById(id int) (models.Type, error) {
	var type_ models.Type

	resp, err := api.GetModelById("types", strconv.Itoa(id))
	if err != nil {
		return type_, ModelNotFound{
			When:time.Now(),
			What: "type not found",
		}
	}

	err = utils.ParseResponseBody(resp, &type_)
	if err != nil {
		return type_, err
	}

	return type_, nil
}
