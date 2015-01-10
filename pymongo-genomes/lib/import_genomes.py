import sys
import os
import logging

import pymongo


def _getLogger(level=logging.DEBUG):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s'))
    logger.addHandler(handler)
    return logger
log = _getLogger()


def import_genomes():
    log.info('pass')

    # with pymongo.Connection(host=settings.MONGO_URI) as connection:
    #     db = connection['pergenie']

    #     for username in user_ids or settings.CRON_DIRS.keys():
    #         log.info('===============================')
    #         log.info('Job for username: %s' % username)
    #         # Try to import/update files
    #         # If timestamp is newer than one in DB, re-import.
    #         for datadir in settings.CRON_DIRS[username]:
    #             log.debug('datadir: %s' % datadir)
    #             for fileformat in settings.FILEFORMATS:
    #                 glob_path = os.path.join(datadir, fileformat['name'], fileformat['extention'])
    #                 filepaths = glob.glob(glob_path)

    #                 for filepath in filepaths:
    #                     log.debug('filepath: %s' % filepath)
    #                     last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
    #                     info = {'user_id': username,
    #                             'name': clean_file_name(os.path.basename(filepath), fileformat['name']),
    #                             'raw_name': os.path.basename(filepath),
    #                             'date': last_modified,
    #                             'population': POPULATION,
    #                             'file_format': fileformat['name'],
    #                             'catalog_cover_rate': db['catalog_cover_rate'].find_one({'stats': 'catalog_cover_rate'})['values'][fileformat['name']],
    #                             'genome_cover_rate': db['catalog_cover_rate'].find_one({'stats': 'genome_cover_rate'})['values'][fileformat['name']],
    #                             'status': float(0.0)}

    #                     db_info = db['data_info'].find_one({'user_id': username, 'name': info['name']})

    #                     if db_info and (last_modified < db_info['date']): continue

    #                     db['data_info'].insert(info)
    #                     log.info('Importing into DB: %s' % filepath)
    #                     log.info(import_variants(filepath,
    #                                              info['population'],
    #                                              info['file_format'],
    #                                              info['user_id']))

    #                     # `info` is overwritten in import_variants
    #                     new_info = genomes.get_data_info(info['user_id'], info['name'])

    #                     # if import_variants succeeded
    #                     if new_info.get('status') != -1:
    #                         # Riskreport
    #                         riskreport.import_riskreport(new_info)
    #                         riskreport.write_riskreport(username, [new_info], force_uptade=True)

    #                         # population PCA
    #                         person_xy = [0,0]  # FIXME: projection(info)
    #                         db['data_info'].update({'user_id': new_info['user_id'], 'name': new_info['name']},
    #                                                {"$set": {'pca': {'position': person_xy,
    #                                                                  'label': new_info['user_id'],
    #                                                                  'map_label': ''},
    #                                                          'status': 100}})
    #         log.info('Import new files done.')

    #         # Try to delete non exist files.
    #         # If file exists in DB, but does not exist,
    #         # delete data_info and variants from DB.
    #         user_datas = db['data_info'].find({'user_id': username})
    #         for user_data in user_datas:

    #             # Check if file exists
    #             is_file_exists = False
    #             for datadir in settings.CRON_DIRS[username]:
    #                 db_filepath = os.path.join(datadir, user_data['file_format'], user_data['raw_name'])
    #                 if os.path.exists(db_filepath):
    #                     is_file_exists = True
    #                     break

    #             if not is_file_exists:
    #                 log.warn('Deleting from DB: %s %s %s' % (username, user_data['raw_name'], user_data['file_format']))
    #                 db.drop_collection('variants.{0}.{1}'.format(username, user_data['name']))
    #                 db.drop_collection('reports.{0}.{1}'.format(username, user_data['name']))
    #                 for r in db['data_info'].find({'user_id': username, 'raw_name': user_data['name']}):
    #                     db['data_info'].remove(r)

    #         log.info('Delete non exist files done.')
    #     log.info('Finished!')
