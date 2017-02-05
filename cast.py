import argparse
import pychromecast
import requests
import sys
from random import shuffle
from time import sleep


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


def pick_stream(streams):
    shuffle(streams)
    for s in streams:
        if requests.head(s).ok:
            print('Using stream: {}'.format(s))
            return s
    return False


def list_chromecasts(chromecasts):
    for cast in chromecasts:
        print('"{}" ({})'.format(
            cast.device.friendly_name,
            cast.device.model_name)
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--list",
        help="List the Chromecasts on the network",
        action="store_true"
    )

    parser.add_argument(
        "-p", "--play",
        help="Play a feed on a Chromecast device",
        action="store_true"
    )

    parser.add_argument(
        "--target",
        help="The target speakers of your feed. This can be a group or an individual device.",
    )

    parser.add_argument(
        "--streams",
        help="Specify one ore multiple streams. Must be a HTTP/HTTPS stream. Use a comma separated list for multiple feeds.",
    )

    parser.add_argument(
        "-r", "--reset_volume_on_speakers",
        help="Force volume reset on individual speakers. Use a comma separated list or multiple speakers.",
    )

    parser.add_argument(
        "--timer",
        help="The time in seconds before the feed is stopped. Default is one hour.",
        type=int,
        default=3600,
    )

    parser.add_argument(
        "--volume_start",
        help="The start volume. Default is 0.1.",
        type=int,
        default=0.1,
    )

    parser.add_argument(
        "--volume_end",
        help="The end volume. Default is 0.3",
        type=int,
        default=0.3,
    )

    parser.add_argument(
        "--volume_intervals",
        help="The number of volume 'steps' between start and end volume. Default is 10.",
        type=int,
        default=10,
    )

    args = parser.parse_args()

    if args.list:
        chromecasts = pychromecast.get_chromecasts()
        list_chromecasts(chromecasts)
        sys.exit(0)
    if args.play:
        if not (args.target and args.streams):
            print('\nError: Both a target and stream must be specified when playing.\n')
            parser.print_help()
            sys.exit(1)

        volume_increase = args.volume_end > args.volume_start

        if volume_increase:
            volume = args.volume_start
        else:
            volume = args.volume_end

        chromecasts = pychromecast.get_chromecasts()

        if args.reset_volume_on_speakers:
            """
            Volume does not seem to always be propagated
            recursively if the target is a group. To mitigate this
            we need to manually for each device..
            """
            for device in args.reset_volume_on_speakers.split(','):
                conn = get_device(chromecasts, device)
                if conn:
                    conn.set_volume(volume)
                    print('Set volume to {} on {}.'.format(volume, device))
                else:
                    print('Device {} not found'.format(device))

        device = get_device(chromecasts, args.target)
        if not device:
            print('Device "{}" not found'.format(args.target))
            sys.exit(1)

        stream = pick_stream(args.streams.split(','))
        if not stream:
            print('No valid stream found')

        # Set the volume for the device.
        volume = device.set_volume(volume)
        print('Set initial volume to {} on {}.'.format(volume, args.target))

        print('Starting stream...')
        stream = send_stream(device, stream)

        step = 0
        while step < args.volume_intervals:
            sleep(args.timer / args.volume_intervals)
            adjustment = (args.volume_end - args.volume_start)/args.volume_intervals

            if volume_increase:
                volume += adjustment
            else:
                volume -= adjustment

            print('Adjusting volume to {}.'.format(round(volume, 3)))
            device.set_volume(volume)
            step += 1

        stream.stop()
        print('Time up. Exiting.')

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
