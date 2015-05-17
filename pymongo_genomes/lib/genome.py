import os

import pymongo

from logger import getLogger
log = getLogger(__name__)

class Genome(object):
    def __init__(self, file_name, owner, mongo_uri=''):
        self.file_name = file_name
        self.owner = owner

        self.con = pymongo.MongoClient(host=mongo_uri)
        self.db = self.con.get_default_database()

        found = self.db['genome_info'].find_one({'owner': owner, 'file_name': file_name})
        if not found:
            raise Exception('Genome not imported')  #

        if not found.get('file_uuid'):
            raise Exception('Genome not imported')  #

        self.genome = self.db['genomes'][found['file_uuid']]
        self.file_format = found['file_format']
        self.count = self.genome.count()

    def get_genotype_by_rsid(self, rsid):
        """Get genotypes by rsids.

        Args:
          rsid: a list of query rsids

        Returns:
          {rsid: genotype, ...}

        Example:
          >>> get_genotype_by_rsid([10,20,30])
          {10: 'GG', 20: '', 30: ''}
        """
        if type(rsid) == int:
            rsid = [rsid]

        genotypes = {rs: '' for rs in rsid}
        found = self.genome.find({'rs': {'$in': list(set(rsid))}})

        if found.count() > 0:
            for record in found:
                genotypes.update({record['rs']: record['genotype']})

        return genotypes

    # def get_genotype_by_chr_pos(self, chrpos):
    #     """
    #     TODO
    #     """
    #     pass

    def remove(self):
        """Remove self genome data.
        """

        # Remove genotype collection in MongoDB.
        self.db.drop_collection(self.genome)

        # Remove genome_info in MongoDB.
        self.db['genome_info'].remove({'owner': self.owner, 'file_name': self.file_name})
        return
