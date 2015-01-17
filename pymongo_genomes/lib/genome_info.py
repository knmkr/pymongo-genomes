import pymongo

from logger import getLogger
log = getLogger(__name__)


class GenomeInfo(object):
    def __init__(self, mongo_uri=''):
        self.con = pymongo.MongoClient(host=mongo_uri)
        self.db = self.con.get_default_database()
        self.genome_info = self.db['genome_info']

    def get_infos_by_owner(self, owner):
        return list(self.genome_info.find({'owner': owner}))
