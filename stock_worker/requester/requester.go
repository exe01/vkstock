package requester

import (
	"io"
	"net/http"
	"strings"
)

type VKRequester struct {
	VKURL string
	Client *http.Client

	accessToken string
	version     string
}

func NewVKRequester(accessToken string, version string) *VKRequester {
	vkURL := "https://api.vk.com"

	vkRequester := &VKRequester{
		vkURL,
		&http.Client{},
		accessToken,
		version,
	}

	return vkRequester
}

func (r *VKRequester) CreateVKRequest(method, action string, params map[string]string, body io.Reader) (*http.Request, error) {
	if !strings.HasPrefix(action, "/") {
		action = "/" + action
	}

	req, err := http.NewRequest(method, r.VKURL+action, body)
	if err != nil {
		return nil, err
	}

	// All request to VKApi must contain 2 parameters:
	// v - version;
	// access_token - authorization token;
	query := req.URL.Query()
	query.Add("v", r.version)
	query.Add("access_token", r.accessToken)

	if params != nil {
		for key, value := range params {
			query.Add(key, value)
		}
	}

	req.URL.RawQuery = query.Encode()

	return req, nil
}
