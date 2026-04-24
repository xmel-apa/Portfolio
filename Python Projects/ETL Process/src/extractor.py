# # Lê as planilhas do Excel e as converte em DataFrames
# # Reads Excel sheets and converts them into DataFrames

import pandas as pd
from pathlib import Path

class Extractor:
    def __init__(self, file_path, sheet_name, usecols=None):
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name
        self.usecols = usecols
        self._data = None  

    def extract(self):
        #-- Metodo que copia os dados da planilha para um DataFrame, e armazena em cache para evitar leituras repetidas
        if self._data is not None:
            return self._data.copy()  # return a copy to avoid modification

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        #-- Validações e Callbacks para a leirtua do excel
        # Optional: validate sheet exists
        try:
            excel = pd.ExcelFile(self.file_path, engine='openpyxl')
            if self.sheet_name not in excel.sheet_names:
                raise ValueError(f"Sheet '{self.sheet_name}' not found in {self.file_path}. Available sheets: {excel.sheet_names}")
        except Exception as e:
            raise RuntimeError(f"Failed to read Excel file: {e}")
        
        # A caso as verificações passarm, faz a leitura efetiva do excel
        try:
            df = pd.read_excel(
                self.file_path,
                sheet_name=self.sheet_name,
                usecols=self.usecols,
                engine='openpyxl'
            )
        except Exception as e:
            raise RuntimeError(f"Error reading sheet '{self.sheet_name}': {e}")
        
        # Retorna o DataFrame e  armazena em cache para futuras chamadas
        self._data = df
        return df.copy()  # return a copy to prevent accidental mutation of cache