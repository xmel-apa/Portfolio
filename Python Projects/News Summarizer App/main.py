# ------------------------------------------------------#
# Data de criação: 2024-06-20
# Autor: Pamela Almeida
# email: pamela.almeidasp@gmail.com
# GitHub: xmel-apa
# linkedin: pamela-almeida-7b6695320
# -------------------------------------------------------#

import tkinter as tk
from tkinter import messagebox
import webbrowser
import requests
import threading
import urllib.parse
from typing import List, Dict
from summarizer import resumir
from bs4 import BeautifulSoup
from sentimentAnalizer import analisar_sentimento

# -- Configuração da API de notícias --
NEWSAPI_KEY = "9cfb289f91834653a0ebd34917415c25"
NEWSAPI_URL = "https://newsapi.org/v2/everything"

CATEGORIAS = {
    "MP - PVC/PE": {
        "base": '("PVC" OR "PE" OR "polietileno" OR "plastic resin" OR "polychloride" OR "polyethylene")',
        "mercado": ["price", "market", "quotation", "demand", "petrochemical", "supply",
                    "production", "consumption", "import", "export"],
        "domains": "icis.com,globo.com,estadao.com.br,folha.uol.com.br,plasticomoderno.com.br,plasticoindustrial.com.br,plastshow.com.br,abiplast.org.br,petroquimica.com.br,plasticsnews.com,plasticsnewseurope.com,pvc.org,icis.com,chemorbis.com,spglobal.com"
    },
    "MP - Óleo de soja": {
        "base": '("soybean" OR "soybean oil" OR "soy meal" OR "CBOT" OR "Chicago Board of Trade" OR "soja" OR "óleo de soja" OR "farelo de soja")',
        "mercado": ["price", "quotation", "market", "demand", "export", "harvest", "production",
                    "consumption", "import", "weather", "crop", "CBOT"],
        "domains": "icis.com,globo.com,estadao.com.br,folha.uol.com.br,canalrural.com.br,noticiasagricolas.com.br,revistagloborural.globo.com,agenciabrasil.ebc.com.br,embrapa.br,cepea.esalq.usp.br,reuters.com,bloomberg.com,farmfutures.com,dtnpf.com,agriculture.com,www.oilworld.biz"
    },
    "Global - Mercado global": {
        "base": '("global market" OR "world economy" OR "commodities" OR "inflation" OR "trade war" OR "Trump" OR "interest rate")',
        "mercado": ["price", "stock", "index", "dollar", "commodity", "oil", "gold", "currency",
                    "exchange rate", "tariff", "trade", "economy", "growth", "recession"],
        "domains": "icis.com,globo.com,estadao.com.br,folha.uol.com.br,cnnbrasil.com.br,thedailybeast.com,terra.com.br,agenciabrasil.ebc.com.br,einvestidor.estadao.com.br,reuters.com,cnbc.com,marketwatch.com,investing.com,bloomberg.com,imf.org,newyorktimes.com,ft.com,wsj.com,bbc.com,worldometers.info"
    }
}

