# Runescape Python bot

## System requirements and build notes

### OS compatibility

* Ubuntu 18.04
* Ubuntu 20.04
* Ubuntu 22.04

`build.sh` has everything you need to install the dependencies.

This application expects a `ramfs` mounted at `/tmp/yeetcachemoney`,
which is configured in `build.sh`.

`ml_build.sh` installs machine learning dependencies.
This one you have to babysit and run one section at a time,
since a reboot is required halfway through.

### NOTE

* The build scripts are not robust, 
you are better off cherrypicking the commands for installing the various dependencies.
* On Ubuntu 22.04, you need to disable Wayland to use Xorg:
  * `/etc/gdm3/custom.conf`
  * uncomment `#WaylandEnable=false`

## Botting

The `bot` module contains all the code for running bots.
* `bot/classic` contains code that uses classic rules based reasoning
to move through workflows.
* `bot/ml` contains machine learning code for a more modern approach.
  * **This module is not currently working.**

List of functioning modules:
 * `bot/action/smelt_steel_al-kharid.py`
 * `bot/action/mine_coal_barbarian_village.py`
 * `bot/action/mine_iron_se_varrock.py`
 * `bot/action/smelt_bronze_al-kharid.py`
 * `bot/action/mine_copper_tin_se_varrock.py`
   
To use one of the above functioning action modules, 
open up the `bot/etc/config.json` file and change the `activities` section:

```json
"activities": [
    {
        "name": "mine_copper_tin_se_varrock",
        "schedule": {
          "seconds": 600
        }
    }
]
```

In the above example, 
the `mine_copper_tin_se_varrock` 
module will get executed for 600 seconds and quit.

NOTE: Changing the credentials will currently have no effect
on the behavior of the application.
Once automatic login/logout is implemented,
this will be relevant along with the VPN configuration section.  

### Writing your own action module

If you start modifying code, 
make your own branch and change the screenshots if things don't work.

The `bot/classic/common.py` contains helper functions that abstract many low level tasks.
You can chain them together with other programming structures
to get the desired behavior. 
There are comments peppered throughout the existing code that explain 
how I solved certain problems or just add some clarification to what is going on.

This section definitely needs to be better documented. On my TODO list!

## Flipping

The `flip` module contains code and configuration files for tracking
inventory and comparing that to the evolving state of the GE
to alert when the inventory should be offloaded.

## Scripts

The `scripts` directory contains useful scripts for various tasks like
taking screenshots.
