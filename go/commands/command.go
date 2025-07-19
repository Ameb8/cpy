package commands

import (
	"errors"
	"strings"
)

type Command struct {
	Cmd   string
	Args  []string
	Flags map[string][]string
}

func getParams(cmd *Command, cmd_parts []string) error {
	if cmd == nil { // Ensure valid command
		return errors.New("Command Not Present")
	}

	lastFlag := ""

	for _, part := range cmd_parts {
		part = strings.TrimSpace(part)

		if strings.HasPrefix(part, "-") { // Parse flag
			lastFlag = part              // Set as last read flag
			_, ok := cmd.Flags[lastFlag] // Check if flag exists

			if !ok { // Append empty space to flag parameters
				cmd.Flags[lastFlag] = append(cmd.Flags[lastFlag], " ")
			}
		} else {
			if lastFlag == "" { // Reading command argument
				cmd.Args = append(cmd.Args, part)
			} else { // Reading flag parameter
				cmd.Flags[lastFlag] = append(cmd.Flags[lastFlag], part)
			}
		}

	}

	return nil
}

func ParseCommand(content string) (*Command, error) {
	if strings.TrimSpace(content) == "" { // Ensure valid command
		return nil, errors.New("Command not present")
	}

	cmd_parts := strings.Fields(content) // Get list of params

	cmd := &Command{ // Instantiate  Command object
		Cmd:   cmd_parts[0],
		Args:  make([]string, 0),
		Flags: make(map[string][]string),
	}

	err := getParams(cmd, cmd_parts[1:]) // Parse params

	if err != nil { // Error parsing command
		return nil, errors.New("Command could not be parse")
	}

	return cmd, nil
}
