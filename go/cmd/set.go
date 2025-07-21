package cmd

import (
	"fmt"
	"os"

	"github.com/ameb8/cpy/dev"
	"github.com/ameb8/cpy/vars"
	"github.com/spf13/cobra"
)

var (
	params []string
)

var setCmd = &cobra.Command{
	Use:   "set param=value... [content...]",
	Short: "Set a variable with given parameters and content",
	Args:  cobra.MinimumNArgs(2),
	Run: func(cmd *cobra.Command, args []string) {
		dev.Debugf("\ncmd.setCmd()") // ***** DEBUG

		result, err := vars.SetVar(args[0], args[1:], params)

		if err != nil {
			fmt.Fprintln(os.Stderr, err)
		}

		if result != "" {
			fmt.Println(result)
		}
	},
}

func init() {
	setCmd.Flags().StringSliceVar(&params, "param", []string{}, "Space separated list of parameters for variable")
	rootCmd.AddCommand(setCmd)
}
