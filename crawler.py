import requests
from bs4 import BeautifulSoup
import json
import signal
import sys
from urllib.parse import urljoin, urlparse
import nltk
from nltk.tokenize import sent_tokenize
import logging
import time
import random

nltk.download('punkt', quiet=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebCrawler:
    def __init__(self, start_url, max_pages=100):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.to_visit = [start_url]
        self.domain = urlparse(start_url).netloc
        self.processed_data = []
        signal.signal(signal.SIGINT, self.signal_handler)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        ]

    def get_random_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def crawl(self):
        while self.to_visit and len(self.visited_urls) < self.max_pages:
            url = self.to_visit.pop(0)
            if url not in self.visited_urls and self.domain in url:
                try:
                    logging.info(f"Crawling: {url}")
                    self.visited_urls.add(url)
                    headers = self.get_random_headers()
                    response = requests.get(url, timeout=10, headers=headers)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    self.extract_info(url, soup)
                    self.find_links(soup, url)
                    time.sleep(random.uniform(1, 3))  # Random delay between requests
                except requests.RequestException as e:
                    logging.error(f"Error fetching {url}: {str(e)}")
                except Exception as e:
                    logging.error(f"Unexpected error processing {url}: {str(e)}")

    def extract_info(self, url, soup):
        try:
            title = soup.title.string if soup.title else "No Title"
            text_content = self.clean_html(soup)
            if text_content:
                self.process_content(url, title, text_content)
            else:
                logging.warning(f"No content extracted from {url}")
        except Exception as e:
            logging.error(f"Error extracting info from {url}: {str(e)}")

    def clean_html(self, soup):
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        text = soup.get_text(separator='\n', strip=True)
        return text if len(text) > 100 else ""  # Ignore very short or empty content

    def process_content(self, url, title, content):
        chunks = self.create_chunks(content)
        for i, chunk in enumerate(chunks):
            self.processed_data.append({
                "title": f"{title} - Part {i+1}",
                "content": chunk
            })
        logging.info(f"Processed {len(chunks)} chunks from {url}")

    def create_chunks(self, text, max_tokens=500):
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_tokens = len(sentence.split())
            if current_length + sentence_tokens > max_tokens:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_tokens
            else:
                current_chunk.append(sentence)
                current_length += sentence_tokens
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def find_links(self, soup, base_url):
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            if full_url not in self.visited_urls and full_url not in self.to_visit and self.domain in full_url:
                self.to_visit.append(full_url)

    def save_data(self):
        if not self.processed_data:
            logging.warning("No data to save. The crawler didn't extract any content.")
            return

        with open('crawler_results.jsonl', 'w', encoding='utf-8') as f:
            for item in self.processed_data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')
        logging.info(f"Saved {len(self.processed_data)} items to crawler_results.jsonl")

    def signal_handler(self, sig, frame):
        logging.info("Process interrupted by user. Saving data...")
        self.save_data()
        sys.exit(0)

if __name__ == "__main__":
    start_url = input("Digite a URL inicial para o crawler: ")
    crawler = WebCrawler(start_url)
    logging.info("Iniciando o crawler. Pressione Ctrl+C a qualquer momento para encerrar e salvar os dados.")
    crawler.crawl()
    crawler.save_data()
    logging.info(f"Crawling concluído. {len(crawler.processed_data)} chunks criados.")