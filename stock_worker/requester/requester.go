package requester

import (
	"io"
	"net/http"
	"strings"
)

type VKRequester struct {
	VKURL  string
	Client *http.Client

	serviceToken string
	userToken    string
	version      string
}

func NewVKRequester(serviceToken, userToken string, version string) *VKRequester {
	vkURL := "https://api.vk.com"

	vkRequester := &VKRequester{
		vkURL,
		&http.Client{},
		serviceToken,
		userToken,
		version,
	}

	return vkRequester
}

func (r *VKRequester) CreateVKRequest(method, action string, params map[string]string, body io.Reader) (*http.Request, error) {
	params["access_token"] = r.serviceToken
	return r.createVKRequest(method, action, params, body)
}

func (r *VKRequester) CreatePrivilegedVKRequest(method, action string, params map[string]string, body io.Reader) (*http.Request, error) {
	params["access_token"] = r.userToken
	return r.createVKRequest(method, action, params, body)
}

func (r *VKRequester) createVKRequest(method, action string, params map[string]string, body io.Reader) (*http.Request, error) {
	if !strings.HasPrefix(action, "/") {
		action = "/" + action
	}

	req, err := http.NewRequest(method, r.VKURL+action, body)
	if err != nil {
		return nil, err
	}

	if _, ok := params["v"]; !ok {
		params["v"] = r.version
	}

	query := req.URL.Query()
	if params != nil {
		for key, value := range params {
			query.Add(key, value)
		}
	}

	req.URL.RawQuery = query.Encode()

	return req, nil
}
