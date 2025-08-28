package config

import (
	"github.com/spf13/viper"
)

func Init() {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")
	viper.ReadInConfig()
}

func GetExcludeTree() []string {
	return viper.GetStringSlice("exclude_tree")
}
