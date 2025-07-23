package read_files

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strconv"

	"github.com/xlab/treeprint"
)

type include struct {
	include  map[string]struct{}
	exclude  map[string]struct{}
	maxDepth int
	emptyDir bool
}

func getMap(slice []string) map[string]struct{} {
	set := make(map[string]struct{}, len(slice)) // preallocate map with capacity
	for _, s := range slice {
		set[s] = struct{}{} // empty struct{} takes zero bytes
	}
	return set
}

func parseDepth(flags map[string][]string) int {
	// Get depth flag args
	if depthVals, ok := flags["--depth"]; ok && len(depthVals) > 0 {
		val, err := strconv.Atoi(depthVals[0])

		// Valid positive integer
		if err == nil && val > 0 {
			return val
		}
	}

	return 0
}

func getInclude(flags map[string][]string) *include {
	return &include{
		include:  getMap(flags["--include"]),
		exclude:  getMap(flags["--exclude"]),
		maxDepth: parseDepth(flags),
	}
}

func (inc *include) includeFile(path string, depth int) bool {
	ext := filepath.Ext(path)

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
	err = walkDir(rootPath, tree)

	if err != nil { // Error creating tree
		return "", err
	}

	return tree.String(), nil
}

func walkDir(path string, node treeprint.Tree) error {
	entries, err := os.ReadDir(path) // Read directory contents

	if err != nil { // Read error
		return err
	}

	sort.Slice(entries, func(i, j int) bool { // Sort contents alphabetically
		return entries[i].Name() < entries[j].Name()
	})

	for _, entry := range entries { // Iterate entries
		entryPath := filepath.Join(path, entry.Name())

		if entry.IsDir() { // Entry is directory
			branch := node.AddBranch(entry.Name()) // Add branch

			// Add branch to tree
			if err := walkDir(entryPath, branch); err != nil {
				return err // Error adding branch
			}

		} else { // Add file to tree
			node.AddNode(entry.Name())
		}
	}

	return nil
}
