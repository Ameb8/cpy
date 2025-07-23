package read_files

import (
	"strings"
)

func inMap(collection map[string][]string, key string) bool {
	_, ok := collection[key] // Check map keys

	return ok
}

func getLabels(flags map[string][]string) (bool, bool) {
	// Add label to content
	path := inMap(flags, "--path")
	name := inMap(flags, "--name")

	return path, name
}

func getDelimiter(flags map[string][]string) string {
	delimiter, ok := flags["--split"]

	if !ok { // default delimiter
		return "\n\n"
	}

	return strings.Join(delimiter, " ")
}
func HandlePath(path string, flags map[string][]string) (string, error) {
	files, err := loadFiles(path) // Load files

	// Add labels
	pathLbl, nameLbl := getLabels(flags)
	appendLabels(files, pathLbl, nameLbl)

	// Join file content
	delimiter := getDelimiter(flags)
	result := formatFiles(files, delimiter)

	return result, err
}
