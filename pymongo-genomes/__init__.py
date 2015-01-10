#!/usr/bin/env python

import os
import argparse
from lib.import_genome import import_genome
from lib.genome import Genome

try:
    from conf import MONGO_URI
except ImportError:
    MONGO_URI = ''

def main():
    import_genome('test/test.vcf41.vcf', 'you', mongo_uri=MONGO_URI)

    g = Genome('test.vcf41.vcf', 'you', mongo_uri=MONGO_URI)
    print g.get_genotype_by_rsid(6054257)
    print g.get_genotype_by_rsid(60)

if __name__ == '__main__':
    main()
