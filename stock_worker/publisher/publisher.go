package publisher

import (
	"vkstock/stock_worker/requester"
	"vkstock/stock_worker/utils"
)

type SavedVKPost struct {
	Response struct {
		PostId int `json:"post_id"`
	} `json:"response"`
}

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

func (p *VKPublisher) Post(to string, post map[string]string) (int, error) {
	post["owner_id"] = to

	req, err := p.CreatePrivilegedVKRequest("GET", "method/wall.post", post, nil)
	if err != nil {
		return 0, err
	}

	resp, err := p.Client.Do(req)
	if err != nil {
		return 0, err
	}

	var savedVKPost SavedVKPost
	err = utils.ParseResponseBody(resp, &savedVKPost)
	if err != nil {
		return 0, err
	}

	return savedVKPost.Response.PostId, nil
}
