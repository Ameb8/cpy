package main

import (
	"github.com/ameb8/cpy/cmd"
	"github.com/ameb8/cpy/dev"
)

func main() {
	dev.Debug("Debug Mode Enabled\n")
	cmd.Execute()
}
