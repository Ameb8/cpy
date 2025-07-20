// cmd/root.go
package cmd

import (
	"fmt"
	"os"
	"strings"

	"github.com/ameb8/cpy/copy"
	"github.com/spf13/cobra"
)

var (
	appendFlag bool
	outFlag    bool
)

var rootCmd = &cobra.Command{
	Use:   "cpy [clip_content...]",
	Short: "Clipboard manager",
	Args:  cobra.ArbitraryArgs,
	RunE: func(cmd *cobra.Command, args []string) error {
		content := strings.Join(args, " ")
		copy.CopyContent(content, appendFlag, outFlag)

		return nil
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}
}

func init() {
	rootCmd.Flags().BoolVar(&appendFlag, "append", false, "Append instead of replacing clipboard")
	rootCmd.Flags().BoolVar(&outFlag, "out", false, "Print clipboard content")
}
