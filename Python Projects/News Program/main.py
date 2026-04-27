# ------------------------------------------------------#
# Data de criação: 2024-06-20
# Autor: Pamela Almeida
# email: pamela.almeidasp@gmail.com
# GitHub: xmel-apa
# linkedin: pamela-almeida-7b6695320
# -------------------------------------------------------#


# --- Programa de Filtro de Notícias por Categoria ---

import tkinter as tk
from tkinter import messagebox
import webbrowser
import requests
from typing import List, Dict

# -- Configuração da API de notícias --
NEWSAPI_KEY = "Sua_Chave_Aqui"  # Substitua pela sua chave da NewsAPI
NEWSAPI_URL = "https://newsapi.org/v2/everything"

# -- Escolha e definição das categorias e seus termos de busca em determinadas fontes --
CATEGORIAS = {
    "MP - PVC/PE": {
        "base": "PVC OR PE OR polietileno OR resina plástica",
        "mercado": ["preço", "mercado", "cotação", "demanda", "petroquímica"],
        "domains": "globo.com,estadao.com.br,folha.uol.com.br,plasticomoderno.com.br,plasticoindustrial.com.br,plastshow.com.br,abiplast.org.br,petroquimica.com.br,plasticsnews.com,plasticsnewseurope.com,pvc.org,icis.com,chemorbis.com,spglobal.com"
    },
    "MP - Óleo de soja": {
        "base": "soja OR soybean oil OR farelo soja",
        "mercado": ["preço", "cotação", "mercado", "Chicago", "CBOT"],
        "domains": "globo.com,estadao.com.br,folha.uol.com.br,canalrural.com.br,noticiasagricolas.com.br,revistagloborural.globo.com,agenciabrasil.ebc.com.br,embrapa.br,cepea.esalq.usp.br,reuters.com,bloomberg.com/markets/commodities,farmfutures.com,dtnpf.com,agriculture.com,www.oilworld.biz"
    },
    "Global - Mercado global": {
        "base": "mercado global OR economia mundial OR commodities OR inflação OR juros",
        "mercado": ["preço", "bolsa", "índice", "dólar", "taxa"],
        "domains": "globo.com,estadao.com.br,folha.uol.com.br,cnnbrasil.com.br/business,terra.com.br/economia,agenciabrasil.ebc.com.br/economia,einvestidor.estadao.com.br,reuters.com,www.cnbc.com,marketwatch.com,investing.com,bloomberg.com,imf.org/en/Blogs"
    }
}

# --- Função que obtem as notícias da API ---
def obter_noticias(categoria_nome: str) -> List[Dict[str, str]]:
    # Monta a query de busca combinando os termos base e de mercado
    info = CATEGORIAS[categoria_nome]
    termos_base = info["base"]
    termos_mercado = " OR ".join(info["mercado"])
    query = f"({termos_base}) ({termos_mercado})"
    # Query que inclui os termos base e de mercado
    parametros = {
        "q": query,
        "apiKey": NEWSAPI_KEY,
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "domains": info["domains"]
    }
    headers = {"User-Agent": "NewsFilterApp/1.0"}
    # Realiza a requisição à API e processa os resultados
    try:
        resp = requests.get(NEWSAPI_URL, params=parametros, headers=headers, timeout=10)
        resp.raise_for_status()
        dados = resp.json()
        artigos = dados.get("articles", [])
        resultado = []
        # Filtra os artigos para garantir que tenham título e link
        for artigo in artigos:
            titulo = artigo.get("title")
            link = artigo.get("url")
            if titulo and link and "valor.globo.com" not in link:   
                resultado.append({"titulo": titulo, "link": link})
        return resultado
    # Tratamento de erros de requisição e resposta
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []

