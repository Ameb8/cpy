package dev

import (
	"fmt"
	"log"
	"os"
)

var enabled bool

func init() {
	enabled = os.Getenv("DEBUG") == "1"
	if enabled {
		log.SetFlags(log.LstdFlags | log.Lshortfile)
		log.SetPrefix("DEBUG: ")
	}
}

func Debugf(format string, args ...any) {
	if enabled {
		log.Output(2, fmt.Sprintf(format, args...))
	}
}

func Enabled() bool {
	return enabled
}

func Debugln(args ...any) {
	if enabled {
		log.Output(2, fmt.Sprintln(args...))
	}
}

func Debug(args ...any) {
	if enabled {
		log.Output(2, fmt.Sprint(args...))
	}
}
