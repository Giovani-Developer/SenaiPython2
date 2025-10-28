## conexao_bd.py
import psycopg2

## Função para conectar o banco de dados via ORM SQLAlchemy
def conectarSQLAlchemy():
    conectar_al = 'postgresql://postgres:senaisp@localhost:5432/loja_virtual'
    return conectar_al


## Funcão para conectar ao Bando de Dados via Psycopg2
def conectar_bd():
    conecta_bd = psycopg2.connect(
        database='loja_virtual',
        user='postgres',
        password='senaisp',
        host='localhost',
        port='5432'
    )
    return conecta_bd 



