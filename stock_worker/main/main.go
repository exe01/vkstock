package main

import (
	"log"
	"strconv"
	"time"
	"vkstock/stock_worker/backend_api"
	"vkstock/stock_worker/builder"
	"vkstock/stock_worker/collector"
	"vkstock/stock_worker/models"
	"vkstock/stock_worker/publisher"
	"vkstock/stock_worker/requester"
	"vkstock/stock_worker/utils"
)

func main() {
	stockAPI := backend_api.NewStockAPI("http://localhost:8000", "1.0")

	postPosts(stockAPI, 0, 30)
	//
	//posts := getNewPosts(stockAPI)
	//for _, post := range posts {
	//	savedPost, err := stockAPI.SavePost(post)
	//	if err != nil {
	//		log.Print(err)
	//		continue
	//	}
	//
	//	_, err = stockAPI.RenderPost(savedPost.Id)
	//	if err != nil {
	//		log.Print(err)
	//	}
	//}
}

func postPosts(stockAPI *backend_api.StockAPI, timeOfCheckingAccepted int, minutesBetweenPosts int64) {
	vkRequester := requester.NewVKRequester(
		"125433e8125433e8125433e8b91226a08111254125433e84cb77682426af7c6780f2899",
		"17fbc948d00e2e6952b404a8b5523f74468dfea47c6c30d4f55428aae34dfb6eb3c66b16dff263ed10deb",
		"5.52",
	)
	vkPostBuilder := builder.NewVKPostBuilder(vkRequester)
	vkPostPublisher := publisher.NewVKPublisher(vkRequester)

	for {
		projects, err := stockAPI.GetProjects(nil)
		if err != nil {
			log.Print(err)
		}

		for _, project := range projects  {
			if project.PlatformId == "" {
				continue
			}

			lastPostedPost, err := stockAPI.GetLastPostedPost(project.Id)
			if err != nil {
				log.Print(err)
			}

			difInMinutes := utils.DifInMinutesFromNowUnix(lastPostedPost.PostedDate)
			if difInMinutes > minutesBetweenPosts{
				acceptedPost, err := stockAPI.GetFirstAcceptedPost(project.Id)
				if err != nil {
					continue
				}

				vkPostBuilder.Reset()
				vkPostBuilder.FromGroup(true)

				if len(acceptedPost.Text) > 0 {
					vkPostBuilder.SetText(acceptedPost.Text)
				}

				for _, image := range acceptedPost.Images {
					err = vkPostBuilder.DownloadAndSetImg(image.Image, project.PlatformId)
					if err != nil {
						log.Print(err)
					}
				}

				buildedPost := vkPostBuilder.GetPost()
				publishedPostId, err := vkPostPublisher.Post("-"+project.PlatformId, buildedPost)
				if err != nil {
					log.Print(err)
					continue
				}

				acceptedPost.PlatformId = strconv.Itoa(publishedPostId)
				acceptedPost.Status = "PO"
				acceptedPost.PostedDate = time.Now().Unix()
				savedPenderedPost, err := stockAPI.PatchRenderedPost(acceptedPost)
				if err != nil {
					log.Print(err)
				}

				log.Printf("Published post %d in %d", savedPenderedPost.Id, project.Id)
			}
		}

		break
	}
}

func getNewPosts(stockAPI *backend_api.StockAPI) []models.Post {
	newPosts := make([]models.Post, 0, 20)
	sources, err := stockAPI.GetSources(nil)
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
