from __future__ import annotations

import argparse
import logging
import sys
import textwrap
from importlib.metadata import version
from pathlib import Path

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
    args = parse_args(input_args)
    if args.debug:
        log.setLevel(logging.DEBUG)

    log.debug(args)
    handle_files(args)


def handle_files(args):
    results = character_frequency(
        args.files, args.symbols, args.alphas, args.bigram
    )
    [print(r) for r in results]


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
              charfreq --symbols ./**/*.py
              charfreq --alphas ./**/*.py
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
        '-a', '--alphas',
        action='store_true',
        help='only get alpha'
    )
    parser.add_argument(
        '-s', '--symbols',
        action='store_true',
        help='only get symbols'
    )
    parser.add_argument(
        '-b', '--bigram',
        action='store_true',
        help='get character bigram (pair) frequency',
    )
    parser.add_argument(
        'files',
        type=Path,
        nargs="+",
    )
    return parser.parse_args(args)


if __name__ == '__main__':
    main()
