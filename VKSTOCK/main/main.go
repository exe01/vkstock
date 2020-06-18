package main

import (
	"VKStock/VKSTOCK/builder"
	"VKStock/VKSTOCK/collector"
	"VKStock/VKSTOCK/publisher"
	"VKStock/VKSTOCK/requester"
)

func main() {
	vkRequester := requester.NewVKRequester(
		"125433e8125433e8125433e8b91226a08111254125433e84cb77682426af7c6780f2899",
		"5.52",
		)
	vkRequester2 := requester.NewVKRequester(
		"17fbc948d00e2e6952b404a8b5523f74468dfea47c6c30d4f55428aae34dfb6eb3c66b16dff263ed10deb",
		"5.52",
	)
	vkCollector := collector.NewVKCollector(vkRequester)
	vkPublisher := publisher.NewVKPublisher(vkRequester2)
	vkBuilder := builder.NewVKPostBuilder(vkRequester2)

	posts, _ := vkCollector.GetPosts("-20629724", 2)
	for _, post := range posts {
		vkBuilder.Reset()
		vkBuilder.SetText(post.Text)
		err := vkBuilder.SetPhotoByFile("/home/skupov/go/src/VKSTOCK/main/Screenshot from 2020-06-10 20-16-45.png", "196300082")
		if err == nil {
			vkPost := vkBuilder.GetPost()
			vkPublisher.Post("-196300082", vkPost)
		}
	}
}
