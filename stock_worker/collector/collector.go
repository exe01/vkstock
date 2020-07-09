package collector

import (
	"errors"
	"regexp"
	"sort"
	"strconv"
	"vkstock/stock_worker/models"
	"vkstock/stock_worker/requester"
	"vkstock/stock_worker/utils"
)

type VKGetPostsResponse struct {
	Response struct {
		Count    int           `json:"count"`
		Items    []VKPost      `json:"items"`
		Profiles []interface{} `json:"profiles"`
		Groups   []interface{} `json:"groups"`
	} `json:"response"`
}

type VKGetCommentsResponse struct {
	Response struct {
		Count    int           `json:"count"`
		Items    []VKComment   `json:"items"`
		Profiles []interface{} `json:"profiles"`
		Groups   []interface{} `json:"groups"`
	} `json:"response"`
}

type VKPost struct {
	Id          int          `json:"id"`
	Attachments []Attachment `json:"attachments"`
	Text        string       `json:"text"`
	Comments    struct {
		CanPost int `json:"can_post"`
		Count   int `json:"count"`
	} `json:"comments"`
	Date   int64 `json:"date"`
	FromId int   `json:"from_id"`
	Likes  struct {
		CanLike    int `json:"can_like"`
		CanPublish int `json:"can_publish"`
		Count      int `json:"count"`
		UserLikes  int `json:"user_likes"`
	} `json:"likes"`
	MarkedAsAds int `json:"marked_as_ads"`
	OwnerId     int `json:"owner_id"`
	PostSource  struct {
		Platform string `json:"platform"`
		Type     string `json:"type"`
	} `json:"post_source"`
	PostType string `json:"post_type"`
	IsPinned int    `json:"is_pinned"`
	Reposts  struct {
		Count        int `json:"count"`
		UserReposted int `json:"user_reposted"`
	} `json:"reposts"`
}

type Attachment struct {
	Type  string                 `json:"type"`
	Photo map[string]interface{} `json:"photo"`
}

type VKComment struct {
	Id     int    `json:"id"`
	Text   string `json:"text"`
	FromId int    `json:"from_id"`
	Likes  struct {
		Count     int `json:"count"`
		UserLikes int `json:"user_likes"`
		CanLike   int `json:"can_like"`
	} `json:"likes"`
}

type ByLike []VKComment

func (cs ByLike) Len() int {
	return len(cs)
}

// From the biggest to the lowest
func (cs ByLike) Less(i, j int) bool {
	return cs[i].Likes.Count > cs[j].Likes.Count
}
func (cs ByLike) Swap(i, j int) {
	cs[i], cs[j] = cs[j], cs[i]
}

type VKCollector struct {
	*requester.VKRequester
}

func NewVKCollector(vkRequester *requester.VKRequester) *VKCollector {
	vkCollector := &VKCollector{
		vkRequester,
	}

	return vkCollector
}

func (c *VKCollector) GetPosts(ownerId string, lastRecordId int) ([]models.Post, error) {
	countOfComments := 2
	posts := make([]models.Post, 0, 10)

	count := 10
	var vkPosts []VKPost
	var err error
	gettingPosts := true

	for i := 0; gettingPosts; i++ {
		vkPosts, err = c.getVKPosts(ownerId, 10, i*count)
		if err != nil {
			return nil, err
		}

		for _, vkPost := range vkPosts {
			if vkPost.MarkedAsAds != 0 || vkPost.IsPinned == 1 {
				continue
			}

			if vkPostIsNew(vkPost) {
				continue
			}

			if vkPostIsOld(vkPost) {
				gettingPosts = false
				break
			}

			if vkPost.Id < lastRecordId {
				gettingPosts = false
				break
			}

			topVKComments, err := c.getTopVKComments(ownerId, vkPost.Id, countOfComments)
			if err != nil {
				continue
			}

			comments := make([]models.Comment, 0, countOfComments)
			for _, vkComment := range topVKComments {
				comment := convertVKComment(vkComment)
				comments = append(comments, comment)
			}

			images := convertAttachments(vkPost.Attachments)

			post := convertVKPost(vkPost)
			post.Comments = comments
			post.Images = images

			posts = append(posts, post)
		}
	}

	return posts, nil
}

