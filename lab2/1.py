import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
url = "https://lenta.ru"
#class="card-mini _longgrid"
#"card-big _slider _dark _popular _article"
def parse_lenta(url, max_news):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Ошибка при загрузке сайта: {response.status_code}")
    bs = BeautifulSoup(response.text, "html.parser")
    news_list = []
    news_blocks = bs.find_all("a", class_=["card-mini", "card-big"], limit = max_news)
    for block in news_blocks:
        title = block.get_text(strip=True)[:-5]  # заголовок
        link = "https://lenta.ru" + block["href"]  # ссылка на статью
        article_resp = requests.get(link)
        article_bs = BeautifulSoup(article_resp.text, "html.parser")

        paragraphs = article_bs.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs)
        news_list.append({
            "title": title,
            "url": link,
            "text": text
        })
    df = pd.DataFrame(news_list)
    return df

if __name__ == "__main__":
    df = parse_lenta(url, max_news=5)  # например, берём 5 новостей
    print(df.head())
    df.to_csv("lenta_news.csv", index=False, encoding="utf-8")
    print("\nРезультат сохранён в lenta_news.csv")
