# Settings for MongoDB
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_USER = ""
MONGO_PASSWORD = ""
MONGO_URI = "mongodb://{HOST}:{PORT}".format(HOST=MONGO_HOST,
                                             PORT=MONGO_PORT)
# "mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}".format(USER=MONGO_USER,
#                                                    PASSWORD=MONGO_PASSWORD,
#                                                    HOST=MONGO_HOST,
#                                                    PORT=MONGO_PORT)
