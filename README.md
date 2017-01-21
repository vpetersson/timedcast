# TimedCast

**Work in progress.**

A tool for scheduling audio playback for Chromcast and Chromecast Audio. The primary goal was to create an alarm clock that starts to stream music to a Chromecast (or group of Chromecasts) at a set hour using a simple cronjob.

Features:
* Automatically connect to a defined Chromecast
* Randomly picks an audio stream (configurable)
* Starts at a low volume (configurable)
* Gradually increases the volume (to a set max)
* Stops playing after a set time

## Usage

```
$ pip install -r requirements.txt
$ python cast.py
```
