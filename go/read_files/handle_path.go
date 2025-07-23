package read_files

import (
	"github.com/ameb8/cpy/dev"
)

func HandlePath(path string, flags map[string][]string) (string, error) {
	files, err := loadFiles(path)

	dev.Debug("\n\n\nHandlePath() {\n")
	dev.Debug(files)

	if err != nil {
		dev.Debugf("Error getting files:\t%s\n", err)
	}

	dev.Debug("}\n\n\n")

	return "Filepath Evaluated", err
}
