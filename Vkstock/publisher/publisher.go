package publisher

import (
	"VKSTOCK/requester"
	"encoding/json"
	"io"
	"io/ioutil"
	"log"
)

type Publisher interface {
	Post(to string, post map[string]string)
}

type VKPublisher struct {
	*requester.VKRequester
}

func NewVKPublisher(vkRequester *requester.VKRequester) *VKPublisher {
	vkPublisher := &VKPublisher{
		vkRequester,
	}

	return vkPublisher
}

func (p *VKPublisher) Post(to string, post map[string]string) error {
	post["owner_id"] = to
	post["from_group"] = "1"

	req, err := p.CreateVKRequest("GET", "method/wall.post", post, nil)
	if err != nil {
		return err
	}

	resp, err := p.Client.Do(req)
	if err != nil {
		return err
	}

	return p.parsePostedPost(resp.Body)
}

func (p *VKPublisher) parsePostedPost(body io.ReadCloser) error {
	defer body.Close()

	var jsonBody interface{}
	bodyBytes, _ := ioutil.ReadAll(body)
	err := json.Unmarshal(bodyBytes, &jsonBody)
	if err != nil {
		log.Print(err)
	}

	prettyPosts, _ := json.MarshalIndent(jsonBody, "", "\t")
	log.Print("Posted post: " + string(prettyPosts))

	return nil
}
