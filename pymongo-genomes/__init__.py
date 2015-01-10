#!/usr/bin/env python

import argparse
from lib.import_genome import import_genome

try:
    from conf import MONGO_URI
except ImportError:
    MONGO_URI = ''

def main():
    import_genome('test/test.vcf41.vcf', 'you', mongo_uri=MONGO_URI)


if __name__ == '__main__':
    main()
