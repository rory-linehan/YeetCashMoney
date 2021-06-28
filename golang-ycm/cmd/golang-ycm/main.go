package main

import (
	"flag"
	log "github.com/sirupsen/logrus"
	"golang-ycm/internal/activities"
	"golang-ycm/internal/config"
	"os"
)

func main() {
	var configFile string
	flag.StringVar(&configFile, "configFile", "config.yaml", "where is the config file located?")
	flag.Parse()

	log.SetFormatter(&log.JSONFormatter{})
	contextLogger := log.WithFields(log.Fields{"function": "main"})

	for {
		handle, err := os.Open(configFile)
		if err != nil {
			contextLogger.Fatal("failed to open file handle: ", err.Error())
		}
		conf, err := config.LoadConfig(handle)
		if err != nil {
			contextLogger.Fatal("failed to load config: ", err.Error())
		}
		for _, activity := range conf.Activities {
			switch activity.Name {
			case "mineIronMiningGuild":
				activities.MineIronMiningGuild(activity.Schedule.Seconds)
			default:
				contextLogger.Fatal("no valid activities found in config")
			}
		}
	}
}
