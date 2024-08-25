import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import declarative_base, declared_attr

host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
name = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

DB_HOST = host
DB_PORT = port
DB_NAME = name
DB_USER = user
DB_PASSWORD = password