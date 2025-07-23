package commands

import (
	"errors"
	"fmt"
	"strings"

	"github.com/ameb8/cpy/dev"
	"github.com/ameb8/cpy/read_files"
)

func applyVar(input string) (string, error) {
	result := ""

	command, err := ParseCommand(input)

	dev.Debugf("Command:\n%s\n", command.String())

	if err != nil {
		return "", err
	}

	handler, ok := CommandTable[command.Cmd]

	if !ok { // Command not in table
		// Attempt to parse as filepath
		file_content, file_err := read_files.HandlePath(command.Cmd, command.Flags)

		if file_err == nil {
			return file_content, file_err
		}

		return "", fmt.Errorf("unknown command: %s", command.Cmd)
	}

	result, cmd_err := handler(*command)

	if cmd_err != nil {
		return "", err
	}

	return result, nil
}

func ProcessCommands(input string) (string, error) {
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

				dev.Debugf("\n\n\nReplacing Command: %s\n", content)

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
