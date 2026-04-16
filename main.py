# ===========================================================================
# PROJETO: Pipeline de Dados IoT com Docker e PostgreSQL
# VERSÃO: 1.0
# AUTOR: Bruna Coelho
# DATA: 04/04/2026
# OBJETIVO: 
# Realizar a ingestão, tratamento e carga de dados de sensores de 
# temperatura IoT para um banco de dados relacional, permitindo 
# análises estatísticas via Views SQL.
# ===========================================================================

import pandas as pd
from sqlalchemy import create_engine
import sys

# Configurações de conexão (Idealmente viriam de variáveis de ambiente em produção)
DB_USER = "bruna"
DB_PASS = "adminadmin"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "iot_db"

def connect_db():
    """Estabelece conexão com o banco de dados PostgreSQL via SQLAlchemy."""
    try:
        url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(url)
        return engine
    except Exception as e:
        print(f"[ERRO] Falha ao conectar no banco: {e}")
        sys.exit(1)

def process_and_load(file_path):
    """
    Lê o arquivo CSV, realiza o tratamento de tipos de dados
    e exporta para a tabela final no PostgreSQL.
    """
    engine = connect_db()
    
    try:
        print(f"[*] Iniciando leitura do arquivo: {file_path}")
        # Lendo o CSV 
        df = pd.read_csv(file_path)
        
        # Tratamento: Conversão de data para formato datetime do Python
        # Isso permite que o SQL entenda o campo como TIMESTAMP
        df['noted_date'] = pd.to_datetime(df['noted_date'], dayfirst=True)
        
        print("[*] Enviando dados para o banco de dados...")
        # if_exists='replace' recria a tabela. Em produção, usaríamos 'append'
        df.to_sql('temperature_readings', engine, if_exists='replace', index=False)
        
        print("[SUCESSO] Pipeline executado com êxito!")
        
    except FileNotFoundError:
        print(f"[ERRO] Arquivo {file_path} não encontrado na pasta.")
    except Exception as e:
        print(f"[ERRO] Ocorreu um problema durante o processamento: {e}")

if __name__ == "__main__":
    # Nome do arquivo conforme baixado do Kaggle
    FILENAME = "temperature_readings.csv" 
    process_and_load(FILENAME)