from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import psycopg

content = ""

try:
    with open('exercises.html') as f:
        content = f.read()
except FileNotFoundError:
    page = requests.get('https://www.strengthlog.com/exercise-directory/')
    content = page.text
    with open('exercises.html', 'w') as f:
        f.write(page.text)

soup = BeautifulSoup(content, 'html.parser')

headers = soup.find_all('h3', class_='wp-block-heading')
lists = soup.find_all('ol', class_='wp-block-list')

for header, list in zip(headers, lists):
    if str(header.text).endswith('Exercises'):
        print(header.text)
        links = list.find_all('a')
        for link in links:
            print(link.text)
            cache_filename = f"cache/{link.text.replace(' ', '_')}.html"
            exercise_content = ""
            try:
                with open(cache_filename, 'r') as cache_file:
                    exercise_content = cache_file.read()
            except FileNotFoundError:
                exercise_page = requests.get(link['href'])
                exercise_content = exercise_page.text
                if exercise_content:
                    with open(cache_filename, 'w') as cache_file:
                        cache_file.write(str(exercise_content))
            exercise_soup = BeautifulSoup(exercise_content, 'html.parser')
            exercise_description = exercise_soup.find('div', class_='wp-block-columns is-layout-flex wp-container-core-columns-is-layout-1 wp-block-columns-is-layout-flex')
            description_text = '\n'.join(exercise_description.stripped_strings)
            print(description_text)

            
            
            
