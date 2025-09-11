from sqlalchemy import create_engine
import os

_driver_to_scheme = {
    "postgresql": "postgresql+psycopg",  # psycopg3
    "mysql": "mysql+pymysql",
}

def get_engine(_db_conf: dict):
    # Read ONLY from environment variables
    driver = os.environ.get("DB_DRIVER", "postgresql")
    scheme = _driver_to_scheme.get(driver, driver)

    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    database = os.environ.get("DB_NAME")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")

    # Optional TLS controls (set in task definition if needed)
    sslmode = os.environ.get("DB_SSLMODE")  # e.g., "require" for Postgres
    ssl_ca = os.environ.get("DB_SSL_CA")    # path to CA for MySQL

    missing = [k for k, v in {
        "DB_HOST": host, "DB_PORT": port, "DB_NAME": database,
        "DB_USERNAME": username, "DB_PASSWORD": password
    }.items() if not v]
    if missing:
        raise RuntimeError(f"Missing required database environment variables: {', '.join(missing)}")

    if driver == "postgresql":
        uri = f"{scheme}://{username}:{password}@{host}:{port}/{database}"
        if sslmode:
            sep = "&" if "?" in uri else "?"
            uri = f"{uri}{sep}sslmode={sslmode}"
        return create_engine(uri, pool_pre_ping=True, pool_recycle=3600)

    if driver == "mysql":
        uri = f"{scheme}://{username}:{password}@{host}:{port}/{database}"
        
        # Handle SSL based on server requirements
        ssl_mode = os.environ.get("DB_SSL_MODE", "REQUIRED")
        
        if ssl_mode == "REQUIRED":
            # For Azure MySQL with require_secure_transport=ON
            connect_args = {"ssl": {"check_hostname": False}}
        elif ssl_mode == "VERIFY_CA":
            # For CA verification
            ssl_ca = os.environ.get("DB_SSL_CA")
            if ssl_ca:
                connect_args = {"ssl": {"ca": ssl_ca, "check_hostname": False}}
            else:
                connect_args = {"ssl": {"check_hostname": False}}
        else:
            # No SSL
            connect_args = {}
        
        return create_engine(uri, connect_args=connect_args, pool_pre_ping=True, pool_recycle=3600)

    uri = f"{scheme}://{username}:{password}@{host}:{port}/{database}"
    return create_engine(uri, pool_pre_ping=True, pool_recycle=3600)