import requests
import os
from datetime import datetime, timedelta
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import feedparser
from dotenv import load_dotenv
import re
import time
import schedule

# Configuração inicial
load_dotenv()

class AdvancedPVCNewsMonitor:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.pvc_keywords = [
            "PVC", 
            "policloreto de vinila",
            "polyvinyl chloride",
            "resina PVC",
            "composto PVC",
            "mercado PVC",
            "preço PVC",
            "tubos PVC",
            "conexões PVC",
            "polietilenos",
            "polímeros",
            "plásticos",
            "indústria de PVC",
            "setor de PVC",
            "antidumping PVC",
            "atidumping polímeros",
            "antidunping 39011030",
            "antidumping 39014000",
            "GECEX CAMEX antidumping PVC",
            "GECEX CAMEX antidumping policloreto de vinila",
            "GECEX CAMEX antidumping polímeros",
            "GECEX CAMEX antidumping plásticos",
            "GECEX CAMEX antidumping resina PVC",
            "GECEX CAMEX antidumping polietilenos",
            "GECEX CAMEX antidumping composto PVC",
            "polietileno",
            "Unipar",
            "Braskem",
            "Petroquímico"
        ]
        self.exclude_terms = [
            "futebol", "esporte", "música", 
            "celebridade", "entretenimento"
        ]
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
    
    def build_search_query(self):
        """Constroi query de busca avançada"""
        include = " OR ".join(f'"{kw}"' for kw in self.pvc_keywords)
        exclude = " ".join(f'-{term}' for term in self.exclude_terms)
        return f"({include}) {exclude}"
    
    def search_newsapi(self):
        """Busca usando NewsAPI com filtros avançados"""
        api_key = os.getenv('NEWSAPI_KEY')
        if not api_key:
            return []
        
        query = self.build_search_query()
        first_day_of_month = datetime(self.current_year, self.current_month, 1).strftime('%Y-%m-%d')
        
        params = {
            'q': query,
            'from': first_day_of_month,
            'language': 'pt',
            'sortBy': 'relevancy',
            'pageSize': 30,
            'apiKey': api_key,
           # 'domains': 'valor.com.br'
        }
        
        try:
            response = requests.get(
                "https://newsapi.org/v2/everything",
                params=params,
                timeout=15
            )
            response.raise_for_status()
            return response.json().get('articles', [])
        except Exception as e:
            print(f"Erro NewsAPI: {e}")
            return []
    
    def search_industry_sites(self):
        """Busca direta em sites especializados"""
        sites = {
            "Canal Plástico": "https://www.canalplastico.com.br/search/=PVC",
            "Revista Plástico Sul": "https://www.plasticosul.com.br/?s=PVC",
            "ABIQUIM": "https://abiquim.org.br/?s=PVC",
            "Valor Econômico": "https://valor.globo.com/busca/?q=PVC",
            "Plástico Moderno": "https://plasticomoderno.com.br/?s=PVC",
            "Plástico em Revista": "https://plasticosemrevista.com.br/?s=PVC",
            "Plástico Brasil": "https://plasticobrasil.com.br/?s=",
            "Plástico News": "https://plasticonews.com.br/?s=PVC",
            "Plástico Hoje": "https://plasticohoy.com.br/?s=PVC",
            "Gov": "https://www.gov.br/pt-br/busca?q=PVC+antidumping",
            "ICIS": "https://www.icis.com/explore/search/?q=pvc",
            "Google News": "https://news.google.com/rss/search?q=brankem+OR+unipar+OR+pvc+OR+policloreto+de+vinila+OR+polyvinyl+chloride&hl=pt-BR&gl=BR&ceid=BR:pt-419",
            "Valor Econômico (Braskem)": "https://valor.globo.com/busca/?q=Braskem",
            "Reuters Brasil": "https://www.reuters.com/search/news?blob=Braskem",
            "Notícias Petroquímicas": "https://www.noticiaspetroquimicas.com.br/?s=Braskem",
            "Valor Econômico (Unipar)": "https://valor.globo.com/busca/?q=Unipar",
            "valor economico (Braskem)": "https://valor.globo.com/busca/?q=Braskem",
            "Folha de S.Paulo": "https://www1.folha.uol.com.br/busca/?q=Braskem+OR+Unipar+OR+PVC+OR+policloreto+de+vinila+OR+polyvinyl+chloride",
            "Brasil energia": "https://www.brasilenergia.com.br/busca?q=Braskem+OR+Unipar+OR+PVC+OR+policloreto+de+vinila+OR+polyvinyl+chloride",
            "Terra": "https://www.terra.com.br/busca/?q=Braskem+OR+Unipar+OR+PVC+OR+policloreto+de+vinila+OR+polyvinyl+chloride",
            "UOL Economia": "https://economia.uol.com.br/busca/?q=Braskem+OR+Unipar+OR+PVC+OR+policloreto+de+vinila+OR+polyvinyl+chloride",
            "G1 Economia": "https://g1.globo.com/busca/?q=Braskem+OR+Unipar+OR+PVC+OR+policloreto+de+vinila+OR+polyvinyl+chloride",
            "Exame": "https://exame.com/busca/?q=Braskem+OR+Unipar+OR+PVC+OR+policloreto+de+vinila+OR+polyvinyl+chloride",
            "Jornal do Commercio": "https://jc.ne10.uol.com.br  /busca/?q=Braskem+OR+Unipar+OR+PVC+OR+policloreto+de+vinila+OR+polyvinyl+chloride",
            "Jornal do Brasil": "https://www.jb.com.br/busca/?q=Braskem+OR+Unipar+OR+PVC+OR+policloreto+de+vinila+OR+polyvinyl+chloride",
            "O Globo": "https://oglobo.globo.com/busca/?q=Braskem+OR+Unipar+OR+PVC+OR+policloreto+de+vinila+OR+polyvinyl+chloride"
            

    }
        
        results = []
        
        for site_name, url in sites.items():
            try:
                headers = {'User-Agent': self.user_agent}
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Adaptar conforme a estrutura de cada site
                articles = soup.find_all('article', limit=5)
                
                for article in articles:
                    title = article.find('h2').get_text(strip=True) if article.find('h2') else "Sem título"
                    link = article.find('a')['href'] if article.find('a') else "#"
                    date_element = article.find('time')  # Procura por elemento de data
                    
                    # Verifica se é realmente sobre PVC
                    if any(re.search(rf'\b{kw}\b'.lower(), title.lower()) for kw in self.pvc_keywords):
                        # Tenta obter a data da notícia
                        published_at = datetime.now().isoformat()
                        if date_element and 'datetime' in date_element.attrs:
                            try:
                                article_date = datetime.strptime(date_element['datetime'], '%Y-%m-%d')
                                if article_date.month == self.current_month and article_date.year == self.current_year:
                                    published_at = article_date.isoformat()
                                else:
                                    continue  # Pula notícias de outros meses
                            except ValueError:
                                pass
                        
                        results.append({
                            'title': title,
                            'url': link,
                            'source': {'name': site_name},
                            'publishedAt': published_at
                        })
                        
            except Exception as e:
                print(f"Erro ao buscar {site_name}: {e}")
        
        return results
    
    def search_google_news(self):
        """Busca alternativa no Google News"""
        try:
            query = quote_plus(" OR ".join(self.pvc_keywords))
            first_day_of_month = datetime(self.current_year, self.current_month, 1).strftime('%Y-%m-%d')
            url = f"https://news.google.com/rss/search?q={query}+OR+Braskem+after:{first_day_of_month}&hl=pt-BR"
            
            feed = feedparser.parse(url)
            results = []
            
            for entry in feed.entries[:15]:
                if any(kw.lower() in entry.title.lower() for kw in self.pvc_keywords):
                    # Verifica se a data da notícia é do mês atual
                    if hasattr(entry, 'published_parsed'):
                        pub_date = datetime(*entry.published_parsed[:6])
                        if pub_date.month == self.current_month and pub_date.year == self.current_year:
                            results.append({
                                'title': entry.title,
                                'url': entry.link,
                                'source': {'name': entry.source.title if hasattr(entry, 'source') else "Google News"},
                                'publishedAt': entry.published
                            })
            
            return results
        except Exception as e:
            print(f"Erro Google News RSS: {e}")
            return []
    
    def filter_relevant_news(self, news_items):
        """Filtra notícias por relevância e data"""
        filtered = []
        
        for item in news_items:
            title = item.get('title', '').lower()
            content = item.get('description', '').lower()
            
            # Verifica termos-chave no título ou conteúdo
            title_matches = sum(kw.lower() in title for kw in self.pvc_keywords)
            content_matches = sum(kw.lower() in content for kw in self.pvc_keywords)
            
            # Verifica termos a excluir
            has_excluded = any(term in title or term in content for term in self.exclude_terms)
            
            # Pontuação de relevância
            relevance_score = title_matches * 2 + content_matches
            
            # Verifica se a data é do mês atual
            is_current_month = True
            if 'publishedAt' in item:
                try:
                    pub_date = datetime.strptime(item['publishedAt'][:10], '%Y-%m-%d')
                    if pub_date.month != self.current_month or pub_date.year != self.current_year:
                        is_current_month = False
                except (ValueError, TypeError):
                    pass
            
            if relevance_score >= 2 and not has_excluded and is_current_month:
                item['relevance'] = relevance_score
                filtered.append(item)
        
        # Ordena por relevância e data
        return sorted(filtered, key=lambda x: (-x['relevance'], x.get('publishedAt', '')))
    
    def get_pvc_news(self):
        """Obtém todas as notícias relevantes sobre PVC"""
        print(f"Coletando notícias sobre PVC do mês {self.current_month}/{self.current_year}...")
        
        # Múltiplas fontes
        sources = [
            self.search_newsapi(),
            self.search_industry_sites(),
            self.search_google_news()
        ]
        
        # Consolida e filtra
        all_news = [item for sublist in sources for item in sublist]
        relevant_news = self.filter_relevant_news(all_news)
        
        # Remove duplicatas
        unique_news = {}
        for item in relevant_news:
            url = item.get('url')
            if url and url not in unique_news:
                unique_news[url] = item
        
        return list(unique_news.values())
    
    def display_news(self, news_items):
        """Exibe as notícias de forma organizada"""
        if not news_items:
            print(f"\nNenhuma notícia relevante encontrada no mês {self.current_month}/{self.current_year}.")
            return
        
        print(f"\n=== NOTÍCIAS SOBRE PVC DO MÊS {self.current_month}/{self.current_year} ({len(news_items)} resultados) ===")
        print(f"Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for idx, item in enumerate(news_items[:20], 1):  # Limita a 15 melhores
            print(f"\n{idx}. {item['title']}")
            print(f"   🔍 Relevância: {item.get('relevance', 0)}")
            print(f"   📅 Data: {item.get('publishedAt', 'Não disponível')}")
            print(f"   📰 Fonte: {item.get('source', {}).get('name', 'Desconhecida')}")
            print(f"   🌐 Link: {item.get('url', '#')}")

def run_monitor():
    """Função para executar o monitor e exibir as notícias"""
    monitor = AdvancedPVCNewsMonitor()
    pvc_news = monitor.get_pvc_news()
    monitor.display_news(pvc_news)
    print("\nPróxima atualização em 30 minutos...\n")

# Execução principal com agendamento
if __name__ == "__main__":
    # Executa imediatamente na primeira vez
    run_monitor()
    
    # Agenda a execução a cada 30 minutos
    schedule.every(30).minutes.do(run_monitor)
    
    # Loop para manter o programa rodando
    while True:
        schedule.run_pending()
        time.sleep(1)