# --- Função para extrair texto completo de uma notícia via scraping ---
def extrair_texto_noticia(url: str) -> str:
    """
    Tenta extrair o texto principal da notícia a partir da URL.
    Retorna o texto concatenado dos parágrafos ou '' se falhar.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; NewsFilterApp/2.0)"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "lxml")

        artigo = soup.find("article")
        if not artigo:
            paragrafos = soup.find_all("p")
        else:
            paragrafos = artigo.find_all("p")

        texto = " ".join(p.get_text(strip=True) for p in paragrafos if len(p.get_text(strip=True)) > 40)
        return texto if texto else ""
    except Exception:
        return ""

# --- Função que obtém as notícias da API ---
def obter_noticias(categoria_nome: str) -> List[Dict[str, str]]:
    info = CATEGORIAS[categoria_nome]
    termos_base = info["base"]
    termos_mercado = " OR ".join(info["mercado"])
    query = f"({termos_base}) ({termos_mercado})"

    parametros = {
        "q": query,
        "apiKey": NEWSAPI_KEY,
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "domains": info["domains"]
    }
    headers = {"User-Agent": "NewsFilterApp/1.0"}

    try:
        resp = requests.get(NEWSAPI_URL, params=parametros, headers=headers, timeout=10)
        resp.raise_for_status()
        dados = resp.json()
        artigos = dados.get("articles", [])
        resultado = []
        for artigo in artigos:
            titulo = artigo.get("title")
            link = artigo.get("url")
            descricao = artigo.get("description") or ""
            data_iso = artigo.get("publishedAt") or ""
            if titulo and link and "valor.globo.com" not in link:
                resultado.append({
                    "titulo": titulo,
                    "link": link,
                    "descricao": descricao,
                    "data": data_iso,
                    "texto_completo": ""
                })
        return resultado
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
    BLUE_BUTTON_BG = "#1565c0"
    RADIO_BG = "#2d2d2d"
    TEXT_AREA_BG = "#2d2d2d"

    def __init__(self, root):
        self.root = root
        self.root.title("News Summarizer App")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        self.root.configure(bg=self.DARK_BG)

        # Armazena informações dos blocos: idx -> (inicio_index_str, link, numero, data_formatada, titulo)
        self.marcas_resumo = {}

        # --- Frame de seleção ---
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

        # --- Frame de botões (horizontal) ---
        frame_botoes = tk.Frame(frame_selecao, bg=self.DARK_BG)
        frame_botoes.pack(fill="x", pady=10, padx=10)

        # Botão "Abrir no E‑mail" (esquerda)
        tk.Button(
            frame_botoes, text="📬 Eniar por E-mail", font=("Arial", 11, "bold"),
            bg=self.BLUE_BUTTON_BG, fg="white", activebackground="#0d47a1",
            activeforeground="white", relief="flat", bd=0, padx=10, pady=3,
            command=self.abrir_no_email_cliente
        ).pack(side="left")

        # Botão "Buscar Notícias" (direita)
        tk.Button(
            frame_botoes, text="🔍 Buscar Notícias", font=("Arial", 11, "bold"),
            bg=self.GREEN_BUTTON_BG, fg="white", activebackground="#1b5e20",
            activeforeground="white", relief="flat", bd=0, padx=10, pady=3,
            command=self.buscar_noticias
        ).pack(side="right")

        # Separador
        tk.Frame(root, height=2, bg="#555555").pack(fill="x", padx=10)

        # --- Frame de resultados ---
        frame_resultados = tk.Frame(root, bg=self.DARK_BG)
        frame_resultados.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame_resultados, text="Resultados:", font=("Arial", 11, "bold"),
                 bg=self.DARK_BG, fg=self.TEXT_COLOR).pack(anchor="w")

        self.texto_resultado = tk.Text(
            frame_resultados, wrap="word", font=("Arial", 11),
            relief="flat", borderwidth=0, padx=8, pady=8, state="disabled",
            bg=self.TEXT_AREA_BG, fg=self.TEXT_COLOR, insertbackground="white",
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(frame_resultados, command=self.texto_resultado.yview)
        self.texto_resultado.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.texto_resultado.pack(side="left", fill="both", expand=True)

        # Configuração de tags
        self.texto_resultado.tag_configure("link", foreground=self.LINK_COLOR, underline=False)
        self.texto_resultado.tag_configure("visited", foreground=self.VISITED_COLOR, underline=False)
        self.texto_resultado.tag_configure("resumo", foreground=self.TEXT_COLOR)

        self.texto_resultado.bind("<Motion>", self._on_mouse_move)
        self.texto_resultado.bind("<Leave>", self._on_mouse_leave)

    def _on_mouse_move(self, event):
        index = self.texto_resultado.index(f"@{event.x},{event.y}")
        tags = self.texto_resultado.tag_names(index)
        # Qualquer tag que comece com "link" (inclui as individuais)
        if any(tag.startswith("link") for tag in tags):
            self.texto_resultado.configure(cursor="hand2")
        else:
            self.texto_resultado.configure(cursor="xterm")

    def _on_mouse_leave(self, event):
        self.texto_resultado.configure(cursor="xterm")

    def abrir_link(self, url, inicio, fim):
        webbrowser.open(url)
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.tag_add("visited", inicio, fim)
        self.texto_resultado.configure(state="disabled")

    def formatar_data(self, data_iso):
        if not data_iso:
            return "Data não disponível"
        try:
            from datetime import datetime
            data_iso = data_iso.replace("Z", "+00:00")
            dt = datetime.fromisoformat(data_iso)
            return dt.strftime("%d/%m/%Y %H:%M")
        except:
            return data_iso

    def buscar_noticias(self):
        """Realiza a busca de notícias e inicia o processamento em background."""
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
            self.texto_resultado.configure(state="disabled")
            return

        # Limpa dados anteriores
        self.marcas_resumo.clear()

        for i, n in enumerate(noticias, 1):
            data_formatada = self.formatar_data(n.get('data'))
            titulo = n['titulo']
            link = n['link']

            # Bloco placeholder
            bloco = (
                f"{i}. {titulo}  [{data_formatada}]\n"
                f"   ⏳ Gerando resumo...\n\n"
            )

            inicio_index_str = self.texto_resultado.index("end-1c")
            self.texto_resultado.insert("end", bloco)
            fim_index_str = self.texto_resultado.index("end-1c")

            # Marcas temporárias para substituição posterior
            self.texto_resultado.mark_set(f"bloco_start_{i}", inicio_index_str)
            self.texto_resultado.mark_set(f"bloco_end_{i}", fim_index_str)

            # Armazena dados para reconstruir o bloco final
            self.marcas_resumo[i-1] = (inicio_index_str, link, i, data_formatada, titulo)

        self.texto_resultado.configure(state="disabled")
        print(f"{len(noticias)} notícia(s) encontrada(s) para '{categoria}'.")

        # Inicia thread para resumo e sentimento
        thread = threading.Thread(target=self._processar_resumos, args=(noticias,))
        thread.daemon = True
        thread.start()

    def _processar_resumos(self, noticias):
        """Em segundo plano, extrai texto, resume e analisa sentimento."""
        for idx, noticia in enumerate(noticias):
            texto_completo = extrair_texto_noticia(noticia['link'])

            # Define o texto a ser analisado
            if texto_completo and len(texto_completo) > len(noticia.get('descricao', '')):
                texto_analise = noticia['titulo'] + ". " + texto_completo
            else:
                texto_analise = noticia['titulo']
                if noticia.get('descricao'):
                    texto_analise += ". " + noticia['descricao']

            # Análise de sentimento
            try:
                sentimento = analisar_sentimento(texto_analise[:2000])
            except Exception:
                sentimento = {
                    "classificacao": "ERRO",
                    "emoji": "⚠️",
                    "score_compound": 0.0,
                    "scores": {}
                }

            # Resumo
            try:
                resumo = resumir(texto_analise[:2000])
            except Exception as e:
                resumo = f"Erro ao resumir: {e}"

            # Atualiza a interface
            self.root.after(0, self._exibir_resumo, idx, resumo, sentimento)

    def _exibir_resumo(self, idx, resumo_texto, sentimento_info):
        """Substitui o placeholder pelo título + sentimento + resumo, mantendo o título clicável."""
        try:
            inicio_str, link, numero, data_formatada, titulo = self.marcas_resumo[idx]
        except KeyError:
            return

        self.texto_resultado.configure(state="normal")

        # Remove bloco placeholder
        marca_start = f"bloco_start_{idx+1}"
        marca_end = f"bloco_end_{idx+1}"
        self.texto_resultado.delete(marca_start, marca_end)

        # Novo bloco com dados processados
        texto_final = (
            f"{numero}. {titulo}  [{data_formatada}]\n"
            f"   📊 Sentimento: {sentimento_info['emoji']} {sentimento_info['classificacao']} "
            f"(Score: {sentimento_info['score_compound']:.2f})\n"
            f"   📄 Resumo: {resumo_texto}\n\n"
        )

        self.texto_resultado.insert(inicio_str, texto_final)

        # Torna o título clicável
        fim_titulo = self.texto_resultado.index(f"{inicio_str} lineend")
        tag_link = f"link_noticia_{idx}"
        self.texto_resultado.tag_configure(tag_link, foreground=self.LINK_COLOR, underline=False)
        self.texto_resultado.tag_add(tag_link, inicio_str, fim_titulo)
        self.texto_resultado.tag_bind(
            tag_link,
            "<Button-1>",
            lambda e, url=link, ini=inicio_str, fi=fim_titulo: self.abrir_link(url, ini, fi)
        )

        # Aplica tag 'resumo' às linhas de dados (opcional)
        self.texto_resultado.tag_add("resumo", f"{inicio_str} + 1 line", f"{inicio_str} + 3 lines")

        self.texto_resultado.configure(state="disabled")

    def abrir_no_email_cliente(self):
        """Abre o cliente de e-mail padrão com os resumos prontos para envio."""
        conteudo = self.texto_resultado.get("1.0", "end-1c")
        if not conteudo.strip() or "Buscando notícias..." in conteudo:
            messagebox.showwarning("Sem conteúdo", "Execute uma busca antes de abrir o e-mail.")
            return

        categoria = self.categoria_selecionada.get()
        assunto = f"Resumos de Notícias - {categoria}"

        # Cria a URL mailto: com assunto e corpo
        mailto_url = (
            f"mailto:?"
            f"subject={urllib.parse.quote(assunto)}"
            f"&body={urllib.parse.quote(conteudo)}"
        )
        webbrowser.open(mailto_url)

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("app_icon.ico")
    app = Aplicacao(root)
    root.mainloop()