import textwrap

from charfreq.run import (clean_dict, clean_json, merge, tally_up,
                          tally_up_bigram)


def test_merge():
    dict1 = {
        '!': 10,
        '@': 10,
        '#': 10,
    }
    dict2 = {
        '@': 10,
        '#': 10,
        '$': 10,
    }
    merged = merge(dict1, dict2)
    assert merged == {
        '!': 10,
        '@': 20,
        '#': 20,
        '$': 10,
    }


def test_tally_up():
    lines = [
        'aaabbc',
        'abc',
        '123',
    ]
    tally = tally_up(lines)
    assert tally == {
        'a': 4,
        'b': 3,
        'c': 2,
        '1': 1,
        '2': 1,
        '3': 1,
    }


def test_tally_up_bigram():
    lines = [
        'asas',
        'qwer',
    ]
    tally = tally_up_bigram(lines)
    assert tally == {
        'as': 2,
        'sa': 1,
        'qw': 1,
        'we': 1,
        'er': 1,
    }



def test_clean_dict__only():
    tally = {
        '!': 10,
        '@': 10,
        '#': 10,
    }
    assert clean_dict(tally, only="[@]") == {
        '@': 10,
    }


def test_clean_dict__exclude():
    tally = {
        '!': 10,
        '@': 10,
        '#': 10,
    }
    assert clean_dict(tally, exclude="[@]") == {
        '!': 10,
        '#': 10,
    }


def test_clean_dict__only_and_exclude():
    tally = {
        '!': 10,
        '@': 10,
        '#': 10,
    }
    assert clean_dict(tally, only="[@]", exclude="[#]") == {
        '@': 10,
    }


def test_clean_json():
    json = textwrap.dedent("""\
        {
            "\\u1234": 10
            "$": 10
        }
    """)
    assert clean_json(json) == textwrap.dedent("""\
        {
            "$": 10
        }
    """)
