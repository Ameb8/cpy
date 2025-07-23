package commands

import (
	"fmt"
	"time"

	"github.com/ameb8/cpy/dev"
	"github.com/ameb8/cpy/vars"
)

type CommandHandler func(cmd Command) (string, error)

var CommandTable = map[string]CommandHandler{}

func handleNow(cmd Command) (string, error) {
	format := "rfc3339" // Default format
	if val, ok := cmd.Flags["format"]; ok && len(val) > 0 {
		format = val[0]
	}

	location := time.Local // Default to local time
	if val, ok := cmd.Flags["timezone"]; ok && len(val) > 0 {
		tz := val[0]
		loc, err := time.LoadLocation(tz)

		if err != nil {
			return "", fmt.Errorf("invalid timezone: %s", tz)
		}

		location = loc
	}

	now := time.Now().In(location)

	var output string

	// Set output format
	switch format {
	case "unix":
		output = fmt.Sprintf("%d", now.Unix())
	case "unixMilli":
		output = fmt.Sprintf("%d", now.UnixMilli())
	case "unixNano":
		output = fmt.Sprintf("%d", now.UnixNano())
	case "rfc3339":
		output = now.Format(time.RFC3339)
	case "rfc3339nano":
		output = now.Format(time.RFC3339Nano)
	case "rfc822":
		output = now.Format(time.RFC822)
	case "rfc850":
		output = now.Format(time.RFC850)
	case "rfc1123":
		output = now.Format(time.RFC1123)
	case "rfc1123z":
		output = now.Format(time.RFC1123Z)
	case "kitchen":
		output = now.Format(time.Kitchen)
	case "stamp":
		output = now.Format(time.Stamp)
	case "stampmilli":
		output = now.Format(time.StampMilli)
	case "stampmicro":
		output = now.Format(time.StampMicro)
	case "stampnano":
		output = now.Format(time.StampNano)
	default:
		return "", fmt.Errorf("unsupported format: %s", format)
	}

	return output, nil
}

func handleVar(cmd Command) (string, error) {
	user_var, err := vars.UseVar(cmd.Args[0], cmd.Args[1:]) // Replace command with var

	dev.Debugf("\ncommands.handleVar():\n%s\n", user_var)

	if err != nil { // Error applying var
		return "", err
	}

	swap, rec_err := ProcessCommands(user_var) // Recursively process var content

	if rec_err != nil { // Error processing
		return "", rec_err
	}

	return swap, nil
}

func init() { // Initialize Command handler functions
	CommandTable["now"] = handleNow
	CommandTable["var"] = handleVar
}
