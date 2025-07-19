package cpy

import (
	"fmt"
	"os"
	"strings"

	"github.com/spf13/cobra"
)

func main() {
	var appendFlag bool
	var outFlag bool
	var getFlag []string
	var setFlag []string
	var listFlag bool
	var deleteFlag []string

	var rootCmd = &cobra.Command{
		Use:   "cpy [clip_content...]",
		Short: "Clipboard management CLI",
		Args:  cobra.ArbitraryArgs,
		RunE: func(cmd *cobra.Command, args []string) error {
			clipContent := strings.Join(args, " ")

			if appendFlag {
				fmt.Println("Appending:", clipContent)

			} else if outFlag {
				fmt.Println("Output:", clipContent)

			} else if len(getFlag) == 1 {
				fmt.Println("Get key:", getFlag[0])

			} else if len(setFlag) == 2 {
				fmt.Println("Set key:", setFlag[0], "Value:", setFlag[1])

			} else if listFlag {
				fmt.Println("Listing keys")

			} else if len(deleteFlag) == 1 {
				fmt.Println("Delete key:", deleteFlag[0])

			} else if clipContent != "" {
				fmt.Println("Copying to clipboard:", clipContent)

			} else {
				return fmt.Errorf("no valid flags or content provided")
			}
			return nil
		},
	}

	rootCmd.Flags().BoolVar(&appendFlag, "append", false, "Append to clipboard")
	rootCmd.Flags().BoolVar(&outFlag, "out", false, "Print clipboard content")
	rootCmd.Flags().StringSliceVar(&getFlag, "get", nil, "Get key (1 argument)")
	rootCmd.Flags().StringSliceVar(&setFlag, "set", nil, "Set key value (2 arguments)")
	rootCmd.Flags().BoolVar(&listFlag, "list", false, "List all keys")
	rootCmd.Flags().StringSliceVar(&deleteFlag, "delete", nil, "Delete key (1 argument)")

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
