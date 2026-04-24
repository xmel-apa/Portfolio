# Carrega variáveis de ambiente e fornece credenciais
# Charge enviroment variables and provide credentials 

# configs.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus

class Configs:
    def __init__(self, dotenv_path=None):
        # Usa o parâmetro dotenv_path (e não self.dotenv_path)
        load_dotenv(dotenv_path)
        
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_USER = os.getenv('DB_USER')
        # Aplica quote_plus apenas se a senha existir
        raw_password = os.getenv('DB_PASSWORD')
        self.DB_PASSWORD = quote_plus(raw_password) if raw_password else ''
        self.DB_PORT = os.getenv('DB_PORT')

    def engine(self):
        return create_engine(f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')