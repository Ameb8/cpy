package commands

import (
	"fmt"
	"time"
)

type CommandHandler func(cmd Command) (string, error)

var CommandTable = map[string]CommandHandler{
	"now": handleNow,
	//"var": handleVar,
}

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
