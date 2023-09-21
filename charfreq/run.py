from __future__ import annotations

from logging import getLogger
import os


log = getLogger(__name__)


def character_frequency(
        paths: list[str],
        symbols: bool = True,
        alpha: bool = True,
        bigram: bool = False,
) -> dict:
    main_tally = dict()
    for path in paths:
        if not os.path.isfile(path) or not os.path.exists(path):
            continue

        with open(path, 'r') as file:
            try:
                lines = file.read().splitlines()
            except UnicodeDecodeError as e:
                log.info(
                    f'Failed to decode {path}, continuing anyway',
                    exc_info=e
                )
                continue

            log.debug(f'tallying {path}')
            if bigram:
                sub_tally = tally_up_bigram(lines)
            else:
                sub_tally = tally_up(lines)
            main_tally = merge(main_tally, sub_tally)

    main_tally = clean_dict(main_tally, symbols, alpha, bigram)
    return dict(sorted(main_tally.items(), key=lambda x: x[1]))


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


def tally_up(lines: list[str]) -> dict:
    output = dict()
    for line in lines:
        for char in line:
            output[char] = output.get(char, 0) + 1
    return output


def tally_up_bigram(lines: list[str]) -> dict:
    output = dict()
    for line in lines:
        for i in range(0, len(line) - 1):
            combo = line[i] + line[i+1]
            output[combo] = output.get(combo, 0) + 1
    return output


def clean_dict(tally: dict, symbols: bool, alpha: bool, bigram: bool) -> dict:
    if not symbols and not alpha:
        return tally

    remove_keys = []
    slist = [
        "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "%", "[", "]", "\\",
        "+", "=", "-", "_", "|", "<", ">", "?", "/", "\"", "'", "{", "}", ":",
        "`", ";", ",", "."
    ]
    for key in tally.keys():
        if bigram:
            if symbols and (key[0] not in slist or key[1] not in slist):
                remove_keys.append(key)
                continue
            if alpha and (not key[0].isalnum() or not key[1].isalnum()):
                remove_keys.append(key)
                continue
        else:
            if symbols and key not in slist:
                remove_keys.append(key)
                continue
            if alpha and not key.isalnum():
                remove_keys.append(key)
                continue

    [tally.pop(k, None) for k in remove_keys]
    return tally


def clean_json(input: str) -> str:
    # A lot of "\uXXXX" characters were being displayed, cleaning them here.
    output = ""
    for line in input.splitlines():
        if '\\u' not in line:
            output += f'{line}{os.linesep}'

    return output
