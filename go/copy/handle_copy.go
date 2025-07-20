package copy

import (
	"fmt"
)

func CopyContent(content string, append bool, print bool) {
	if print {
		fmt.Println(content)
	}
}
