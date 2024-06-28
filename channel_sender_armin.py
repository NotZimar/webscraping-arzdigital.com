import pandas as pd
import requests
from bs4 import BeautifulSoup
from telethon import TelegramClient
import time
import hashlib
import re  # وارد کردن کتابخانه re


def get_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.select_one('main > section > section > article > section > div > div > p')
        element = soup.select_one('main > section > section > article > section > div > p')
        element_natiomal = soup.select_one('main > section > section > article > section > div > div > div > div > div > div > p')
        if elements:
            return elements.get_text().strip() 
        if element:
            return element.get_text().strip() 
        if element_natiomal:
            return element_natiomal.get_text().strip()

        else:
            print("No article")
            return 'faild'
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def hash_dataframe(df):
    df_str = df.to_string()
    return hashlib.sha256(df_str.encode()).hexdigest()

csv_file = 'news.csv'
api_id = 'x'
api_hash = 'x'
bot_token = 'x'
admin_id = 'x'


client = TelegramClient('bot', api_id=api_id, api_hash=api_hash).start(bot_token=bot_token)

async def send_message(text):
    await client.send_message(admin_id, text)

async def main():
    previous_hash = None
    while True:
        df = pd.read_csv(csv_file, delimiter=',', encoding='utf-8')
        df['text'] = df['link'].apply(get_article_text)
        
        current_hash = hash_dataframe(df)
        
        if current_hash != previous_hash:
            if not df.empty:
                last_row = df.iloc[-1] 
                formatted_text = re.sub(r'(?<=[.!?])(?=\s|$)', '\n\n', last_row['text'])
                message = f"**🛑{last_row['title']}** \n\n **{formatted_text}**"
                await send_message(message)
                previous_hash = current_hash

        time.sleep(960)  

with client:
    client.loop.run_until_complete(main())
