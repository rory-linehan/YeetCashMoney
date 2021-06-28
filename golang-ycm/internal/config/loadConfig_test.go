package config

import (
	"errors"
	"strings"
	"testing"
)

func TestLoadConfig(t *testing.T) {
	_, err := LoadConfig(strings.NewReader(`
activities:
- name: mine_iron_mining_guild
  schedule:
    seconds: 8000`))
	if err != nil {
		t.Fatal()
	}
}

func TestLoadInvalidConfig(t *testing.T) {
	_, err := LoadConfig(strings.NewReader(`invalid`))
	if err == nil {
		t.Fatal()
	}
}

type brokenReader struct{}

func (r brokenReader) Read(o []byte) (n int, err error) {
	return 0, errors.New("broke")
}

func TestLoadIOError(t *testing.T) {
	_, err := LoadConfig(brokenReader{})
	if err == nil {
		t.Fatal()
	}
}
