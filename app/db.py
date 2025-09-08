from sqlalchemy import create_engine

_driver_to_scheme = {
    "postgresql": "postgresql+psycopg",  # psycopg3
    "mysql": "mysql+pymysql",
}

def get_engine(db_conf: dict):
    driver = db_conf.get("driver", "postgresql")
    scheme = _driver_to_scheme.get(driver, driver)
    host = db_conf.get("host")
    port = db_conf.get("port")
    database = db_conf.get("database")
    username = db_conf.get("username")
    password = db_conf.get("password")
    uri = f"{scheme}://{username}:{password}@{host}:{port}/{database}"
    return create_engine(uri, pool_pre_ping=True, pool_recycle=3600)
