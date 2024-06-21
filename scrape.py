import requests
from bs4 import BeautifulSoup
import json

def cleaner(url):

    # url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"

    page = requests.get(url)
    # print(page.content)

    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)

    div_page_header = soup.find('div', class_='page-header')
    page_header = div_page_header.text.strip() if div_page_header else "No Header!"
    # print(page_header)

    all_books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    # print(all_books)

    category_arr = []

    for book in all_books:
        a_title = book.find('h3').find('a')
        title = a_title.text.strip() if a_title else "No Title!"
        # print(title)

        p_rating = book.find('p',class_='star-rating')
        rating_class = p_rating.get('class', [])[1]
        # print(rating_class)

        p_price = book.find('p', class_='price_color')
        price = p_price.text.strip() if p_price else "No Price!"
        # print(price)

        p_availability = book.find('p', class_='availability')
        availability = p_availability.text.strip() if p_availability else "No Info!"
        # print(availability)

        single_book = {
            "title": title,
            "rating": rating_class,
            "price": price,
            "availability": availability
        }
        
        category_arr.append(single_book)

    category_dictionary = {
        "data": category_arr,
        "type": page_header
    }

    return category_dictionary

sequential_art = cleaner("https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html")
# print(sequential_art)

fiction = cleaner("https://books.toscrape.com/catalogue/category/books/fiction_10/index.html")
# print(fiction)

fantasy = cleaner("https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html")
# print(fantasy)

books_arr = [sequential_art, fiction, fantasy]


json_data = json.dumps(books_arr, indent=2)

with open('book_api.json', 'w') as file:
    file.write(json_data)




with open("book_api.json", 'r') as file:
    data = json.load(file)
# print(data)

def count_posts_with_rating(data, rating):
    count = 0
    for category in data:
        for item in category['data']:
            if item['rating'] == rating:
                count += 1
    return count

test_five_rating_count = count_posts_with_rating(data, "Five")
print(test_five_rating_count)