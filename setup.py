#!/usr/bin/env python
from distutils.core import setup


if __name__ == "__main__":
    setup(name='oopsy',
          description="ECMWF OOPS Scripts Project",
          author="Francesco Pierfederici",
          author_email="francesco.pierfederici@ecmwf.int",
          license="GPL",
          version='0.1',

          packages=['oopsy', ],
          )
