#!/usr/bin/env sh

git clone https://github.com/mark-bromell/charfreq
cd charfreq
pip3 install -e .
cd ..
rm -rf charfreq
