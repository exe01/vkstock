package utils

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

func GetFileSizeMB(path string) (int, error) {
	file, err := os.Open(path)
	defer file.Close()

	if err != nil {
		return 0, err
	}
	fileInfo, err := file.Stat()
	if err != nil {
		return 0, err
	}

	size := fileInfo.Size()
	return int(size / 1048576), nil
}

func ParseResponseBody(resp *http.Response, v interface{}) error {
	bodyBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	err = json.Unmarshal(bodyBytes, v)
	if err != nil {
		return err
	}

	return err
}

func NowMinusDaysUnix(days int64) int64 {
	secondsInDays := int64(time.Hour.Seconds() * 24) * days
	return time.Now().Unix() - secondsInDays
}
