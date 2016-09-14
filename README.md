# Surveillance-system

Surveillance system for Raspberry Pi


## About the project

This project was implemented as a course project for Internet of Things and media services (SGN-35016) in Tampere University of Technology. Code is written in Python. Configurations are determined in conf.json -file.

This project was designed to be used with Raspberry Pi that has a webcamera or camera module connected to it. Camera tracks footage and uploads images and videos to cloud when motion is regocnized. The motion tracking is done by motion-software, which is a motion tracking software for the Linux operating systems written in C. 

## Preparations

* Install motion with e.g apt-get (might need sudo depending of user rights)
`apt-get install motion`
* Install missing packets from requirements.txt
`pip install -r requirements.txt`
* Insert info to conf.json


## Usage

```python main.py --conf conf.json
```


## TODO

* Google Drive integration
