package copy

import (
	"fmt"
	"os"
	"strings"

	"github.com/ameb8/cpy/commands"
	"github.com/atotto/clipboard"
)

func applyEscapeChars(content string) string {
	content = strings.ReplaceAll(content, `\n`, "\n")
	content = strings.ReplaceAll(content, `\t`, "\t")
	content = strings.ReplaceAll(content, `\a`, "\a")
	content = strings.ReplaceAll(content, `\r`, "\r")

	return content
}

func CopyContent(content string, append bool, print bool) {
	result, err := commands.ProcessCommands(content)

	if err != nil { // Error processing commands
		fmt.Fprintln(os.Stderr, err)
	}

	result = applyEscapeChars(result)

	if append { // Append new text to current clipboard content
		content, read_err := clipboard.ReadAll()

		if read_err != nil { // Error getting clipboard content
			fmt.Fprintln(os.Stderr, read_err)
		} else { // Append clipboard content
			result = content + result
		}
	}

	clip_err := clipboard.WriteAll(result) // Attempt write to clipboard

	if clip_err != nil { // Error writing to clipboard
		fmt.Fprintln(os.Stderr, clip_err)
	}

	if print { // Print result
		fmt.Println(result)
	}
}
