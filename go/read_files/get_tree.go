package read_files

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"

	"github.com/xlab/treeprint"
)

func GetTree(inputPath string) (string, error) {
	// Convert input to absolute path
	rootPath, err := filepath.Abs(inputPath)

	if err != nil { // Error converting path
		return "", fmt.Errorf("failed to resolve path: %w", err)
	}

	info, err := os.Stat(rootPath) // Get file info

	if err != nil {
		return "", fmt.Errorf("invalid path: %w", err)
	}

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

	for _, entry := range entries { // Iterate entried
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
