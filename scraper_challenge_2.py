import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time

class MLBNewsScraper:
    def __init__(self,site):
        self.site=site

    def _get_html(self,url):
        req=urllib.request.Request(url,headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req)as r:
            return r.read()

    def _resolve_final_url(self, url):
        req=urllib.request.Request(url,headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.uropen(req) as r:
                return r.geturl()
        except Exception as e:
            print("Failed Redirect Solution", url, e)
            return url

    def scrape(self):
        html=self._get_html(self.site)
        soup=BeautifulSoup(html, "html.parser")
        articles=[]
        for tag in soup.find_all("a"):
            title=(tag.get_text() or "").strip()
            url=tag.get("href")
            if not title or not url:
                continue
            full_url=urllib.parse.urljoin(self.site,url)
            keyword="MLB"
            if keyword.lower() not in title.lower():
                continue
            final_url=self._resolve_final_url(full_url)

            if not final_url.startswith("http"):
                continue
            
            print("title:", title)
            print("URL:", final_url)
            print("-"*40)
            articles.append({
                "title": title,
                "url": final_url,
                })
            time.sleep(1)

        return articles

def write_html(articles, filename="mlb_news.html"):

    with open(filename, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang='ja'>\n<head>\n")
        f.write("<meta charset='UTF-8'>\n")
        f.write("<title>MLB News</title>\n")
        f.write("""<style>
ul{
list-style: none;
padding-left: 0;
}
li{
margin-bottom: 10px;
}
</style>""")
        f.write("</head>\n<body>\n")
        f.write("<h1>MLB News Links</h1>\n")
        f.write("<ul>\n")
        for a in articles:
            f.write(f'<li><a href="{a["url"]}" target="_blank">{a["title"]}</a></li>\n')
            f.write("<ul>\n</body>\n</html>\n")

if __name__=="__main__":
                    site="https://news.google.com/search?q=MLB&hl=en-US&gl=US&ceid=US:en"
                    scraper=MLBNewsScraper(site)
                    articles=scraper.scrape()

                    write_html(articles, "mlb_news.html")
                    print(f"{len(articles)} MLB News were written in mlb_news.html")
                    print("Try opening mlb_news.html in your blowser") 
 
