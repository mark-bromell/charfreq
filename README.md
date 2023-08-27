# charfreq

Get the frequency of characters in your files!
Outputs JSON with character counts

## Install

```shell
pip3 install charfreq
```

## Example usage

```shell
charfreq --only "[()]" ./**/*.py
```

This outputs the following JSON
```json
{
    "(": 83281,
    ")": 83286
}
```

### More random examples

```shell
# Have a look at the options available
charfreq --help

# Check a file
charfreq script.py

# Check many files
charfreq script.py test.py api.js

# Test all py files recursively using glob (only tested on bash shell)
charfreq ./**/*.py

# Use multiple globs! (only tested on bash shell)
charfreq ./**/*.py ./**/*.html

# Exclude characters based on regex
charfreq --exclude "[a-zA-Z]" ./**/*.py

# Only capture characters based on regex
charfreq --only "[a-zA-Z]" ./**/*.py
```
