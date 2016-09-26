# Pirates of the Carribean Online - Private Server
![](https://img.shields.io/badge/VERSION-1.0.0-green.svg)
![](https://img.shields.io/badge/STATE-EARLY--DEV-red.svg)

**Warning: This is the development (aka Master) branch. DO NOT clone from this branch when running a production server**

Pirates Online - Private Server is an Astron based, open source project aiming to emulate POTCO using the 2013 source files. It's currently in early stages of development and is not yet ready for public usage.

When commiting, make sure to follow the general commit format "(FILE): (COMMIT)". E.g. Lets say I fixed something within Pirates Client Repository; My commit would look like "PCR: Fixed issue in Pirates Client Repository" (Obiously you would go more in depth in the commit description)

## Requirements

#### Panda3D
Panda3D 1.10.0 with Astron support is the game engine used by POTCO-PS. You can find the repo with build instructions [here](https://github.com/Astron/panda3d).

### Resources
The resource files (Commonly refered to as "Phase Files") are the assets for the game (3D Models, Texture Maps, etc.) You can clone/download the repo they are stored in [here](https://github.com/ksmit799/POTCO-PS-Resources).

## Usage
In order to run the source (uncompiled) navigate to the POTCO-PS folder (Where you cloned the repo) and issue the following commands.
```sh
$ start_client.bat
$ start_astron.bat
$ start_astron_ai.bat
$ start_astron_ud.bat
```
You can also navigate to the repo in file explorer and run the above bat files.

## Building for production
When building for production, the recommended compiler to use is Nirai. Nirai can be found [here](https://github.com/nirai-compiler/src).
