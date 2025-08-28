package cmd

import (
	"fmt"
	"os"

	"github.com/ameb8/cpy/vars"
	"github.com/spf13/cobra"
)

func printResult(success []string, errs []error) {
	for _, deleted := range success { // LPrint successful deletions
		fmt.Printf("'%s' Successfully deleted", deleted)
	}

	if len(errs) != 0 { // Display errors
		fmt.Println("Errors deleting variables:")

		for _, err := range errs { // Print individual error
			fmt.Fprintln(os.Stderr, err)
		}
	}
}

var deleteCmd = &cobra.Command{
	Use:   "delete <variable name> <variable name> ...",
	Short: "Delete variable(s) by providing name",
	Args:  cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		success, errs := vars.DeleteVars(args) // Attempt deletions
		printResult(success, errs)             // Output results
	},
}

func init() {
	rootCmd.AddCommand(deleteCmd)
}
