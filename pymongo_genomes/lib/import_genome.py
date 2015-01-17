import sys
import os
import datetime
import subprocess
from uuid import uuid4 as uuid

import pymongo

from parser.VCFParser import VCFParser, VCFParseError
from parser.andmeParser import andmeParser, andmeParseError
from logger import getLogger
log = getLogger(__name__)

def count_line(file_path):
    return int(subprocess.Popen(['wc', '-l', file_path], stdout=subprocess.PIPE).communicate()[0].split()[0])  # py26

def import_genome(file_path, owner, file_format='vcf', mongo_uri=''):
    log.info('Counting lines...')
    file_lines = count_line(file_path)
    log.info('#lines: {}'.format(file_lines))

    with pymongo.MongoClient(host=mongo_uri) as con:
        db = con.get_default_database()

        # Use UUID
        file_uuid = uuid().hex
        genome = db['genomes'][file_uuid]
        genome_info = db['genome_info']

        # Drop old collection if exists
        file_name = os.path.basename(file_path)
        old_genome_info = genome_info.find_one({'owner': owner, 'file_name': file_name})
        if old_genome_info:
            db.drop_collection(db['genomes'][old_genome_info['file_uuid']])
            log.warn('Dropped old collection')

        info = {'owner': owner,
                'file_name': file_name,
                'file_uuid': file_uuid,
                'file_format': file_format,
                'date': datetime.datetime.today(),
                'status': 1.0}

        genome_info.update({'owner': owner, 'file_name': file_name},
                           {"$set": info}, upsert=True)

        log.info('Start importing...')

        # if minimum_import:
        #     uniq_snps = set(gwascatalog.get_uniq_snps_list())

        with open(file_path, 'rb') as fin:
            try:
                p = {'vcf': VCFParser,
                     'andme': andmeParser}[info['file_format']](fin)

                for i, data in enumerate(p.parse_lines()):
                    first_sample_name = p.sample_names[0]
                    data['genotype'] = data['genotype'][first_sample_name]

                    if data['rs']:
                        # # Minimum import
                        # if minimum_import:
                        #     if not data['rs'] in uniq_snps:
                        #         continue

                        sub_data = {k: data[k] for k in ('chrom', 'pos', 'rs', 'genotype')}
                        genome.insert(sub_data)

                    if i > 0 and i % 10000 == 0:
                        log.debug('{i} lines done...'.format(i=i+1))
                        import_status = int(100 * (i * 0.9 / file_lines) + 1)
                        genome_info.update({'owner': owner, 'file_name': file_name},
                                           {"$set": {'status': import_status}})

            except (VCFParseError, andmeParseError), e:
                log.error('ParseError: %s' % e.error_code)
                genome_info.update({'owner': owner, 'file_name': file_name},
                                   {"$set": {'status': -1}})
                db.drop_collection(genome)
                return e.error_code

            log.info('Creating index...')
            genome.create_index('rs')
            genome.create_index([('chrom', pymongo.ASCENDING), ('pos', pymongo.ASCENDING)])

            log.info('#record: {}'.format(genome.count()))
            log.info('Done!')

            return
