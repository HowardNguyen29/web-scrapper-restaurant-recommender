# %%
from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import csv

# %%
URL = "https://www.yelp.ca/biz/pai-northern-thai-kitchen-toronto-5?osq=Restaurants"

def get_page():
    global url
    url = URL
    if not re.match(r'https?://www.yelp.ca/',url):
        sys.exit(1)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('\<(.*?)\>', '', text)
    return text

def collect_name_res(soup):

    restaurant_text = soup.find("h1")
    restaurant_name = restaurant_text.text.strip()

    return restaurant_name

def collect_the_total_review(soup):
    reviews_element = soup.find("p", class_="css-foyide")
    reviews_text = reviews_element.text.split(' ')[0]
    return reviews_text

def collect_text(soup):
    text = f'url: {url}\n\n'
    para_text = soup.find_all('p')
    for para in para_text:
        text += f"{para.text}\n\n"
    return text

def collect_name(soup):
    text = []
    name_text = soup.select('div[class*="user-passport-info"] span[class*="fs-block"] a')
    for name in name_text:
        val = name.text
        text.append(val)
    return text

def collect_review(soup):
    text = []
    name_text = soup.select('p[class*="comment__09f24__D0cxf"] span')
    for name in name_text:
        val = name.text
        text.append(val)
    return text

def collect_stars(soup):
    text = []
    name_text = soup.select('#reviews > section > div.css-1qn0b6x > ul > li > div > div.css-10n911v > div > div > span > div')
    for name in name_text:
        val = name['aria-label'].replace(' star rating', '')
        text.append(val)
    return text

def save_file(reviews):
    # Name of the CSV file
    csv_file = 'reviews.csv'
    page = get_page()
    res_name = collect_name_res(page)
    total_review = collect_the_total_review(page)
    # Writing to CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name of restaurant: ' + res_name])
        writer.writerow(['Total Review: ' + total_review])
        # Write the header row if needed
        writer.writerow(['Reviewer', 'Rating (stars)', 'Review'])
        # Write the data rows
        writer.writerows(reviews)

    print(f'Reviews have been written to {csv_file}.')
        
if __name__ == '__main__':
    page = get_page()
    
    names = collect_name(page)
    reviews = collect_review(page)
    stars = collect_stars(page)
    infos = list(map(list, zip(names, stars, reviews)))
    

    save_file(infos)


