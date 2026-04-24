#-----------------------------------------------------------------------------------------------------------#
# Este programa executa o processo de pesquisar notícias, utilizando a API do NewsAPI.
# Apresenta uma interface gráfica para o usuário, onde ele pode escolher a categoria de notícias que deseja.
#-----------------------------------------------------------------------------------------------------------#
import tkinter as tk
from tkinter import messagebox
import webbrowser
import requests
import os
from typing import List, Dict

# ======================== CONFIGURAÇÃO DA API ========================
NEWSAPI_KEY = "9cfb289f91834653a0ebd34917415c25"   # Sua chave real
NEWSAPI_URL = "https://newsapi.org/v2/everything"

#========================================= Definição das categorias ==========================================#
MP1 = [
    "PVC", "PE", "policloreto de vinila", "polietileno",
    "PEBD", "PEAD", "resina PVC", "preço PVC", "mercado de PVC"
]

MP2 = [
    "óleo de soja", "soybean oil", "farelo de soja",
    "soja", "CBOT soja", "Chicago soja", "prêmio soja"
]

GLOBAL = [
    "mercado global", "global market", "economia mundial",
    "world economy", "crise global", "commodities globais",
    "índices globais", "bolsas mundiais", "bolsas de valores",
    "stock exchange", "commodities", "guerra comercial",
    "trade war", "petróleo", "oil", "dólar", "dollar",
    "antidumping", "tarifas internacionais", "tarifas globais"
]

CATEGORIAS = {
    "MP - PVC/PE": MP1,
    "MP - Óleo de soja": MP2,
    "Global - Mercado global": GLOBAL
}

