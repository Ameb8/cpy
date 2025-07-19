package commands

import (
	"testing"
	"reflect"
)

func TestParseCmd(t *testing.T) {
	tests := []struct {
		name string
		want Command

	} {
		{
			name: "No Parameters"
			input: "cmd"
			want: Command{
				Cmd: "cmd",
				Args: []string{},
				Flags: map[string][]string{}
			}
		}
		{
			name: "No Parameters"
			input: "cmd arg1 arg2 arg3"
			want: Command{
				Cmd: "cmd",
				Args: []string{{"arg1", "arg2", "arg3"},
				Flags: map[string][]string},
			}
		}

	}

	
}