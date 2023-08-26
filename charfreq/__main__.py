import logging
import os
import sys
import argparse
import textwrap
import json

from charfreq.run import character_frequency

logging.basicConfig(
    format='[%(levelname)s] %(message)s',
    level=logging.WARNING
)
log = logging.getLogger('root')


def main():
    try:
        cli_entry()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        log.error('charfreq failed', exc_info=e)
        sys.exit(1)


def cli_entry(input_args=None):
    """Entry point for the command line utility."""
    args = parse_args(input_args)
    
    if args.debug:
        log.setLevel(logging.DEBUG)

    log.debug(args)
    handle_files(args)


def handle_files(args):
    results = character_frequency(args.files, args.ignore, args.ignore_regex)
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1]))
    json_output = json.dumps(sorted_results, indent=4)

    # A lot of "\uXXXX" characters were being displayed, cleaning them here.
    clean_output = ""
    for line in json_output.splitlines():
        if '\\u' not in line:
            clean_output += f'{line}{os.linesep}'
    print(clean_output)


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog='charfreq',
        add_help=True,
    )
    parser.add_argument(
        '--debug',
        action='store_true',
    )
    parser.add_argument(
        '-f', '--files',
        type=str,
        nargs='+',
        default=[line.strip() for line in sys.stdin]
    )
    parser.add_argument(
        '-i', '--ignore',
        type=str,
        nargs='+',
        default=[]
    )
    parser.add_argument(
        '-x', '--ignore-regex',
        type=str,
    )
    return parser.parse_args(args)


if __name__ == '__main__':
    main()
