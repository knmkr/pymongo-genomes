# Settings for MongoDB
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_USER = ""
MONGO_PASSWORD = ""
MONGO_DBNAME = "mypymongodb"
MONGO_URI = "mongodb://{HOST}:{PORT}/{DBNAME}".format(HOST=MONGO_HOST,
                                                     PORT=MONGO_PORT,
                                                     DBNAME=MONGO_DBNAME)
# "mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}".format(USER=MONGO_USER,
#                                                             PASSWORD=MONGO_PASSWORD,
#                                                             HOST=MONGO_HOST,
#                                                             PORT=MONGO_PORT,
#                                                             DBNAME=MONGO_DBNAME)
