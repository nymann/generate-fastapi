import os
import uuid

from sqlalchemy.engine.url import URL

import pykpi_config


class ConfigWrapper:

    def __init__(self, cfg_path):
        common_config = pykpi_config.CommonConfig(cfg_path)
        config = common_config.get_section(self)

        self.database = config["database"]

        db_config = common_config.databases[self.database]
        db_server = db_config["server"]
        self.db_host = db_server["host"]
        self.db_port = db_server["port"]

        db_credentials = db_config.get_credentials(self)
        self.db_user = db_credentials.user
        self.db_password = db_credentials.password


config = ConfigWrapper(os.environ["PROJECT_NAME_CONFIG"])

DB_DSN = URL(drivername="postgresql",
             username=config.db_user,
             password=config.db_password,
             host=config.db_host,
             port=config.db_port,
             database=config.database)

DB_POOL_MIN_SIZE = 1
DB_POOL_MAX_SIZE = 16
DB_ECHO = False
DB_SSL = None
DB_USE_CONNECTION_FOR_REQUEST = True
DB_RETRY_LIMIT = 32
DB_RETRY_INTERVAL = 1

SECRET_KEY = str(uuid.uuid4())
