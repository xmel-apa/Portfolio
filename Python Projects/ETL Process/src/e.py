# import pandas as pd
# from sqlalchemy import create_engine
# from dotenv import load_dotenv
# import os
# from urllib.parse import quote_plus

# load_dotenv()

# # Paths
# input_path = r'C:\Users\palmeida\OneDrive - Dacarto\Área de Trabalho\Auto\Auto - planílhas\Cache Exports\Saving\EXPORT.XLSX'
# checkpoint_json = r'C:\Users\palmeida\OneDrive - Dacarto\Área de Trabalho\Auto\Auto - planílhas\Cache Exports\Saving\EXPORT.json'
# sheet_name = 'AAA'

# try:
#     colunas = ['ABA']

#     mapeamento_colunas = {
#         'ABA': '1'
#     }

#     # Read current Excel data
#     df_current = pd.read_excel(input_path, sheet_name=sheet_name, usecols=colunas, engine='openpyxl')
#     print(f"Current Excel: {len(df_current)} rows.")

#     # --- Load previous JSON checkpoint if it exists ---
#     if os.path.exists(checkpoint_json):
#         df_previous = pd.read_json(checkpoint_json)
#         print(f"Previous JSON: {len(df_previous)} rows.") 
#     else:
#         df_previous = pd.DataFrame()  # empty DataFrame
#         print("No previous JSON found – will insert all rows.")

#     # --- Identify new rows ---
#     # This works if the entire row must be identical to be considered a duplicate
#     if not df_previous.empty:
#         # Convert to tuples for comparison (avoid index issues)
#         current_tuples = df_current.apply(tuple, axis=1)
#         previous_tuples = df_previous.apply(tuple, axis=1)
#         df_new = df_current[~current_tuples.isin(previous_tuples)]
#     else:
#         df_new = df_current.copy()

#     print(f"New rows to insert: {len(df_new)}")

#     if df_new.empty:
#         print("No new data to insert.")
#     else:
#         # --- Database insertion ---
#         DB_HOST = os.getenv('DB_HOST')
#         DB_NAME = os.getenv('DB_NAME')
#         DB_USER = os.getenv('DB_USER')
#         DB_PASSWORD = os.getenv('DB_PASSWORD')
#         DB_PORT = os.getenv('DB_PORT')

#         DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)
#         engine = create_engine(
#             f'postgresql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
#         )

#         # Insert only new rows
#         df_new.to_sql('teste', con=engine, if_exists='append', index=False)
#         print(f"Inserted {len(df_new)} rows into PostgreSQL.")

#         # --- Update the JSON checkpoint with the full current data (for next run) ---
#         df_current.to_json(checkpoint_json, orient='records', indent=2, force_ascii=False)
#         print("Checkpoint JSON updated.")

# except Exception as e:
#     print(f"Error: {e}")