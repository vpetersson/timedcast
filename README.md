# TimedCast

A tool for scheduling audio playback for Chromecast and Chromecast Audio. The primary goal was to create an alarm clock that starts to stream music to a Chromecast (or group of Chromecasts) at a set hour using a simple cronjob.

Features:
* Automatically connect to a defined Chromecast
* Randomly picks an audio stream (configurable)
* Starts at a low volume and gradually increases the volume
* Stops playing after after a set duration

## Installation

```
$ git clone git@github.com:vpetersson/timedcast.git
$ cd timedcast
$ pip install -r requirements.txt
```

## Usage

```
$ python cast.py
usage: cast.py [-h] [-l] [-p] [--target TARGET] [--streams STREAMS]
               [-r RESET_VOLUME_ON_SPEAKERS] [--timer TIMER]
               [--volume_start VOLUME_START] [--volume_end VOLUME_END]
               [--volume_intervals VOLUME_INTERVALS]

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List the Chromecasts on the network
  -p, --play            Play a feed on a Chromecast device
  --target TARGET       The target speakers of your feed. This can be a group
                        or an individual device.
  --streams STREAMS     Specify one ore multiple streams. Must be a HTTP/HTTPS
                        stream. Use a comma separated list for multiple feeds.
  -r RESET_VOLUME_ON_SPEAKERS, --reset_volume_on_speakers RESET_VOLUME_ON_SPEAKERS
                        Force volume reset on individual speakers. Use a comma
                        separated list or multiple speakers.
  --timer TIMER         The time in seconds before the feed is stopped.
                        Default is one hour.
  --volume_start VOLUME_START
                        The start volume. Default is 0.1.
  --volume_end VOLUME_END
                        The volume at the end of the feed. Default is 0.4
  --volume_intervals VOLUME_INTERVALS
                        The number of volume 'steps' between start and end
                        volume. Default is 10.

```

Now let's get started. First, we scan for the Chromecasts available:
```
$ python cast.py --list
"Living Room" (Chromecast Audio)
"Bed" (Chromecast Audio)
"Home Group" (Google Cast Group)
```


With this data, we can now start playing:
```
$ python cast.py --play \
    --timer=3600 \
    --target="Home Group" \
    --stream="http://streaming214.radionomy.com/1000ClassicalHits" \
    -r "Bed,Living Room"
Set volume to 0.1 on Bed.
Set volume to 0.1 on Living Room.
Using stream: http://streaming214.radionomy.com/1000ClassicalHits
Set initial volume to 0.1 on Home Group.
Starting stream...
Adjusting volume to 0.16.
Adjusting volume to 0.22.
Adjusting volume to 0.28.
Adjusting volume to 0.34.
Adjusting volume to 0.4.
Time up. Exiting.
```
