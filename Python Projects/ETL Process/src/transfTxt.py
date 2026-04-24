# import pandas as pd
# from sqlalchemy import create_engine
# from dotenv import load_dotenv, find_dotenv
# import os 
# from urllib.parse import quote_plus  

# #Find dotenv file
# print("Current working directory:", os.getcwd())
# dotenv_path = find_dotenv()
# print("Dotenv file found at:", dotenv_path)
# load_dotenv(r'C:\Users\palmeida\OneDrive - Dacarto\Área de Trabalho\Auto BI\.env')

# # Debug: check variables
# print("DB_HOST =", os.getenv('DB_HOST'))
# print("DB_NAME =", os.getenv('DB_NAME'))
# print("DB_USER =", os.getenv('DB_USER'))
# print("DB_PORT =", os.getenv('DB_PORT'))

# #Define the path to excel file and the path to save the text file
# input_path = r'C:\Users\palmeida\OneDrive - Dacarto\Área de Trabalho\Auto\Auto - planílhas\Cache Exports\Saving\EXPORT.XLSX'
# output_json = r'C:\Users\palmeida\OneDrive - Dacarto\Área de Trabalho\Auto\Auto - planílhas\Cache Exports\Saving\EXPORT.json'

# # Define the sheet name to read 
# sheet_name = 'AAA'

# try:
#     # Read the Excel file
#     df = pd.read_excel(input_path, sheet_name = sheet_name, engine='openpyxl')
#     print(f"Successfully read the excel file: ' {sheet_name} ' with {len(df)}  rows.")

# except Exception as e: 
#     print(f"An error accurred: {e}")

# # Load environment variables from .env file
# DB_HOST = os.getenv('DB_HOST')
# DB_NAME = os.getenv('DB_NAME')
# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD')) 
# DB_PORT = os.getenv('DB_PORT')

# df_temp = pd.read_excel(input_path, sheet_name=sheet_name, nrows=1)
# print(df_temp.columns.tolist())