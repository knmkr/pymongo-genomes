import sys
import os
from pprint import pformat
from collections import defaultdict

import pymongo

from logger import getLogger
log = getLogger(__name__)


class Genome(object):
    def __init__(self, file_name, owner, mongo_uri=''):
        self.con = pymongo.MongoClient(host=mongo_uri)
        self.db = self.con['pymongo-genomes']
        self.genome_info = self.db['genome_info']

        found = self.genome_info.find_one({'owner': owner, 'file_name': file_name})
        if found:
            self.genome = self.db['genomes'][found['file_uuid']]

    def get_genotype_by_rsid(self, rsid):
        found = self.genome.find_one({'rs': rsid})
        return found['genotype'] if found else ''

    def get_genotypes(self, user_id, file_name, file_format, locs, loctype='rs', rec=None, check_ref_or_not=True):
        """
        Get genotypes of a user's genome file.
        Args:
          user_id:
          file_name:
          file_format:
          locs: a list of locations. locations are chrpos(int) or rsid(int).
          loctype: 'chrpos' or 'rs'

        Returns:
          a dict: {loc: genotype}

        Example:
          >>> get_genotypes('knmkr@pergenie.org', 'genome_1.vcf', 'vcf_whole_genome', [100,200], 'rs')
          {100: 'GG', 200: 'AT'}
        """
        assert loctype in ('rs', 'chrpos')
        genotypes = dict()
        locs = list(set(locs))

        variants = self.get_variants(user_id, file_name)  #
        records = variants.find({loctype: {'$in': locs}})

        if records:
            for record in records:
                genotypes.update({record[loctype]: record['genotype']})

        # Add ref or N/A
        for loc in locs:
            if not loc in genotypes:
                if rec:
                    genotypes.update({loc: self._ref_or_na(loc, loctype, file_format, rec=rec)})
                elif check_ref_or_not:
                    # FIXME:
                    genotypes.update({loc: self._ref_or_na(loc, loctype, file_format)})

        return genotypes

    def get_data_infos(self, user_id):
        if user_id.startswith(settings.DEMO_USER_ID): user_id = settings.DEMO_USER_ID

        with MongoClient(host=settings.MONGO_URI) as c:
            data_info = c['pergenie']['data_info']
            infos = list(data_info.find({'user_id': user_id}))

        return infos

    def get_data_info(self, user_id, file_name):
        if user_id.startswith(settings.DEMO_USER_ID): user_id = settings.DEMO_USER_ID

        with MongoClient(host=settings.MONGO_URI) as c:
            data_info = c['pergenie']['data_info']
            info = data_info.find_one({'user_id': user_id, 'name': file_name})

        return info

    def search_data_info(self, user_id, query):
        """
        Example:
          query = {'rs': xxxx, 'genotype': 'XX'}

        Returns:
          # people who have genotypes of 'XX' for rs xxxx
          ['personA', 'personC']

        """
        people = set()

        # FIXME: "get data_info then, get_vatiants" is redundant (searching database twice)...
        with MongoClient(host=settings.MONGO_URI) as c:
            data_info = c['pergenie']['data_info']
            infos = list(data_info.find({'user_id': user_id}))
            for info in infos:
                variants = self.get_variants(user_id, info['name'])
                records = list(variants.find(query))
                if records:
                    people.update([info['raw_name']])

        return list(people)

    def _ref_or_na(self, loc, loctype, file_format, rec=None):
        """
        Determine if genotype is `reference` or `N/A`.
        Args:
          loc: genomic location
          loctype: 'chrpos' or 'rs'
          file_format:

        Returns:
          genotype: 'XX'

        Example:
          >>> _ref_or_na(100, 'rs', 'andme')
          'na'  # N/A in SNP array
          >>> _ref_or_na(100, 'rs', 'vcf_whole_genome')
          'GG'  # reference genome is G
        """
        assert loctype == 'rs'  # TODO: add `chrpos`

        # If fileformat is SNP array, always `N/A`.
        na = 'na'
        if file_format == 'andme':
            # log.debug('in andme region, but genotype is na')
            return na

        # If rec(gwascatalog record) is provided, use it. otherwise seach mongo.catalog.
        if not rec:
            rec = list(gwascatalog.search_catalog_by_query('rs%s' % loc, None))
            if rec:
                rec = rec[0]
            else:
                log.warn('gwascatalog record not found: loc: %s loctype: %s' % (loc, loctype))
                return na

        # Try to get ref(reference allele).
        ref = rec.get('ref')
        if not ref:
            # log.debug('try to get allele of reference genome')
            ref = self.bq.get_ref_genome(loc, rec=rec)
            if not ref:
                ref = na
                log.warn('ref not found: loc: %s loctype: %s' % (loc, loctype))

        # Cases for each fileformat
        # FIXME: reflect settings.FILEFORMAT. otherwise this hardcoding maybe buggy.
        if file_format == 'vcf_whole_genome':
            return ref * 2
        elif file_format == 'vcf_exome_truseq':
            if rec['is_in_truseq']:
                return ref * 2
            else:
                return na
        elif file_format == 'vcf_exome_iontargetseq':
            if rec['is_in_iontargetseq']:
                return ref * 2
            else:
                return na
