package vars

import (
	"fmt"
	"strings"

	"github.com/ameb8/cpy/dev"
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

	return fmt.Sprintf("'%s' successfully created", new_var.String()), nil
}

func GetVars(var_names []string) (string, []error) {
	dev.Debugf("\nvars.GetVars()") // *****DEBUG

	if len(var_names) == 0 { // Retrieve all vars
		return listVars()
	}

	// List of errors and valid retrievals
	var errs []error
	var valid_names []string

	for _, name := range var_names {
		valid := validate(name)

		if valid == '0' { // Name is valid
			valid_names = append(valid_names, name)
		} else { // Invalid name
			errs = append(errs, fmt.Errorf("invalid character in variable name '%s':\t%q", name, valid))
		}
	}

	if len(valid_names) == 0 { // No valid errors
		return "", errs
	}

	var vars []string

	for _, name := range valid_names { // Get named items from data
		fetched, err := getVar(name) // Attempt fetch

		if err != nil { // Record fetch errors
			errs = append(errs, err)
		}

		if fetched != "" { // Record Variable
			vars = append(vars, fetched)
		}
	}

	return strings.Join(vars, "\n"), errs
}
