package dev

import (
	"fmt"
	"log"
	"os"
	"runtime"
	"runtime/debug"
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

func PrintStack() {
	if enabled {
		log.Output(2, string(debug.Stack()))
	}
}

func Here() {
	if enabled {
		_, file, line, ok := runtime.Caller(1)
		if ok {
			log.Output(2, fmt.Sprintf("HERE: %s:%d", file, line))
		}
	}
}

func Trace() {
	if !enabled {
		return
	}
	for i := 1; ; i++ {
		pc, file, line, ok := runtime.Caller(i)
		if !ok {
			break
		}
		fn := runtime.FuncForPC(pc)
		log.Output(2, fmt.Sprintf("%s:%d - %s", file, line, fn.Name()))
	}
}

func DebugInfo() {
	PrintStack()
	Here()
	Trace()
}
