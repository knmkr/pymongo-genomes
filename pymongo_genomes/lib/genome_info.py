import pymongo

from logger import getLogger
log = getLogger(__name__)


class GenomeInfo(object):
    def __init__(self, mongo_uri=''):
        self.con = pymongo.MongoClient(host=mongo_uri)
        self.db = self.con.get_default_database()
        self.collection = self.db['genome_info']

    def get_infos_by_owner(self, owner):
        return list(self.collection.find({'owner': owner}))

    def get_info(self, owner, file_name):
        return self.collection.find_one({'owner': owner, 'file_name': file_name})
