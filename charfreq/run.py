from logging import getLogger
import re


log = getLogger(__name__)

def character_frequency(
        paths: list[str],
        ignore: list[str],
        ignore_regex: str=None,
    ) -> dict:
    main_tally = dict()
    for path in paths:
        log.debug(f'opening {path}')
        with open(path, 'r') as file:
            try:
                lines = file.read().splitlines()
            except UnicodeDecodeError as e:
                log.error(f'Failed to decode {path}, continuing anyway', exc_info=e)
                continue

            log.debug(f'tallying {path}')
            tally = _tally(path, lines, ignore, ignore_regex)
            main_tally = merge(main_tally, tally)

    return main_tally


def merge(tally1: dict, tally2: dict) -> dict:
    new_dict = dict()
    conflicts = tally1.keys() & tally2.keys()

    for c in conflicts:
        new_dict[c] = tally1[c] + tally2[c]

    for key in tally1.keys() - tally2.keys():
        new_dict[key] = tally1[key]

    for key in tally2.keys() - tally1.keys():
        new_dict[key] = tally2[key]

    return new_dict


def _tally(
        path: str,
        lines: list[str],
        ignore: list[str],
        ignore_regex: str=None,
    ) -> dict:
    tally = dict()
    for line_no, line in enumerate(lines):
        for column_no, char in enumerate(line):
            if char in ignore:
                log.debug(f'ignore "{char}" {path}:{line_no+1}:{column_no+1}')
                continue
            if ignore_regex is not None and re.match(ignore_regex, char):
                log.debug(f'ignore "{char}" {path}:{line_no+1}:{column_no+1}')
                continue
            tally[char] = tally.get(char, 0) + 1
    return tally
