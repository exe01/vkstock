package utils

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"strings"
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
	secondsInDays := int64(time.Hour.Seconds()*24) * days
	return time.Now().Unix() - secondsInDays
}

func DifInMinutesFromNowUnix(to int64) int64 {
	now := time.Now().Unix()
	return DifInMinutesUnix(now, to)
}

func DifInMinutesUnix(from, to int64) int64 {
	difInSec := from - to
	return difInSec / 60
}

func DownloadImage(url string) (io.ReadCloser, string, error) {
	resp, err := http.Get(url)
	if err != nil {
		return resp.Body, "", err
	}

	format, err := DefineFormatFromHeader(resp.Header)
	if err != nil {
		return resp.Body, "", err
	}

	return resp.Body, format, nil
}

func DefineFormatFromHeader(header http.Header) (string, error) {
	mimeType := header.Get("Content-Type")
	typeAndFormat := strings.Split(mimeType, "/")
	if len(typeAndFormat) < 2 {
		return "", errors.New("format of image is undefined")
	}

	format := typeAndFormat[1]

	return format, nil
}

func GenerateRandomString(postfix string) string {
	str := strconv.Itoa(rand.Int())
	str += postfix
	return str
}

func PrettyJson(msg []byte) string {
	var prettyJSON bytes.Buffer
	err := json.Indent(&prettyJSON, msg, "", "\t")
	if err != nil {
		log.Println("JSON parse error: ", err)
		return ""
	}

	return prettyJSON.String()
}

func ParseUsernameAndPassFromToken(token string) (string, string, error) {
	usernameAndPass := strings.Split(token, "|")
	if len(usernameAndPass) != 2 {
		errorMsg := fmt.Sprintf("incorrect token, count of elements %d", len(usernameAndPass))
		return "", "", errors.New(errorMsg)
	}

	return usernameAndPass[0], usernameAndPass[1], nil
}
