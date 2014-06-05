#!/bin/bash
sphinx-apidoc -f -o api/ ../api/
sphinx-apidoc -f -o item/ ../item/
sphinx-apidoc -f -o champion/ ../champion/
sphinx-apidoc -f -o summoner/ ../summoner/
sphinx-apidoc -f -o lol_stats/ ../lol_stats/
make clean
make html
