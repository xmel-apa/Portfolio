import pandas as pd

class Transformer:
#-- Realiza as transformações necessárias na extração dos dados, como renomear colunas, filtrar colunas e comparar com os checkpoints anteriores para identificar novos registros
     def __init__(self, column_mapping=None, key_columns=None, columns_to_keep=None):
         self.column_mapping = column_mapping or {} # Mapeamento de colunas {}
         self.key_columns = key_columns or [] # Colunas que formam a chave composta para comparação
         self.columns_to_keep = columns_to_keep # Lista de colunas a manter (filtragem), no caso de novos checkpoints

     def _apply_transformations(self, df):
         #-- Aplica filtro de colunas e renomeação
         df = df.copy()
         if self.columns_to_keep:
             df = df[self.columns_to_keep]
         if self.column_mapping:
             df = df.rename(columns=self.column_mapping)
         return df

     def apply_transformations(self, df):
         #-- Método público para transformar um DataFrame (sem comparação)
         return self._apply_transformations(df)

     def transform(self, df_current, previous_df=None):
         #-- Transforma os dados atuais e compara com checkpoint (se houver)
         df_current_transformed = self._apply_transformations(df_current)

         if previous_df is None:
             return df_current_transformed, df_current_transformed

         if not self.key_columns:
             return df_current_transformed, df_current_transformed
         
         #- Cria chaves compostas para deduplicação
         # Concatenando os valores das colunas e unificando para criar uma chave única para comparação
         df_current_transformed['_key'] = (
             df_current_transformed[self.key_columns]
             .astype(str)
             .agg('-'.join, axis=1)
         )
         previous_df = previous_df.copy()
         previous_df['_key'] = (
             previous_df[self.key_columns]
             .astype(str)
             .agg('-'.join, axis=1)
         )

        #-- Filtra novos registros comparando as chaves criadas, e remove a coluna de chave após a comparação 
         df_new = df_current_transformed[
             ~df_current_transformed['_key'].isin(previous_df['_key'])
         ].drop(columns=['_key'])

         df_current_transformed = df_current_transformed.drop(columns=['_key'])
         return df_new, df_current_transformed