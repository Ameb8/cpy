package read_files

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"

	"github.com/ameb8/cpy/dev"
	"github.com/spf13/viper"
	"github.com/xlab/treeprint"
)

type include struct {
	includeExts      map[string]struct{}
	excludeDirs      map[string]struct{}
	excludeFileGlobs []string
	maxDepth         int
}

func getMap(slice []string) map[string]struct{} {
	set := make(map[string]struct{}, len(slice)) // preallocate map with capacity

	for _, s := range slice {
		set[s] = struct{}{}
	}

	return set
}

func parseDepth(flags map[string][]string) int {
	// Get depth flag args
	if depthVals, ok := flags["--depth"]; ok && len(depthVals) > 0 {
		val, err := strconv.Atoi(depthVals[0])

		// Valid positive integer param
		if err == nil && val > 0 {
			return val
		}
	}

	return 0
}

/*
func getExcluded(flags map[string][]string) map[string]struct{} {
	exclude := make(map[string]struct{})

	// Add excludes from config settings
	for _, exc := range viper.GetStringSlice("tree_exclude") {
		exclude[exc] = struct{}{}
	}

	// Add exclude arguments
	for _, exc := range flags["--exclude"] {
		exclude[exc] = struct{}{}
	}

	return exclude

}
*/

func getInclude(flags map[string][]string) *include {
	// DEBUG *****
	dev.Debug("\n\n\n\nEXCLUDE:\n\n")
	dev.Debug(viper.GetStringSlice("exclude_dirs"))

	return &include{
		includeExts:      getMap(flags["--include"]),
		excludeDirs:      getMap(viper.GetStringSlice("exclude_dirs")),
		excludeFileGlobs: viper.GetStringSlice("exclude_files"),
		maxDepth:         parseDepth(flags),
	}
}

func (inc *include) excludeFile(path string, depth int) bool {
	if depth >= inc.maxDepth {
		return false // Depth too great, exclude file
	}

	base := filepath.Base(path)

	for _, pattern := range inc.excludeFileGlobs {
		match, _ := filepath.Match(pattern, base)

		if match {
			return true
		}
	}

	if len(inc.includeExts) == 0 {
		return false
	}

	_, include := inc.includeExts[filepath.Ext(path)]

	return !include
}

func (inc *include) excludeDir(path string, depth int) bool {
	if depth >= inc.maxDepth {
		return false // Too deep, exclude
	}

	for dir, _ := range inc.excludeDirs {
		if strings.Contains(path, dir) {
			return true
		}
	}

	return false
}

/*
func (inc *include) includeFile(path string, depth int) bool {
	if inc.maxDepth > 0 && depth > inc.maxDepth {
		return false // Too deep
	}

	//Segment filepath
	ext := filepath.Ext(path)
	base := filepath.Base(path)

	// excluded base path
	if _, ok := inc.exclude[base]; ok {
		return false
	}

	if ext != "" {
		_, ok := inc.include[ext]

		// Do not include file
		if !ok && len(inc.include) > 0 {
			return false
		}
	}

	_, ok := inc.exclude[ext]

	if ok { // Do not include file
		return false
	}

	return inc.maxDepth <= depth
}
*/

func GetTree(inputPath string, flags map[string][]string) (string, error) {
	// Convert input to absolute path
	rootPath, err := filepath.Abs(inputPath)

	if err != nil { // Error converting path
		return "", fmt.Errorf("failed to resolve path: %w", err)
	}

	info, err := os.Stat(rootPath) // Get file info

	if err != nil { // Error getting info
		return "", fmt.Errorf("invalid path: %w", err)
	}

	include := getInclude(flags)

	// Create tree
	tree := treeprint.New()
	tree.SetValue(info.Name())
	err = walkDir(rootPath, tree, include, 1)

	if err != nil { // Error creating tree
		return "", err
	}

	return tree.String(), nil
}

func walkDir(path string, node treeprint.Tree, inc *include, depth int) error {
	entries, err := os.ReadDir(path) // Read directory contents

	if err != nil { // Read error
		return err
	}

	sort.Slice(entries, func(i, j int) bool { // Sort contents alphabetically
		return entries[i].Name() < entries[j].Name()
	})

	for _, entry := range entries { // Iterate entries
		entryName := entry.Name()
		entryPath := filepath.Join(path, entryName)

		if entry.IsDir() { // Entry is directory
			if inc.excludeDir(entryName, depth) {
				continue
			}

			//if _, skip := inc.excludeDirs[entryName]; skip {
			//	continue // Exclude directory
			//}

			// Add branch for directory
			branch := node.AddBranch(entryName)
			err := walkDir(entryPath, branch, inc, depth+1)

			if err != nil { // Error adding branch
				return err
			}

		} else if !inc.excludeFile(entryPath, depth) {
			node.AddNode(entryName) // Add file
		}
	}

	return nil
}
