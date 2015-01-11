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
        if found:
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

        TODO:
          - Optionally, fill reference genotype if given rsid is no in db but is in sequenced region.
        """
        if type(rsid) == int:
            rsid = [rsid]

        genotypes = {rs: '' for rs in rsid}
        found = self.genome.find({'rs': {'$in': list(set(rsid))}})

        if found.count() > 0:
            for record in found:
                genotypes.update({record['rs']: record['genotype']})

        return genotypes

    def get_genotype_by_chr_pos(self, chrpos):
        pass

    def is_blnak_record_sequenced(self, rs, file_format):
        pass
        # """Determine if genotype is `reference` or `N/A`.

        # By checking if it is in sequenced region of the file_format: vcf_whole_genome, snparray_23andme, etc.

        # TODO:
        #   - Add exome region
        # """

        # return file_format == 'vcf_whole_genome'

        # TODO: exome region
        # # Extract region
        #         region_file = os.path.join(settings.PATH_TO_INTERVAL_LIST_DIR, file_format['region_file'] + '.{0}.interval_list'.format(chrom))
        #         extracted = extract_region(region_file, ok_records)
        #         n_counter[file_format['short_name']] += len(extracted)
        #         for record in extracted:
        #             catalog.update(record, {"$set": {'is_in_' + file_format['short_name']: True}})

        #         # Uniq records
        #         ok_records_uniq = []
        #         uniq_snps = set([rec['snp_id_current'] for rec in ok_records])
        #         for record in ok_records:
        #             if record['snp_id_current'] in uniq_snps:
        #                 ok_records_uniq.append(record)
        #                 uniq_snps.remove(record['snp_id_current'])
        #         n_counter_uniq[file_format['short_name']] += len(extract_region(region_file, ok_records_uniq))

    def get_reference_allele():
        pass
        # # Try to get ref(reference allele).
        # ref = rec.get('ref')
        # if not ref:
        #     # log.debug('try to get allele of reference genome')
        #     ref = self.bq.get_ref_genome(loc, rec=rec)
        #     if not ref:
        #         ref = na
        #         log.warn('ref not found: loc: %s loctype: %s' % (loc, loctype))
