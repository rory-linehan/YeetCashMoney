# Runescape Python bot

## Build

Everything assumes Ubuntu 18.04. 
There are helper scripts and such for running elsewhere (Windows), 
but I don't guarantee it will work.

`build.sh` will install the base dependencies automatically.

`ml_build.sh` installs machine learning dependencies.
This one you have to babysit and run one section at a time,
since a reboot is required halfway through.

## Botting

The `bot` module contains all the code for running bots.
* `bot/classic` contains code that uses classic rules based reasoning
to move through workflows.
* `bot/ml` contains machine learning code for a more modern approach.
  * **This module is not currently used or even working correctly.**

List of functioning modules:
 * `bot/classic/action/smelt_steel_al-kharid.py`
   * Smelts steel bars in Al-Kharid
 * `bot/classic/action/mine_coal_barbarian_village.py`
   * Mines coal in Barbarian Village
 * `bot/classic/action/mine_iron_se_varrock.py`
   * Mines iron in SE Varrock
 * `bot/classic/action/smelt_bronze_al-kharid.py`
   * Smelts bronze bars in Al-Kharid
 * `bot/classic/action/mine_copper_tin_se_varrock.py`
   * Mines copper and tin in SE Varrock
   
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
