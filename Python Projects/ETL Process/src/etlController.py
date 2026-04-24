import logging
import os
import pandas as pd
from sqlalchemy import text

class ETLController:
    def __init__(self, configs, extractor, transformer, loader,
                 checkpoint_path=None, usar_ultimo_id_data=False,
                 nome_coluna_fk='id_tt', id_table='testedt', id_column='id_tt',
                 apenas_ultimo=False, coluna_ordenacao=None):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.checkpoint_path = checkpoint_path
        self.usar_ultimo_id_data = usar_ultimo_id_data   # apenas informativo, não usado para adicionar FK
        self.nome_coluna_fk = nome_coluna_fk             # não usado internamente
        self.id_table = id_table
        self.id_column = id_column
        self.configs = configs
        self.logger = logging.getLogger(__name__)
        self.apenas_ultimo = apenas_ultimo
        self.coluna_ordenacao = coluna_ordenacao

    # Este método é mantido apenas para uso externo (main.py), não é chamado internamente
    def _get_ultimo_id_data(self):
        query = f"SELECT {self.id_column} FROM {self.id_table} ORDER BY {self.id_column} DESC LIMIT 1"
        with self.configs.engine().connect() as connection:
            result = connection.execute(text(query)).fetchone()
            if result:
                return result[0]
            else:
                self.logger.warning(f"No ID found in table {self.id_table}. Using 0 as initial value.")
                return 0

    def run(self):
        try:
            df_current = self.extractor.extract()
            self.logger.info("Data extracted successfully.")

            # Carrega checkpoint apenas no modo normal
            previous_df = None
            if not self.apenas_ultimo and self.checkpoint_path and os.path.exists(self.checkpoint_path):
                previous_df = pd.read_json(self.checkpoint_path, orient='records')
                self.logger.info("Checkpoint loaded.")

            # Transformação e (opcional) deduplicação
            if self.apenas_ultimo:
                df_transformed = self.transformer.apply_transformations(df_current)
                if self.coluna_ordenacao and self.coluna_ordenacao in df_transformed.columns:
                    df_transformed = df_transformed.sort_values(self.coluna_ordenacao)
                df_transformed = df_transformed.tail(1)
                df_to_load = df_transformed.copy()
                df_current_transformed = df_transformed.copy()
                self.logger.info(f"Modo 'apenas último' ativado. Linha selecionada: {len(df_to_load)}")
            else:
                df_to_load, df_current_transformed = self.transformer.transform(df_current, previous_df)

            if df_to_load.empty:
                self.logger.info("Nenhum dado novo para carregar.")
            else:
                # NÃO adicionamos FK aqui – as FKs já foram adicionadas via loader.add_fixed_column no main.py
                self.loader.load(df_to_load)
                self.logger.info(f"Inseridas {len(df_to_load)} linhas.")

            # Salva checkpoint apenas no modo normal
            if not self.apenas_ultimo and self.checkpoint_path:
                df_current_transformed.to_json(
                    self.checkpoint_path,
                    orient='records',
                    indent=2,
                    force_ascii=False
                )
                self.logger.debug("Checkpoint salvo.")

        except Exception as e:
            self.logger.exception("ETL run failed")
            raise