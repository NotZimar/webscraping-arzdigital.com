import csv
import requests
from bs4 import BeautifulSoup
import schedule
import time
def scrape_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    first_item = soup.find('div', class_='arz-breaking-news__item')
    news_item = {}
    link = first_item.find('a', class_='arz-breaking-news__item-link')['href']
    if 'arzdigital' in link:
        news_item['link'] = link
        title_div = first_item.find('div', class_='arz-breaking-news__title arz-tw-p-0')
        if title_div:
            news_item['title'] = title_div.text.strip()
        else:
            news_item['title'] = 'No title available'
        return news_item
def item_exists_in_csv(news_item, csv_file):
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['title'] == news_item['title'] and row['link'] == news_item['link']:
                    return True
    except FileNotFoundError:
        return False
    return False
def write_to_csv(news_item, csv_file):
    if item_exists_in_csv(news_item, csv_file):
        print(f"Item with title '{news_item['title']}' and link '{news_item['link']}' already exists in the CSV.")
        return
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        file.seek(0, 2)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(news_item)
        print(f"Successfully added item with title '{news_item['title']}' and link '{news_item['link']}' to the CSV.")
def scrape_and_save_to_csv(url, csv_file):
    news_item = scrape_news(url)
    write_to_csv(news_item, csv_file)
def job():
    url = 'https://arzdigital.com/breaking/'
    url_two = 'https://arzdigital.com/breaking/bitcoin'
    csv_file = 'news.csv'
    scrape_and_save_to_csv(url, csv_file)
    scrape_and_save_to_csv(url_two, csv_file)
schedule.every(15).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)