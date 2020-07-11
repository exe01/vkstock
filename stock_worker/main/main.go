package main

import (
	"log"
	"strconv"
	"vkstock/stock_worker/backend_api"
	"vkstock/stock_worker/collector"
	"vkstock/stock_worker/models"
	"vkstock/stock_worker/requester"
)

func main() {
	stockAPI := backend_api.NewStockAPI("http://localhost:8000/api/1.0")

	posts := getNewPosts(stockAPI)
	for _, post := range posts {
		savedPost, err := stockAPI.SavePost(post)
		if err != nil {
			log.Print(err)
			continue
		}

		_, err = stockAPI.RenderPost(savedPost.Id)
		if err != nil {
			log.Print(err)
		}
	}

}

func getNewPosts(stockAPI *backend_api.StockAPI) []models.Post {
	newPosts := make([]models.Post, 0, 20)
	sources, err := stockAPI.GetSources()
	if err !=nil {
		log.Panic(err)
	}

	for _, source := range sources {
		var lastPostPlatformId int

		type_, err := stockAPI.GetTypeById(source.TypeId)
		if err != nil {
			log.Panic(err)
		}

		newSourcePosts := make([]models.Post, 0, 20)
		switch type_.Name {
			case "vk_group": {
				project, err := stockAPI.GetProjectById(source.ProjectId)
				if err != nil {
					log.Panic(err)
				}

				vkRequester := requester.NewVKRequester(
					type_.Token,
					project.Token,
					"5.52",
				)
				vkCollector := collector.NewVKCollector(vkRequester)

				//var e backend_api.ModelNotFound
				post, err := stockAPI.GetLastPost(source.Id)
				if err != nil {
					lastPostPlatformId = 0
				} else {
					lastPostPlatformId, _ = strconv.Atoi(post.PlatformId)
				}

				ownerId := "-" + source.PlatformId
				newSourcePosts, err = vkCollector.GetPosts(ownerId, lastPostPlatformId)
				if err != nil {
					log.Panic(err)
				}
			}
		}

		for _, newSourcePost := range newSourcePosts {
			newSourcePost.SourceId = source.Id
			newPosts = append(newPosts, newSourcePost)
		}
	}

	return newPosts
}
