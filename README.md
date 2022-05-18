# ladder: Find a longest "word ladder"
Bart Massey 2022

This program finds a longest "word ladder" in a large
dictionary of fixed-length words. A word ladder is
a sequence of words with just one letter change separating
them — for example

    bat
    bag
    hag
    hog
    dog

## Install and Run

This Python 3 program requires the library
`python-igraph`. This can be installed by running

    python3 -m pip install -r requirements.txt

in this directory.

Once the `igraph` library is installed, the program can be
run with

    python3 ladder.py dictionary.txt

where `dictionary.txt` contains the candidate words, one per
line. All words must be of the same length in characters.

The dictionary `common-seven.txt` containing common
seven-letter words is provided. On a fast multicore machine,
this program runs in about a half second on this dictionary.

## License

This work is made available under the "MIT License". See the
file `LICENSE.txt` in this directory for license terms.

## Acknowledgements

Thanks to Gene Welborn for introducing me to this problem.
