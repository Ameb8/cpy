package commands

import (
	"errors"
	"strings"
)

func applyVar(input string) (string, error) {
	result := ""

	command, err := ParseCommand(input)

	if err != nil {
		return "", errors.New("Command could not be parsed")
	}

	return result, nil
}

func replaceBrackets(input string) (string, error) {
	var result strings.Builder
	i := 0
	for i < len(input) {
		if i+1 < len(input) && input[i] == '[' && input[i+1] == '[' {
			end := i + 2
			for end+1 < len(input) {
				if input[end] == ']' && input[end+1] == ']' {
					break
				}
				end++
			}
			if end+1 < len(input) && input[end] == ']' && input[end+1] == ']' {
				content := input[i+2 : end]
				resolvedVar, err := applyVar(content)

				if err != nil {
					return "", errors.New("Command could not be parsed")
				}
				result.WriteString(resolvedVar)
				i = end + 2
				continue
			}
		}
		result.WriteByte(input[i])
		i++
	}
	return result.String(), nil
}
