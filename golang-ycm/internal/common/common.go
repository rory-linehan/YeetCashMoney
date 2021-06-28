package common

import (
	"math/rand"
	"time"
)

func randomDelayShort() {
	time.Sleep(time.Duration(rand.Float32()))
}

func loadObjects(module string, objects []string, commonObjects []string) () {

}