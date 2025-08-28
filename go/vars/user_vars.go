package vars

import (
	"fmt"
	"regexp"
	"strings"
	"unicode"

	"github.com/ameb8/cpy/dev"
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
		return fmt.Errorf("Invalid character in variable name '%s':\t%q", user_var.Name, name_err)
	}

	for _, param := range user_var.Params {
		param_err := validate(param)

		if param_err != '0' {
			return fmt.Errorf("Invalid character in parameter '%s':\t%q", param, param_err)
		}
	}

	return nil
}

func applyParams(user_var *Entry, args []string) (string, error) {
	dev.Debugf("\n\n\napplyParams() { \n")

	re := regexp.MustCompile(`<<.*?>>`)

	// Find all parameters
	params := re.FindAllString(user_var.UserVar, -1)
	if len(params) != len(args) {
		dev.Debugf("Error: params found = %d, args passed = %d\n\n\n", len(params), len(args))

		return "", fmt.Errorf("mismatch: found %d params but got %d args", len(params), len(args))
	}

	// Apply arguments
	i := 0
	result := re.ReplaceAllStringFunc(user_var.UserVar, func(_ string) string {
		repl := args[i]
		i++
		return repl
	})

	return result, nil
}
