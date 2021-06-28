package config

import (
	log "github.com/sirupsen/logrus"
	"gopkg.in/yaml.v3"
	"io"
	"io/ioutil"
)

type Activity struct {
	Name string `yaml:"name"`
	Schedule struct {
		Seconds int64 `yaml:"seconds"`
	}
}

type Conf struct {
	Activities []Activity `yaml:"protocol"`
}

func LoadConfig(reader io.Reader) (Conf, error) {
	contextLogger := log.WithFields(log.Fields{"function": "LoadConfig"})
	contextLogger.Info("loading config")
	var c Conf
	yamlFile, err := ioutil.ReadAll(reader)
	if err != nil {
		contextLogger.Error("failed to load config.yaml: " + err.Error())
		return Conf{}, err
	}
	contextLogger.Info("unmarshaling yaml from config")
	err = yaml.Unmarshal(yamlFile, &c)
	if err != nil {
		contextLogger.Error("failed to unmarshal yaml: " + err.Error())
		return Conf{}, err
	}
	return c, nil
}
