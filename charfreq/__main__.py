from __future__ import annotations

import argparse
import json
import logging
import sys
import textwrap
from importlib.metadata import version
from pathlib import Path

from charfreq.run import character_frequency, clean_json

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
    args = parse_args(input_args)
    if args.debug:
        log.setLevel(logging.DEBUG)

    log.debug(args)
    handle_files(args)


def handle_files(args):
    results = character_frequency(args.files, args.only, args.exclude)
    json_output = json.dumps(results, indent=4)
    print(clean_json(json_output))


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog='charfreq',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            examples:
              charfreq script.py
              charfreq script.py test.py api.js
              charfreq ./**/*.py
              charfreq ./**/*.py ./**/*.html
              charfreq --exclude "[a-zA-Z]" ./**/*.py
              charfreq --only "[a-zA-Z]" ./**/*.py
         ''')
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=version("charfreq")
    )
    parser.add_argument(
        '-o', '--only',
        type=str,
        metavar="re",
        help='regex of characters to only show'
    )
    parser.add_argument(
        '-x', '--exclude',
        type=str,
        metavar="re",
        help='regex of characters to exclude'
    )
    parser.add_argument(
        'files',
        type=Path,
        nargs="+",
    )
    return parser.parse_args(args)


if __name__ == '__main__':
    main()
