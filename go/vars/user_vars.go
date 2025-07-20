package vars

import (
	"fmt"
	"strings"
	"unicode"
)

type Entry struct {
	Name    string
	UserVar string
	Params  []string
}

func (e Entry) String() string {
	return fmt.Sprintf("%s(%s): %s", e.Name, strings.Join(e.Params, ", "), e.UserVar)
}

func validate(str string) rune {
	for _, r := range str {
		if !(unicode.IsLetter(r) || unicode.IsDigit(r) || r == '_') {
			return r
		}
	}

	return '0'
}

func validateVar(user_var *Entry) error {
	name_err := validate(user_var.Name)

	if name_err != '0' {
		return fmt.Errorf("Invalid character in variable name '%s':\t%r", user_var.Name, name_err)
	}

	for _, param := range user_var.Params {
		param_err := validate(param)

		if param_err != '0' {
			return fmt.Errorf("Invalid character in parameter '%s':\t%r", param, param_err)
		}
	}

	return nil
}
