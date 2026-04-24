import json
import logging
from configs import Configs
from extractor import Extractor
from transformer import Transformer
from loader import Loader
from etlController import ETLController
from sqlalchemy import text

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    configs = Configs()
    engine = configs.engine()    

    with open('tables_config.json', 'r', encoding='utf-8') as f:
        tables_config = json.load(f)

    generated_ids = {}

    for cfg in tables_config:
        nome_tabela = cfg.get('nome', 'desconhecida')
        logging.info(f"Iniciando ETL para a tabela: {nome_tabela}")

        try:
            extractor = Extractor(
                file_path=cfg['arquivo'],
                sheet_name=cfg['aba'],
                usecols=cfg.get('colunas')
            )

            transformer = Transformer(
                column_mapping=cfg.get('mapeamento', {}),
                key_columns=cfg.get('chave', [])
            )

            loader = Loader(
                engine=engine,
                table_name=cfg['tabela_bd'],
                column_mapping=cfg.get('mapeamento', {}),
                pk_column=cfg.get('pk_column'),
                pk_expression=cfg.get('pk_expression')
            )

            # Adicionar colunas de chave estrangeira (FK) com base no mapeamento 'fk'
            fk_map = cfg.get('fk', {})
            for fk_col, src_table in fk_map.items():
                if src_table in generated_ids:
                    loader.add_fixed_column(fk_col, generated_ids[src_table])
                else:
                    logging.warning(f"FK '{fk_col}' aponta para '{src_table}' mas esta ainda não foi processada ou não gerou ID.")

            etl = ETLController(
                configs=configs,
                extractor=extractor,
                transformer=transformer,
                loader=loader,
                checkpoint_path=cfg.get('checkpoint'),
                usar_ultimo_id_data=cfg.get('usar_ultimo_id_data', False),
                id_table=cfg['tabela_bd'],
                id_column=cfg.get('pk_column', 'id'),
                apenas_ultimo=cfg.get('apenas_ultimo', False),
                coluna_ordenacao=cfg.get('coluna_ordenacao')
            )

            for col, val in cfg.get('fixed_columns', {}).items():
                loader.add_fixed_column(col, val)

            etl.run()

            # Capturar último ID gerado (apenas se a tabela for pai e tiver sequence)
            if cfg.get('usar_ultimo_id_data', False):
                pk_expr = cfg.get('pk_expression')
                if pk_expr and pk_expr.startswith("nextval('") and pk_expr.endswith("')"):
                    seq_name = pk_expr[9:-2]
                else:
                    raise ValueError(f"pk_expression inválida ou ausente para tabela {nome_tabela}")

                with engine.connect() as conn:
                    result = conn.execute(text(f"SELECT currval('{seq_name}')"))
                    last_id = result.scalar()
                generated_ids[nome_tabela] = last_id
                logging.info(f"Último ID gerado para {nome_tabela}: {last_id}")

        except Exception as e:
            logging.error(f"Erro ao processar tabela {nome_tabela}: {e}", exc_info=True)

if __name__ == "__main__":
    main()