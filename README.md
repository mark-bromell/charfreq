# charfreq

Get the frequency of characters in your files!

## Install

```shell
pip3 install charfreq
```
## Usage

Rather than going into detail on how to use this, here's a few example commands
to help you know what to expect from the tool.

```shell
charfreq --help

# Check a file
charfreq -f script.py

# Check many files
charfreq -f script.py test.py api.js

# Ignore the space and * character
charfreq -f script.py -i " " "*"

# Ignore based on regex
charfreq -f script.py -x "[a-zA-Z]"

# Pipe in files using find
find . -type f -name "*.py" | charfreq

# Pipe and ignore chars using regex (this can be quite slow with large file trees)
find . -type f -name "*.py" | charfreq -x "[a-zA-Z0-9]"
```
