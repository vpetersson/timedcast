import pychromecast
import requests
import sys
from random import shuffle
from time import sleep


VOLUME_MIN = 0.05
VOLUME_MAX = 0.4

# Gradually increase or decrease the volume.
VOLUME_INCREASE = True

# Intervals of volume increase/decrease
VOLUME_INTERVALS = 10

# Total duration of playback
TIMER = 3600

TARGET = 'Home group'
STREAMS = [
    'http://streaming214.radionomy.com/1000ClassicalHits',
    'http://streaming213.radionomy.com/1000HITSClassicalMusic',
    'http://streaming202.radionomy.com/1000HITSClassicalMusic',
    'http://streaming208.radionomy.com:80/1000HITSClassicalMusic',
    'http://stream-mp3-hd2.intellis.usf.edu:8064/listen',
    'http://streaming213.radionomy.com:80/ABC-Piano',
    'http://streaming202.radionomy.com:80/ABC-Piano',
    'http://streaming208.radionomy.com:80/ABC-Piano',
    'http://streaming210.radionomy.com:80/ABC-Piano',
]


def get_device(chromecasts, name):
    for cast in chromecasts:
        if cast.device.friendly_name == name:
            cast.wait()
            return cast
    return False


def send_stream(device, audiostream):
    mc = device.media_controller
    mc.play_media(audiostream, 'audio/mp3')
    return mc


def pick_stream():
    shuffle(STREAMS)
    for s in STREAMS:
        if requests.head(s).ok:
            print('Using stream: {}'.format(s))
            return s
    return False


def volume_control(device, volume):
    step = 0
    while step < VOLUME_INTERVALS:
        sleep(TIMER / VOLUME_INTERVALS)

        if VOLUME_INCREASE:
            volume += (VOLUME_MAX - VOLUME_MIN)/VOLUME_INTERVALS
        else:
            volume -= (VOLUME_MAX - VOLUME_MIN)/VOLUME_INTERVALS

        print('Adjusting volume to "{}".'.format(round(volume, 3)))
        device.set_volume(volume)
        step += 1


def list_chromecasts(chromecasts):
    for cast in chromecasts:
        print('{} ({})'.format(cast.device.friendly_name, cast.device.model_name))


def main():
    chromecasts = pychromecast.get_chromecasts()

    device = get_device(chromecasts, TARGET)
    if not device:
        print('Device "{}" not found'.format(TARGET))
        sys.exit(1)

    stream = pick_stream()
    if not stream:
        print('No valid stream found')

    print('Found device "{}".'.format(TARGET))

    if VOLUME_INCREASE:
        volume = VOLUME_MIN
    else:
        volume = VOLUME_MAX

    # Set base volume twice as it appears to not 
    # always take on the first attempt.
    volume = device.set_volume(volume)
    sleep(1)
    volume = device.set_volume(volume)

    print('Setting initial volume to "{}"'.format(volume))

    print('Starting stream...')
    stream = send_stream(device, stream)
    volume_control(device, volume)

    stream.stop()
    print('Time up. Exiting.')

if __name__ == '__main__':
    main()
