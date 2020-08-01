package main

import (
	"errors"
	"fmt"
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
	"gopkg.in/ahmdrz/goinsta.v2"
)

func main() {
	stockAPI := backend_api.NewStockAPI("http://backend:8000", "1.0")
	finished := make(chan bool)

	go postPosts(stockAPI, 1, 30, finished)
	go collectPosts(stockAPI, 10, finished)

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

		for _, project := range projects {
			if err := postAndSaveReadyPost(project, minutesBetweenPosts, stockAPI); err != nil {
				log.Print(err)
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

func postAndSaveReadyPost(project models.Project, minutesBetweenPosts int64, stockAPI *backend_api.StockAPI) error {
	projectType, err := stockAPI.GetTypeById(project.TypeId)
	if err != nil {
		log.Println("Error while getting type.")
		return err
	}

	lastPostedPost, err := stockAPI.GetLastPostedPost(project.Id)
	if err != nil {
		log.Println("Error while getting last posted post.")
		log.Println(err)
	}

	difInMinutes := utils.DifInMinutesFromNowUnix(lastPostedPost.PostedDate)
	if difInMinutes > minutesBetweenPosts {
		acceptedPost, err := stockAPI.GetFirstAcceptedPost(project.Id)
		if err != nil {
			return nil
		}
		log.Printf("Try to prepare post %d from project %s for publishing in platform %s",
			acceptedPost.Id, project.Name, project.PlatformId)

		var postedPost models.RenderedPost
		switch projectType.Name {
		case "vk_group": {
			// Skip posts of projects without platform id
			if project.PlatformId == "" {
				return nil
			}

			vkRequester := requester.NewVKRequester(
				projectType.Token,
				project.Token,
				"5.52",
			)

			postedPost, err = postVkPost(acceptedPost, project.PlatformId, vkRequester)
			if err != nil {
				log.Println("Error while posting post.")
				return err
			}
		}
		case "instagram": {
			username, pass, err := utils.ParseUsernameAndPassFromToken(project.Token)
			if err != nil {
				log.Println("Error while parse instagram token.")
				return err
			}

			insta := goinsta.New(username, pass)

			postedPost, err = postInstagramPost(acceptedPost, insta)
			if err != nil {
				log.Println("Error while posting post.")
				return err
			}

			if err := insta.Logout(); err != nil {
				log.Println("Error while logout from instagram.")
				return err
			}
		}
		default: {
			errorMsg := fmt.Sprintf("type %s is unknown", projectType.Name)
			return errors.New(errorMsg)
		}
		}

		savedRenderedPost, err := stockAPI.PatchRenderedPost(postedPost)
		if err != nil {
			log.Print(err)
		} else {
			log.Printf("Post %d was updated from AC to PO", savedRenderedPost.Id)
		}
	}

	return nil
}

func postVkPost(post models.RenderedPost, platformId string, vkRequester *requester.VKRequester) (models.RenderedPost, error) {
	var postedPost models.RenderedPost
	vkPostBuilder := builder.NewVKPostBuilder(vkRequester)
	vkPostPublisher := publisher.NewVKPublisher(vkRequester)

	vkPostBuilder.Reset()
	vkPostBuilder.FromGroup(true)

	if len(post.Text) > 0 {
		vkPostBuilder.SetText(post.Text)
	}

	for _, image := range post.Images {
		err := vkPostBuilder.DownloadAndSetImg(image.Image, platformId)
		if err != nil {
			log.Println("Error while setting img to vk post:")
			log.Println(err)
		}
	}

	builtPost := vkPostBuilder.GetPost()
	publishedPostId, err := vkPostPublisher.Post("-"+platformId, builtPost)
	if err != nil {
		return postedPost, err
	}

	log.Printf("Post %d was successed published. Platform id - %d", post.Id, publishedPostId)

	postedPost = post
	postedPost.PlatformId = strconv.Itoa(publishedPostId)
	postedPost.Status = "PO"
	postedPost.PostedDate = time.Now().Unix()

	return postedPost, nil
}

func postInstagramPost(post models.RenderedPost, insta *goinsta.Instagram) (models.RenderedPost, error) {
	var postedPost models.RenderedPost

	if err := insta.Login(); err != nil {
		return postedPost, err
	}

	if len(post.Images) > 0 {
		firstPostImage := post.Images[0]

		img, _, err := utils.DownloadImage(firstPostImage.Image)
		if err != nil {
			return postedPost, err
		}

		instaItem, err := insta.UploadPhoto(img, post.Text, 0, 0)
		if err != nil {
			return postedPost, err
		}

		postedPost = post
		postedPost.PlatformId = instaItem.ID
		postedPost.Status = "PO"
		postedPost.PostedDate = time.Now().Unix()

		return postedPost, nil
	}

	return postedPost, errors.New("images isn't exists")
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
		post, err := stockAPI.GetLastPost(source.Id)
		if err != nil {
			lastPostPlatformId = 0
		} else {
			lastPostPlatformId, _ = strconv.Atoi(post.PlatformId)
		}

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
