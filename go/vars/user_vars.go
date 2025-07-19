package vars

import (
	"fmt"
	"strings"
)

type Entry struct {
	Name    string
	UserVar string
	Params  []string
}

func (e Entry) String() string {
	return fmt.Sprintf("%s(%s): %s", e.Name, strings.Join(e.Params, ", "), e.UserVar)
}
