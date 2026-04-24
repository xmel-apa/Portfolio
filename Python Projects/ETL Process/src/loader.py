# import pandas as pd
# from sqlalchemy import text

import pandas as pd
from sqlalchemy import text

class Loader:
    def __init__(self, engine, table_name: str, if_exists='append',
                 column_mapping=None, pk_column=None, pk_expression=None):
        self.engine = engine
        self.table_name = table_name
        self.if_exists = if_exists
        self.column_mapping = column_mapping or {}
        self.pk_column = pk_column
        self.pk_expression = pk_expression   
        self.fixed_columns = {}

    def add_fixed_column(self, column, value):
        self.fixed_columns[column] = value

    def load(self, df: pd.DataFrame):
        # Renomeia colunas conforme mapeamento (ex: 'Data' -> 'data')
        df_insert = df.rename(columns=self.column_mapping).copy()

        # Adiciona colunas fixas 
        for col, val in self.fixed_columns.items():
            df_insert[col] = val

        # Escolhe método de inserção
        if self.pk_column and self.pk_expression:
            self._insert_with_pk_expression(df_insert)
        else:
            df_insert.to_sql(
                self.table_name,
                self.engine,
                if_exists=self.if_exists,
                index=False
            )

    def _insert_with_pk_expression(self, df: pd.DataFrame):
        #-- Método que constrói um comando SQL para inserir os dados 
        # Colunas que receberão valores literais (todas exceto a PK)
        value_cols = [col for col in df.columns if col != self.pk_column]

        # Monta a lista de colunas na ordem: PK primeiro, depois as demais
        all_columns = [self.pk_column] + value_cols

        # Placeholders para as colunas de valor (usando :col para SQLAlchemy)
        # A coluna PK não recebe placeholder – recebe a expressão diretamente
        # Exemplo: INSERT INTO tabela (id, nome) VALUES (nextval('seq'), :nome)
        placeholders = [self.pk_expression] + [f":{col}" for col in value_cols]

        # Cria o comando SQL
        sql = f"""
            INSERT INTO {self.table_name} ({', '.join(all_columns)})
            VALUES ({', '.join(placeholders)})
        """

        # Converte os dados para uma lista de dicionários
        # Cada dicionário tem chaves = nome das colunas de valor
        records = df[value_cols].to_dict(orient='records')

        # Executa a inserção em uma transação
        with self.engine.begin() as conn:
            conn.execute(text(sql), records)