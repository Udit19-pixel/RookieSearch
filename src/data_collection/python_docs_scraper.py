import urllib.request
import json
import re
from html.parser import HTMLParser
import time
import os

class SimpleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = 0
        self.data = []
        self.current_section = {"title": "", "content": ""}

    def handle_starttag(self, tag, attrs):
        if tag in ['h1', 'h2', 'h3']:
            self.recording = 1

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3']:
            self.recording = 0
            if self.current_section["title"]:
                self.data.append(self.current_section)
            self.current_section = {"title": self.current_section["content"].strip(), "content": ""}

    def handle_data(self, data):
        if self.recording:
            self.current_section["content"] += data
        elif self.current_section["title"]:
            self.current_section["content"] += data + " "

class FullPythonDocScraper:
    def __init__(self, base_url="https://docs.python.org/3/"):
        self.base_url = base_url
        self.data = []
        self.pages_scraped = 0
        self.start_time = time.time()

    def scrape_page(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                html = response.read().decode('utf-8')
                parser = SimpleHTMLParser()
                parser.feed(html)
                for section in parser.data:
                    section['url'] = url
                    self.data.extend(parser.data)
            self.pages_scraped += 1
            if self.pages_scraped % 10 == 0:
                self.save_checkpoint()
                self.print_progress()
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    def scrape_toc(self, toc_url):
        try:
            with urllib.request.urlopen(toc_url) as response:
                html = response.read().decode('utf-8')
                links = re.findall(r'href="(.*?)"', html)
                total_links = len([link for link in links if link.startswith('library/') and link.endswith('.html')])
                print(f"Found {total_links} pages to scrape.")
                for link in links:
                    if link.startswith('library/') and link.endswith('.html'):
                        page_url = self.base_url + link
                        self.scrape_page(page_url)
                        time.sleep(1)  # Be polite to the server
        except Exception as e:
            print(f"Error scraping table of contents: {e}")

    def save_checkpoint(self):
        checkpoint_file = f"python_docs_data_checkpoint_{self.pages_scraped}.json"
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print(f"Checkpoint saved: {checkpoint_file}")

    def print_progress(self):
        elapsed_time = time.time() - self.start_time
        pages_per_second = self.pages_scraped / elapsed_time
        print(f"Pages scraped: {self.pages_scraped}")
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        print(f"Pages per second: {pages_per_second:.2f}")
        print(f"Total sections collected: {len(self.data)}")
        print("--------------------")

    def save_final_data(self, filename="python_docs_data_final.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scraper = FullPythonDocScraper()
    print("Starting full Python documentation scrape...")
    scraper.scrape_toc("https://docs.python.org/3/contents.html")
    scraper.save_final_data()
    end_time = time.time()
    print(f"Scraping complete. Total time taken: {end_time - scraper.start_time:.2f} seconds")
    print(f"Total pages scraped: {scraper.pages_scraped}")
    print(f"Total sections collected: {len(scraper.data)}")
    print(f"Final data saved to python_docs_data_final.json")