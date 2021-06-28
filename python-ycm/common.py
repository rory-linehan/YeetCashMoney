import json
import subprocess
import pathlib
import os


class DirContext:
    def __init__(self, dir):
        self._dir = dir

    def __enter__(self):
        self._cwd = os.getcwd()
        os.chdir(self._dir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self._cwd)


def get_config(file):
    print('getting config: ' + file)
    with open(file, 'r') as handle:
        config = json.loads(handle.read())
    if config:
        return True, config
    else:
        return True, 'failed to get config'


# start up RuneLite, and hand execution back to main
def runelite():
    process = subprocess.Popen(
        ['.sdkman/candidates/java/current/bin/java', '-jar', 'bin/RuneLite.jar'],
        cwd=str(pathlib.Path.home())
    )
    process.wait()
    return process
