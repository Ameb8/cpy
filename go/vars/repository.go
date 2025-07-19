package vars

import (
	"encoding/gob"
	"fmt"
	"os"
	"sort"
	"strings"
)

const varData = "user_vars.gob"

func loadData() (map[string]Entry, error) {
	file, err := os.Open(varData) // Open file

	if err != nil {
		if os.IsNotExist(err) { // No variables found
			return make(map[string]Entry), nil // return empty if file not found
		}

		return nil, err // Error opening file
	}

	defer file.Close() // Close file

	// Convert file data to map
	var data map[string]Entry
	dec := gob.NewDecoder(file)
	err = dec.Decode(&data)

	return data, err
}

func saveData(data map[string]Entry) error {
	file, err := os.Create(varData) // Create file

	if err != nil { // Error creating file
		return err
	}

	defer file.Close() // Close file

	enc := gob.NewEncoder(file) // Encode data

	return enc.Encode(data)
}

func setVar(name, userVar string, params []string) error {
	data, err := loadData()

	if err != nil { // Error loading data
		return err
	}

	// Update variables
	data[name] = Entry{Name: name, UserVar: userVar, Params: params}
	return saveData(data)
}

func getVar(name string) (*Entry, error) {
	data, err := loadData()

	if err != nil { // Error loading data
		return nil, err
	}

	entry, ok := data[name] // Search for variable

	if !ok { // Variable not found
		return nil, fmt.Errorf("entry '%s' not found", name)
	}

	return &entry, nil
}

func deleteVar(name string) (string, error) {
	data, err := loadData()

	if err != nil { // Error loading data
		return "", err
	}

	if _, ok := data[name]; !ok { // Entry not found
		return "", fmt.Errorf("entry '%s' does not exist", name)
	}

	// Update stored variables
	delete(data, name)
	saveResult := saveData(data)

	if saveResult != nil { // Error updating variables
		return "", saveResult
	}

	return fmt.Sprintf("Variable '%s' successfully deleted", name), nil
}

func listVars() (string, error) {
	data, err := loadData()

	if err != nil { // Error loading data
		return "", err
	}

	if len(data) == 0 { // No variables
		return "No variables have been defined", nil
	}

	// Create slice of variable names
	keys := make([]string, 0, len(data))
	for k := range data {
		keys = append(keys, k)
	}

	sort.Strings(keys) // Sort variables by name

	// Create string of all variables
	var b strings.Builder
	for _, k := range keys {
		b.WriteString(data[k].String())
		b.WriteString("\n")
	}

	return b.String(), nil
}
