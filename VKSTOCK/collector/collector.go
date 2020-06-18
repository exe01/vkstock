package collector

import (
	"VKSTOCK/requester"
	"strconv"
)

type VKGetWallResponse struct {
	Response struct {
		Count int				`json:"count"`
		Items []VKPost			`json:"items"`
		Profiles []interface{}	`json:"profiles"`
		Groups []interface{}	`json:"groups"`
	} 						`json:"response"`
}

type VKPost struct {
	Id int						`json:"id"`
	Attachments []interface{}	`json:"attachments"`
	Text string					`json:"text"`
	Comments struct {
		CanPost int					`json:"can_post"`
		Count int					`json:"count"`
	}							`json:"comments"`
	Date int					`json:"date"`
	FromId int					`json:"from_id"`
	Likes struct {
		CanLike int					`json:"can_like"`
		CanPublish int				`json:"can_publish"`
		Count int					`json:"count"`
		UserLikes int				`json:"user_likes"`
	}							`json:"likes"`
	MarkedAsAds int				`json:"marked_as_ads"`
	OwnerId int					`json:"owner_id"`
	PostSource struct {
		Platform string				`json:"platform"`
		Type string					`json:"type"`
	}							`json:"post_source"`
	PostType string				`json:"post_type"`
	Reposts struct {
		Count int				`json:"count"`
		UserReposted int		`json:"user_reposted"`
	}								`json:"reposts"`
}

//type Collector interface {
//	GetPosts(from string, count int) []interface{}
//}

type VKCollector struct {
	*requester.VKRequester
}

func NewVKCollector(vkRequester *requester.VKRequester) *VKCollector {
	vkCollector := &VKCollector{
		vkRequester,
	}

	return vkCollector
}

func (c *VKCollector) GetPosts(from string, count int) ([]VKPost, error) {
	params := map[string]string{
		"owner_id": from,
		"count": strconv.Itoa(count),
	}

	req, err := c.CreateVKRequest("GET", "method/wall.get", params, nil)
	if err != nil {
		return nil, err
	}

	resp, err := c.Client.Do(req)
	if err != nil {
		return nil, err
	}

	var vkWall VKGetWallResponse
	err = c.ParseResponseBody(resp, &vkWall)
	if err != nil {
		return nil, err
	}

	return vkWall.Response.Items, nil
}

//func (c *VKCollector) parseGetWall(body io.ReadCloser) (*VKGetWallResponse, error) {
//	defer body.Close()
//
//	var vkWall VKGetWallResponse
//	bodyBytes, _ := ioutil.ReadAll(body)
//	if err := json.Unmarshal(bodyBytes, &vkWall); err != nil {
//		return nil, err
//	}
//
//	return &vkWall, nil
//}
