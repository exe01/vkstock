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
	stockAPI := backend_api.NewStockAPI("http://backend:8000", "1.0")
	finished := make(chan bool)

	go postPosts(stockAPI, 1, 30, finished)
	go collectPosts(stockAPI, 10, finished)

	<- finished
	<- finished
}

func postPosts(stockAPI *backend_api.StockAPI, timeOfCheckingAccepted time.Duration,
	minutesBetweenPosts int64, finished chan bool) {
	firstRunning := true

	for {
		if !firstRunning {
			time.Sleep(timeOfCheckingAccepted * time.Minute)
		}
		firstRunning = false

		log.Println("Begin publish work")

		projects, err := stockAPI.GetProjects(nil)
		if err != nil {
			log.Println("Error while getting project:")
			log.Println(err)
			continue
		}

		for _, project := range projects  {
			if project.PlatformId == "" {
				continue
			}
			projectType, err := stockAPI.GetTypeById(project.TypeId)
			if err != nil {
				log.Println("Error while getting type:")
				log.Println(err)
				continue
			}

			vkRequester := requester.NewVKRequester(
				projectType.Token,
				project.Token,
				"5.52",
			)
			vkPostBuilder := builder.NewVKPostBuilder(vkRequester)
			vkPostPublisher := publisher.NewVKPublisher(vkRequester)

			lastPostedPost, err := stockAPI.GetLastPostedPost(project.Id)
			if err != nil {
				log.Println("Error while getting last posted post:")
				log.Println(err)
			}

			difInMinutes := utils.DifInMinutesFromNowUnix(lastPostedPost.PostedDate)
			if difInMinutes > minutesBetweenPosts{
				acceptedPost, err := stockAPI.GetFirstAcceptedPost(project.Id)
				if err != nil {
					continue
				}
				log.Printf("Try to prepare post %d from project %s for publishing in platform %s",
					acceptedPost.Id, project.Name, project.PlatformId)

				vkPostBuilder.Reset()
				vkPostBuilder.FromGroup(true)

				if len(acceptedPost.Text) > 0 {
					vkPostBuilder.SetText(acceptedPost.Text)
				}

				for _, image := range acceptedPost.Images {
					err = vkPostBuilder.DownloadAndSetImg(image.Image, project.PlatformId)
					if err != nil {
						log.Println("Error while setting img to vk post:")
						log.Println(err)
					}
				}

				builtPost := vkPostBuilder.GetPost()
				publishedPostId, err := vkPostPublisher.Post("-"+project.PlatformId, builtPost)
				if err != nil {
					log.Print(err)
					continue
				}

				log.Printf("Post %d was successed published. Platform id - %d", acceptedPost.Id, publishedPostId)

				acceptedPost.PlatformId = strconv.Itoa(publishedPostId)
				acceptedPost.Status = "PO"
				acceptedPost.PostedDate = time.Now().Unix()
				savedPenderedPost, err := stockAPI.PatchRenderedPost(acceptedPost)
				if err != nil {
					log.Print(err)
				}

				log.Printf("Post %d was updated from AC to PO", savedPenderedPost.Id)
			}
		}
		log.Println("All project checked")
	}

	finished <- true
}

func collectPosts(stockAPI *backend_api.StockAPI, timeOfCheckingNewPosts time.Duration,
	finished chan bool) {

	firstRunning := true

	for {
		if !firstRunning {
			time.Sleep(timeOfCheckingNewPosts * time.Minute)
		}
		firstRunning = false

		log.Println("Begin collecting work")

		posts := getNewPosts(stockAPI)
		for _, post := range posts {
			savedPost, err := stockAPI.SavePost(post)
			if err != nil {
				log.Printf("Error while save post")
				log.Print(err)
				continue
			}

			_, err = stockAPI.RenderPost(savedPost.Id)
			if err != nil {
				log.Printf("Error while render post %d", savedPost.Id)
				log.Print(err)
			}
		}

		log.Println("Collecting ended")
	}

	finished <- true
}

func getNewPosts(stockAPI *backend_api.StockAPI) []models.Post {
	newPosts := make([]models.Post, 0, 20)
	sources, err := stockAPI.GetSources(nil)
	if err !=nil {
		log.Println("Error while got sources")
		log.Print(err)
	}

	for _, source := range sources {
		var lastPostPlatformId int

		type_, err := stockAPI.GetTypeById(source.TypeId)
		if err != nil {
			log.Printf("Error while got type %s", source.TypeId)
			log.Print(err)
			continue
		}

		newSourcePosts := make([]models.Post, 0, 20)
		switch type_.Name {
			case "vk_group": {
				project, err := stockAPI.GetProjectById(source.ProjectId)
				if err != nil {
					log.Printf("Error while got project %s", source.ProjectId)
					log.Print(err)
					continue
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

				log.Printf("Try to collect posts from %s", source.Name)

				ownerId := "-" + source.PlatformId
				newSourcePosts, err = vkCollector.GetPosts(ownerId, lastPostPlatformId)
				if err != nil {
					log.Printf("Error while got posts %s", source.Name)
					log.Print(err)
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
