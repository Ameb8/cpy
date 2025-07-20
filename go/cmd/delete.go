package cmd

import (
	"fmt"
	"oos"
	"github.com/ameb8/cpy/vars"
	"github.com/spf13/cobra"
)

var printResult(deleted []string, errs []error) {
	for _, deleted := range success { // LPrint successful deletions
		fmt.Println("'%s' Successfully deleted", deleted)
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
		// Hold deletion results
		success := make([]string)
		errs := make([]error)

		for _, arg := range args { // Attempt to delete all args
			deleted, err = vars.DeleteVar(arg)

			if deleted != "" { // Var deleted
				success = append(success, deleted)
			}

			if err != nil { // Deletion error
				errs = append(errs, err)
			}
		}

		printResult(success, errs) // Output results
	},
}

func init() {
	rootCmd.AddCommand(deleteCmd)
}