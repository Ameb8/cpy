package commands

import (
	"errors"
	"fmt"
	"sort"
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
		return nil, errors.New("Command could not be parsed")
	}

	return cmd, nil
}

func (c Command) String() string {
	var b strings.Builder

	b.WriteString("Command Debug Info:\n")

	// Write the command name
	b.WriteString(fmt.Sprintf("  Cmd: %q\n", c.Cmd))

	// Write arguments
	if len(c.Args) > 0 {
		b.WriteString("  Args:\n")
		for i, arg := range c.Args {
			b.WriteString(fmt.Sprintf("    [%d]: %q\n", i, arg))
		}
	} else {
		b.WriteString("  Args: (none)\n")
	}

	// Write flags
	if len(c.Flags) > 0 {
		b.WriteString("  Flags:\n")

		keys := make([]string, 0, len(c.Flags))
		for k := range c.Flags {
			keys = append(keys, k)
		}
		sort.Strings(keys)

		for _, k := range keys {
			b.WriteString(fmt.Sprintf("    %q:\n", k))
			vals := c.Flags[k]
			for i, v := range vals {
				b.WriteString(fmt.Sprintf("      [%d]: %q\n", i, v))
			}
		}
	} else {
		b.WriteString("  Flags: (none)\n")
	}

	return b.String()
}
