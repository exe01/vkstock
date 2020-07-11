package backend_api

import (
	"strconv"
	"time"
	"vkstock/stock_worker/models"
	"vkstock/stock_worker/utils"
)

func (api *StockAPI) GetProjectById(id int) (models.Project, error) {
	var project models.Project

	resp, err := api.GetModelById("projects", strconv.Itoa(id))
	if err != nil {
		return project, ModelNotFound{
			When:time.Now(),
			What: "project not found",
		}
	}

	err = utils.ParseResponseBody(resp, &project)
	if err != nil {
		return project, err
	}

	return project, nil
}