func vkPostIsNew(vkPost VKPost) bool {
	nowMinus1Day := utils.NowMinusDaysUnix(1)
	return vkPost.Date > nowMinus1Day
}

func vkPostIsOld(vkPost VKPost) bool {
	nowMinus2Days := utils.NowMinusDaysUnix(2)
	return nowMinus2Days > vkPost.Date
}

func (c *VKCollector) getVKPosts(ownerId string, count, offset int) ([]VKPost, error) {
	params := map[string]string{
		"owner_id": ownerId,
		"count":    strconv.Itoa(count),
		"offset":   strconv.Itoa(offset),
	}

	req, err := c.CreateVKRequest("GET", "method/wall.get", params, nil)
	if err != nil {
		return nil, err
	}

	resp, err := c.Client.Do(req)
	if err != nil {
		return nil, err
	}

	var vkResponse VKGetPostsResponse
	err = utils.ParseResponseBody(resp, &vkResponse)
	if err != nil {
		return nil, err
	}

	return vkResponse.Response.Items, nil
}

func (c *VKCollector) getTopVKComments(ownerId string, postId, countOfTop int) ([]VKComment, error) {
	allComments, err := c.getAllVKComments(ownerId, postId)
	if err != nil {
		return nil, err
	}

	sort.Sort(ByLike(allComments))

	topComments := allComments[:countOfTop]
	return topComments, nil
}

func (c *VKCollector) getAllVKComments(ownerId string, postId int) ([]VKComment, error) {
	count := 100
	allComments := make([]VKComment, 0, count)
	var vkGetCommentsResponse *VKGetCommentsResponse
	var err error

	for i := 0; ; i++ {
		vkGetCommentsResponse, err = c.getVKPostComments(ownerId, postId, count, i*count)
		if err != nil {
			return nil, err
		}

		vkComments := vkGetCommentsResponse.Response.Items
		if len(vkComments) == 0 {
			break
		}

		allComments = append(allComments, vkComments...)
	}

	return allComments, nil
}

func (c *VKCollector) getVKPostComments(ownerId string, postId, count, offset int) (*VKGetCommentsResponse, error) {
	params := map[string]string{
		"owner_id":   ownerId,
		"post_id":    strconv.Itoa(postId),
		"count":      strconv.Itoa(count),
		"offset":     strconv.Itoa(offset),
		"need_likes": "1",
	}

	req, err := c.CreateVKRequest("GET", "method/wall.getComments", params, nil)
	if err != nil {
		return nil, err
	}

	resp, err := c.Client.Do(req)
	if err != nil {
		return nil, err
	}

	var vkResponse VKGetCommentsResponse
	err = utils.ParseResponseBody(resp, &vkResponse)
	if err != nil {
		return nil, err
	}

	return &vkResponse, nil
}

func convertVKPost(vkPost VKPost) models.Post {
	post := models.Post{
		PlatformId: strconv.Itoa(vkPost.Id),
		Date:       vkPost.Date,
		SourceId:   0,
		Text:       vkPost.Text,
		Images:     nil,
		Comments:   nil,
	}

	return post
}

func convertAttachments(attachments []Attachment) []models.PostImage {
	images := make([]models.PostImage, 0, len(attachments))

	for _, attach := range attachments {
		if attach.Type == "photo" {
			imgURL, err := getUrlOfImageWithMaxResolution(attach.Photo)
			if err != nil {
				continue
			}

			image := models.PostImage{
				Image: imgURL,
			}

			images = append(images, image)
		}
	}

	return images
}

func getUrlOfImageWithMaxResolution(vkPhoto map[string]interface{}) (string, error) {
	photoPattern := `^photo_[0-9]+`
	maxImgWidth := 0
	imgKey := ""

	for key, _ := range vkPhoto {
		matched, _ := regexp.MatchString(photoPattern, key)
		if matched {
			photoWidth, _ := strconv.Atoi(key[6:])
			if photoWidth > maxImgWidth {
				maxImgWidth = photoWidth
				imgKey = key
			}
		}
	}

	if imgKey == "" {
		return "", errors.New("image not found")
	}

	return vkPhoto[imgKey].(string), nil
}

func convertVKComment(vkComment VKComment) models.Comment {
	comment := models.Comment{
		Username: strconv.Itoa(vkComment.FromId),
		Text:     vkComment.Text,
		PostId:   0,
	}

	return comment
}
