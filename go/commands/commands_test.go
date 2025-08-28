package commands

import (
	"reflect"
	"testing"
)

func TestParseCmd(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  Command
	}{
		{
			name:  "No Parameters",
			input: "cmd",
			want: Command{
				Cmd:   "cmd",
				Args:  []string{},
				Flags: map[string][]string{},
			},
		},
		{
			name:  "Multiple Arguments",
			input: "cmd arg1 arg2 arg3",
			want: Command{
				Cmd:   "cmd",
				Args:  []string{"arg1", "arg2", "arg3"},
				Flags: map[string][]string{},
			},
		},
		{
			name:  "Multiple Flags with Params",
			input: "cmd --flg1 arg1.1 arg1.2 --flg2 --flag3 arg3.1",
			want: Command{
				Cmd:  "cmd",
				Args: []string{},
				Flags: map[string][]string{
					"--flg1":  {" ", "arg1.1", "arg1.2"},
					"--flg2":  {" "},
					"--flag3": {" ", "arg3.1"},
				},
			},
		},
		{
			name:  "Multiple Arguments and Flags with Params",
			input: "cmd main_arg1 main_arg2 --flg1 arg1.1 arg1.2 --flg2 --flag3 arg3.1",
			want: Command{
				Cmd:  "cmd",
				Args: []string{"main_arg1", "main_arg2"},
				Flags: map[string][]string{
					"--flg1":  {" ", "arg1.1", "arg1.2"},
					"--flg2":  {" "},
					"--flag3": {" ", "arg3.1"},
				},
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ParseCommand(tt.input)
			if err != nil {
				t.Fatalf("ParseCommand() error = %v", err)
			}
			if !reflect.DeepEqual(*got, tt.want) {
				t.Errorf("ParseCommand() = %+v, want %+v", *got, tt.want)
			}
		})
	}

}
