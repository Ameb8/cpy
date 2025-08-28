package read_files

import (
	"strings"
)

func getName(path string) string {
	// Replace backslashes with forward slashes
	path = strings.ReplaceAll(path, "\\", "/")

	// Find the last slash
	index := strings.LastIndex(path, "/")

	// No slashes found, return whole string
	if index == -1 {
		return path
	}

	// Return the substring after the last slash
	return path[index+1:]
}

func appendLabels(files map[string]string, path bool, name bool) {
	if !path && !name { // No labels required
		return
	}

	for path_key, content := range files { // Add labels
		var header []string

		if path { // Add filepath to label
			header = append(header, path_key)
		}

		if name { // Add filename to label
			header = append(header, getName(path_key))
		}

		// Add label to file map
		full_header := strings.Join(header, "/n")
		files[path_key] = full_header + "\n\n" + content
	}
}

func formatFiles(files map[string]string, delimiter string) string {
	var fmt_files []string

	for _, file := range files { // Create slice of file content
		fmt_files = append(fmt_files, file)
	}

	return strings.Join(fmt_files, delimiter) // Join contents by delimiter
}