# --- Interface ---
class Aplicacao:
    DARK_BG = "#1e1e1e"
    DARKER_BG = "#252525"
    TEXT_COLOR = "#dcdcdc"
    LINK_COLOR = "#4da6ff"
    VISITED_COLOR = "#666666"
    GREEN_BUTTON_BG = "#2e7d32"
    RADIO_BG = "#2d2d2d"
    TEXT_AREA_BG = "#2d2d2d"

    def __init__(self, root):
        self.root = root
        self.root.title("Filtro de Notícias por Categoria")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        self.root.configure(bg=self.DARK_BG)

        frame_selecao = tk.Frame(root, bg=self.DARK_BG, pady=10)
        frame_selecao.pack(fill="x")

        tk.Label(frame_selecao, text="Selecione a categoria:", font=("Arial", 12, "bold"),
                 bg=self.DARK_BG, fg=self.TEXT_COLOR).pack()

        self.categoria_selecionada = tk.StringVar(value="MP - PVC/PE")
        frame_radios = tk.Frame(frame_selecao, bg=self.DARK_BG)
        frame_radios.pack(pady=5)

        for i, nome in enumerate(CATEGORIAS.keys()):
            tk.Radiobutton(
                frame_radios, text=nome, variable=self.categoria_selecionada, value=nome,
                font=("Arial", 10), bg=self.RADIO_BG, fg=self.TEXT_COLOR,
                activebackground=self.DARKER_BG, activeforeground=self.TEXT_COLOR,
                selectcolor=self.DARK_BG, relief="flat"
            ).grid(row=0, column=i, padx=10)

        tk.Button(
            frame_selecao, text="🔍 Buscar Notícias", font=("Arial", 11, "bold"),
            bg=self.GREEN_BUTTON_BG, fg="white", activebackground="#1b5e20",
            activeforeground="white", relief="flat", bd=0, padx=10, pady=3,
            command=self.buscar_noticias
        ).pack(pady=15)

        tk.Frame(root, height=2, bg="#555555").pack(fill="x", padx=10)

        frame_resultados = tk.Frame(root, bg=self.DARK_BG)
        frame_resultados.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame_resultados, text="Resultados:", font=("Arial", 11, "bold"),
                 bg=self.DARK_BG, fg=self.TEXT_COLOR).pack(anchor="w")

        self.texto_resultado = tk.Text(
            frame_resultados, wrap="word", cursor="hand2", font=("Arial", 11),
            relief="flat", borderwidth=0, padx=8, pady=8, state="disabled",
            bg=self.TEXT_AREA_BG, fg=self.TEXT_COLOR, insertbackground="white",
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(frame_resultados, command=self.texto_resultado.yview)
        self.texto_resultado.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.texto_resultado.pack(side="left", fill="both", expand=True)

        self.texto_resultado.tag_configure("link", foreground=self.LINK_COLOR, underline=False)
        self.texto_resultado.tag_configure("visited", foreground=self.VISITED_COLOR, underline=False)
        self.texto_resultado.tag_raise("visited", "link")

    def abrir_link(self, url, inicio, fim):
        webbrowser.open(url)
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.tag_add("visited", inicio, fim)
        self.texto_resultado.configure(state="disabled")

    def buscar_noticias(self):
        categoria = self.categoria_selecionada.get()
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("end", "Buscando notícias...\n")
        self.texto_resultado.configure(state="disabled")
        self.root.update()

        noticias = obter_noticias(categoria)

        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("end", f"Categoria: {categoria}\n\n")

        if not noticias:
            self.texto_resultado.insert("end", "Nenhuma notícia encontrada.")
        else:
            for i, n in enumerate(noticias, 1):
                linha = f"{i}. {n['titulo']}\n"
                inicio = self.texto_resultado.index("end-1c")
                self.texto_resultado.insert("end", linha)
                fim = self.texto_resultado.index("end-1c")
                self.texto_resultado.tag_add("link", inicio, fim)
                self.texto_resultado.tag_bind(
                    "link", "<Button-1>",
                    lambda e, url=n['link'], ini=inicio, fi=fim: self.abrir_link(url, ini, fi)
                )

        self.texto_resultado.configure(state="disabled")
        print(f"{len(noticias)} notícia(s) encontrada(s) para '{categoria}'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()