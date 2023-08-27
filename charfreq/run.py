from glob import iglob
from logging import getLogger
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


log = getLogger(__name__)

def frequency_parallel(
        paths: list[str],
        only: str=None,
        exclude: str=None
    ) -> dict:
    main_tally = dict()
    thread_count = min(32, os.cpu_count() + 4)
    paths_split = split(paths, thread_count)
    log.debug(f'Using {thread_count} threads')
    log.debug(f'paths split into {len(paths_split)} parts')
    with ThreadPoolExecutor() as executor:
        future_tally = [executor.submit(frequency, p) for p in paths_split]
        for future in future_tally:
            try:
                log.debug(f'future: {future}')
                sub_tally = future.result()
                main_tally = merge(main_tally, sub_tally)
            except Exception as e:
                log.info('Failed while performing parallel job',  exc_info=e)

    main_tally = clean_dict(main_tally, only, exclude)
    return dict(sorted(main_tally.items(), key=lambda x: x[1]))


def frequency(
        paths: list[str],
        only: str=None,
        exclude: str=None
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

            sub_tally = tally_up(lines)
            main_tally = merge(main_tally, sub_tally)

    main_tally = clean_dict(main_tally, only, exclude)
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


# https://stackoverflow.com/a/2135920
def split(a: list, n: int) -> list:
    k, m = divmod(len(a), n)
    result = (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))
    return list(result)


def tally_up(lines: list[str]) -> dict:
    output = dict()
    for line in lines:
        for char in line:
            output[char] = output.get(char, 0) + 1
    return output


def clean_dict(tally: dict, only: str=None, exclude: str=None) -> dict:
    remove_keys = []
    for key in tally.keys():
        if only is not None and not re.match(only, key):
            remove_keys.append(key)
            continue
        if exclude is not None and re.match(exclude, key):
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
