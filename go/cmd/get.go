package cmd

import (
	"fmt"
	"os"

	"github.com/ameb8/cpy/dev"
	"github.com/ameb8/cpy/vars"
	"github.com/spf13/cobra"
)

func printGetResult(vars string, errs []error) {
	if vars != "" {
		fmt.Println(vars)
	}

	if len(errs) != 0 { // Display errors
		fmt.Println("Errors Fetching variables:")

		for _, err := range errs { // Print individual error
			fmt.Fprintln(os.Stderr, err)
		}
	}
}

var getCmd = &cobra.Command{
	Use:   "get <variable name> <variable name> ... OR Get",
	Short: "Get variable(s) by providing name(s) (all if no names provided)",
	Args:  cobra.ArbitraryArgs,
	Run: func(cmd *cobra.Command, args []string) {
		dev.Debugf("\ncmd.getCmd()") // ***** DEBUG

		vars, errs := vars.GetVars(args) // Attempt deletions
		printGetResult(vars, errs)       // Output results
	},
}

func init() {
	rootCmd.AddCommand(getCmd)
}
