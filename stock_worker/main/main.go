package main

import (
	"log"
	"vkstock/stock_worker/backend_api"
	"vkstock/stock_worker/models"
)

//func main() {
//	vkRequester := requester.NewVKRequester(
//		"125433e8125433e8125433e8b91226a08111254125433e84cb77682426af7c6780f2899",
//		"5.52",
//		)
//	vkRequester2 := requester.NewVKRequester(
//		"17fbc948d00e2e6952b404a8b5523f74468dfea47c6c30d4f55428aae34dfb6eb3c66b16dff263ed10deb",
//		"5.52",
//	)
//	vkCollector := collector.NewVKCollector(vkRequester)
//	vkPublisher := publisher.NewVKPublisher(vkRequester2)
//	vkBuilder := builder.NewVKPostBuilder(vkRequester2)
//
//	posts, _ := vkCollector.GetPosts("-20629724", 2)
//	for _, post := range posts {
//		vkBuilder.Reset()
//		vkBuilder.SetText(post.Text)
//		err := vkBuilder.SetPhotoByFile("/home/skupov/go/src/stock_worker/main/Screenshot from 2020-06-10 20-16-45.png", "196300082")
//		if err == nil {
//			vkPost := vkBuilder.GetPost()
//			vkPublisher.Post("-196300082", vkPost)
//		}
//	}
//}

func main() {
	api := backend_api.NewStockAPI("http://localhost:8000/api/1.0")

	image := models.PostImage{
		Image:  "https://lh3.googleusercontent.com/proxy/-Cwzls3-ws4U0ROy1AM8zTB40XMCz6YbcdG93qZbUHedmcdy3RhIZRdJg129rZeg3y0FaA9CDZT2F4h9XHCwQKusS114DdBcHOpPeRkkbWON",
		PostId: 1,
	}

	image, err := api.DownloadAndSaveImage(image)
	if err != nil {
		log.Print(err)
	}

	log.Print(image)

	//sources, err := api.GetSources()
	//source := sources[0]
	//
	//params := map[string]string {
	//	"ordering": "-date",
	//	"source_id": strconv.Itoa(source.Id),
	//	"count": "1",
	//}
	//
	//posts, err := api.GetPosts(params)
	//if err != nil {
	//	return
	//}
	//
	//lastRecordId := 0
	//if len(posts) > 0 {
	//	lastRecordId, _ = strconv.Atoi(posts[0].PlatformId)
	//}
	//
	//vkRequester := requester.NewVKRequester(
	//	"125433e8125433e8125433e8b91226a08111254125433e84cb77682426af7c6780f2899",
	//	"5.52",
	//	)
	//vkCollector := collector.NewVKCollector(vkRequester)
	//
	//posts, err = vkCollector.GetPosts("-20629724", lastRecordId)
	//if err != nil {
	//	log.Print(err)
	//}
	//
	//for _, post := range posts {
	//	post.SourceId = 1
	//
	//	_, err = api.SavePost(post)
	//	if err != nil {
	//		log.Print(err)
	//	}
	//}

}
