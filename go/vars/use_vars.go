package vars

import (
	"strings"
)

func DeleteVars(names []string) ([]string, []error) {
	// Hold deletion results
	success := make([]string, 0)
	errs := make([]error, 0)

	for _, name := range names { // Attempt to delete all args
		deleted, err := deleteVar(name)

		if deleted != "" { // Var deleted
			success = append(success, deleted)
		}

		if err != nil { // Deletion error
			errs = append(errs, err)
		}
	}

	return success, errs
}

func SetVar(key string, value []string, params []string) (string, error) {
	new_var := &Entry{
		Name:    key,
		UserVar: strings.Join(value, " "),
		Params:  params,
	}

	var_err := validateVar(new_var)

	if var_err != nil {
		return "", var_err
	}

	set_err := setVar(new_var)

	if set_err != nil {
		return "", set_err
	}

}