#======================================== Função de obtenção de notícias (real) ================================#
def obter_noticias(palavras_chave: List[str]) -> List[Dict[str, str]]:
    if NEWSAPI_KEY == "SUA_CHAVE_AQUI":
        raise ValueError("Defina sua chave de API do NewsAPI.")
    
    query = " OR ".join(palavras_chave)
    parametros = {
        "q": query,
        "apiKey": NEWSAPI_KEY,
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": 20
    }
    headers = {"User-Agent": "NewsFilterApp/1.0 (seuemail@exemplo.com)"}

    try:
        resposta = requests.get(NEWSAPI_URL, params=parametros, headers=headers, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()

        if dados["status"] != "ok":
            print("Erro na API:", dados.get("message", "Erro desconhecido"))
            return []

        artigos = dados.get("articles", [])
        resultado = []
        for artigo in artigos:
            titulo, link = artigo.get("title"), artigo.get("url")
            if titulo and link:
                resultado.append({"titulo": titulo, "link": link})
        return resultado

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []

# ===================== INTERFACE GRÁFICA PRINCIPAL =====================
class Aplicacao:
    # Paleta de cores escuras
    DARK_BG = "#1e1e1e"
    DARKER_BG = "#252525"
    TEXT_COLOR = "#dcdcdc"
    LINK_COLOR = "#4da6ff"        # azul claro
    VISITED_COLOR = "#666666"     # cinza escuro
    BUTTON_BG = "#3c3c3c"
    GREEN_BUTTON_BG = "#2e7d32"
    RADIO_BG = "#2d2d2d"
    TEXT_AREA_BG = "#2d2d2d"

    def __init__(self, root):
        self.root = root
        self.root.title("Filtro de Notícias por Categoria")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        self.root.configure(bg=self.DARK_BG)

        # ----- Frame de seleção (topo) -----
        frame_selecao = tk.Frame(root, bg=self.DARK_BG, pady=10)
        frame_selecao.pack(fill="x")

        titulo = tk.Label(
            frame_selecao,
            text="Selecione a categoria:",
            font=("Arial", 12, "bold"),
            bg=self.DARK_BG,
            fg=self.TEXT_COLOR
        )
        titulo.pack()

        self.categoria_selecionada = tk.StringVar(value="MP - PVC/PE")

        frame_radios = tk.Frame(frame_selecao, bg=self.DARK_BG)
        frame_radios.pack(pady=5)

        for i, nome in enumerate(CATEGORIAS.keys()):
            rb = tk.Radiobutton(
                frame_radios,
                text=nome,
                variable=self.categoria_selecionada,
                value=nome,
                font=("Arial", 10),
                bg=self.RADIO_BG,
                fg=self.TEXT_COLOR,
                activebackground=self.DARKER_BG,
                activeforeground=self.TEXT_COLOR,
                selectcolor=self.DARK_BG,
                relief="flat"
            )
            rb.grid(row=0, column=i, padx=10)

        tk.Button(
            frame_selecao,
            text="🔍 Buscar Notícias",
            font=("Arial", 11, "bold"),
            bg=self.GREEN_BUTTON_BG,
            fg="white",
            activebackground="#1b5e20",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=3,
            command=self.buscar_noticias
        ).pack(pady=15)

        # ----- Separador -----
        separador = tk.Frame(root, height=2, bg="#555555")
        separador.pack(fill="x", padx=10)

        # ----- Frame de resultados -----
        frame_resultados = tk.Frame(root, bg=self.DARK_BG)
        frame_resultados.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(
            frame_resultados,
            text="Resultados:",
            font=("Arial", 11, "bold"),
            bg=self.DARK_BG,
            fg=self.TEXT_COLOR
        ).pack(anchor="w")

        self.texto_resultado = tk.Text(
            frame_resultados,
            wrap="word",
            cursor="hand2",
            font=("Arial", 11),
            relief="flat",
            borderwidth=0,
            padx=8,
            pady=8,
            state="disabled",
            bg=self.TEXT_AREA_BG,
            fg=self.TEXT_COLOR,
            insertbackground="white",   # cursor
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(frame_resultados, command=self.texto_resultado.yview)
        self.texto_resultado.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.texto_resultado.pack(side="left", fill="both", expand=True)

        # Tags para links e visitados
        self.texto_resultado.tag_configure("link", foreground=self.LINK_COLOR, underline=False)
        self.texto_resultado.tag_configure("visited", foreground=self.VISITED_COLOR, underline=False)
        # A tag "visited" terá prioridade sobre "link" quando ambas existirem
        self.texto_resultado.tag_raise("visited", "link")

    def abrir_link(self, url, inicio, fim):
        """Abre o link no navegador e marca a linha como visitada."""
        webbrowser.open(url)
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.tag_add("visited", inicio, fim)
        self.texto_resultado.configure(state="disabled")

    def buscar_noticias(self):
        """Realiza a filtragem e exibe os resultados no campo de texto."""
        categoria = self.categoria_selecionada.get()
        palavras = CATEGORIAS[categoria]

        # Feedback de busca
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("end", "Buscando notícias...\n")
        self.texto_resultado.configure(state="disabled")
        self.root.update()

        noticias = obter_noticias(palavras)

        # Exibe os resultados
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", "end")

        self.texto_resultado.insert("end", f"Categoria: {categoria}\n\n")
        if not noticias:
            self.texto_resultado.insert("end", "Nenhuma notícia encontrada ou erro na API.")
        else:
            for i, n in enumerate(noticias, 1):
                linha = f"{i}. {n['titulo']}\n"
                inicio = self.texto_resultado.index("end-1c")
                self.texto_resultado.insert("end", linha)
                fim = self.texto_resultado.index("end-1c")
                self.texto_resultado.tag_add("link", inicio, fim)
                # Vincula o clique à função abrir_link com os parâmetros necessários
                self.texto_resultado.tag_bind(
                    "link",
                    "<Button-1>",
                    lambda e, url=n['link'], ini=inicio, fi=fim: self.abrir_link(url, ini, fi)
                )

        self.texto_resultado.configure(state="disabled")
        print(f"{len(noticias)} notícia(s) encontrada(s) para '{categoria}'.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()