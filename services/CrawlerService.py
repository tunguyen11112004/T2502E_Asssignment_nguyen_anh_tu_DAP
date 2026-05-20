import requests
from bs4 import BeautifulSoup
import re

class CrawlerService:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    @classmethod
    def fetch_links_from_source(cls, source_url):
        articles = []
        try:
            response = requests.get(source_url, headers=cls.HEADERS, timeout=10)
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                for a_tag in soup.find_all('a', href=True):
                    title = a_tag.get_text().strip()
                    url = a_tag['href']
                    
                    if url.startswith('/'):
                        domain_match = re.match(r'(https?://[^/]+)', source_url)
                        if domain_match:
                            url = domain_match.group(1) + url
                        
                    if len(title) > 20 and (url.endswith('.html') or 'vnexpress.net' in url or 'tuoitre.vn' in url):
                        articles.append({'title': title, 'url': url})
        except Exception as e:
            print(f"⚠️ Lỗi khi crawl link từ {source_url}: {e}")
        return articles

    @classmethod
    def fetch_article_detail(cls, article_url):
        try:
            response = requests.get(article_url, headers=cls.HEADERS, timeout=10)
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                summary_tag = soup.find(class_=['description', 'sapo'])
                content_tag = soup.find(class_=['fck_detail', 'fck-content', 'sidebar-content'])
                
                summary = summary_tag.get_text().strip() if summary_tag else "Không có tóm tắt."
                
                if content_tag:
                    paragraphs = [p.get_text().strip() for p in content_tag.find_all('p')]
                    content = "\n".join(paragraphs)
                else:
                    content = "Không thể bóc tách nội dung chi tiết."
                    
                return summary, content
        except Exception as e:
            print(f"⚠️ Lỗi khi crawl nội dung từ {article_url}: {e}")
        return None, None