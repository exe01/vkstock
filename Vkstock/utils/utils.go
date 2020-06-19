package utils

import "os"

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
