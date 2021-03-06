#!/usr/bin/env python

import os
import argparse
from lib.import_genome import import_genome
from lib.genome import Genome
from lib.genome_info import GenomeInfo

try:
    from conf import MONGO_URI
except ImportError:
    MONGO_URI = ''

def main():
    import_genome('test/test.vcf41.vcf', 'you', mongo_uri=MONGO_URI)

    g = Genome('test.vcf41.vcf', 'you', mongo_uri=MONGO_URI)
    print g.owner
    print g.count
    print g.file_format
    print g.get_genotype_by_rsid(6054257)
    print g.get_genotype_by_rsid([60, 6054257])
    print g.get_genotype_by_rsid([60])

    genome_info = GenomeInfo(mongo_uri=MONGO_URI)
    print genome_info.get_infos_by_owner('you')

    g.remove()
    print genome_info.get_infos_by_owner('you')

    g = Genome('test.vcf41.vcf', 'you', mongo_uri=MONGO_URI)


if __name__ == '__main__':
    main()
