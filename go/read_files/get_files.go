package read_files

import (
	"io/fs"
	"os"
	"path/filepath"
	"unicode/utf8"

	"github.com/bmatcuk/doublestar/v4"
)

func getAbsPath(relativePath string) (string, error) {
	cwd, err := os.Getwd() // Get cwd

	if err != nil { // Error getting cwd
		return "", err
	}

	// Join and clean filepath
	absPath := filepath.Join(cwd, relativePath)
	absPath = filepath.Clean(absPath)

	// Make path relative to root
	relToRoot, err := filepath.Rel("/", absPath)
	if err != nil {
		return "", err
	}

	return relToRoot, nil
}

func loadFiles(relativePath string) (map[string]string, error) {
	absPath, err := getAbsPath(relativePath) // Convert relative path to absolute

	if err != nil { // Error getting absolute path
		return nil, err
	}

	matches, err := doublestar.Glob(os.DirFS("/"), absPath)

	if err != nil { // Error evaluating filepath
		return nil, err
	}

	if len(matches) == 0 { // No matches
		return nil, nil
	}

	result := make(map[string]string)

	for _, match := range matches {
		content, err := readTextFile("/" + match)

		if err != nil { // skip unreadable or binary files
			continue
		}

		result[filepath.Clean(match)] = content
	}

	if len(result) == 0 { // No results read
		return nil, nil
	}

	return result, nil
}

func readTextFile(path string) (string, error) {
	data, err := os.ReadFile(path)

	if err != nil { // Error reading file
		return "", err
	}

	if !isProbablyText(data) { // Detect invalid format
		return "", fs.ErrInvalid
	}

	return string(data), nil
}

func isProbablyText(data []byte) bool {
	if !utf8.Valid(data) { // Invalid format
		return false
	}
	for _, b := range data { // control characters except for newline, tab, etc.
		if b < 0x09 || (b > 0x0D && b < 0x20) {
			return false
		}
	}
	return true
}
