# pymongo-genomes

Python library for handlig personal genome data in MongoDB.

- Import personal genome data into MongoDB
  - VCF
  - gVCF
  - 23andme raw text
- Querying
  - get genotypes by rs ID
  - get genotypes by chromosome & position

Dependencies

- MongoDB
- pymongo

Getting Started

- In Python

```python
from pymogo_genomes import import_genome
from pymogo_genomes import Genome

import_genome('path/to/your.vcf', owner='you', file_format='vcf', mongo_uri=MONGO_URI)

g = Genome('your.vcf', owner='you', mongo_uri=MONGO_URI)

print g.owner
# 'you'

print g.count
# 10000

print g.file_format
# vcf

print g.get_genotype_by_rsid(100)
# 'GG'

print g.get_genotype_by_chr_pos('1', 100)
# 'GG'
```

- Commandline

```bash
$ python ./pymongo-genomes import your.vcf --owner you

$ python ./pymongo-genomes get your.vcf --owner you --rs 100
GG

$ python ./pymongo-genomes get your.vcf --owner you --chr 1 --pos 100
GG
```
