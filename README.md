# Snapcraft architectures parser

This is mostly CLI and test scaffolding set up around the more interesting
library that is meant to be taken and massaged as necessary. Basically, copy the
`architectures_parser` directory and remove the `cli` subdirectory. This was
written to be compatible with both python2 and 3.


The CLI provides an easy way to poke at the library to see what it does. See
`architectures-parser --help` for more info.

To run the tests, run `python3 -m unittest discover tests.unit` (or whatever
your version of python is).
