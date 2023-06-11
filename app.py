import requests
from bs4 import BeautifulSoup
import csv
import pandas
from itertools import zip_longest
import re

product_name = []
price = []
links = []
urls = links
marque = []

data = input('\033[1m- Enter your search > \033[0m')
search = re.sub(r'\s+', '+', data)


choose = '\n  \033[1mPlease choose a number\033[0m'
sort = str(input('Sort By : \n \033[1m1\033[0m > Best Seller \n \033[1m2\033[0m > Newest \n \033[1m3\033[0m > Low to High \n \033[1m4\033[0m > High to Low \n \033[1m5\033[0m > Highest Rating \n\033[1m- Please choose a number > \033[0m'))

if sort == '2' :
    sort = 'newest'
elif sort == '3':
    sort = 'lowest-price'
elif sort == '4':
    sort = 'highest-price'
elif sort == '5':
    sort = 'rating'

print('Please wait sir , until we finished the process...⌛️')

result = requests.get(f"https://www.jumia.ma/catalog/?q={search}&sort={sort}#catalog-listing")


if sort == '1':
    sort = 'best-seller'
fltr = sort.replace('-', ' ')
pathx = f'{data}-[{fltr}]'


src = result.content

soup = BeautifulSoup(src, "lxml")

product_names = soup.find_all('h3', {'class':'name'})
prices = soup.find_all('div', {'class':'prc'})
linke = soup.find_all('article', {'class':'prd _fb col c-prd'})


 # ghadi ndiro wa7ed loop bach manb9awch n3awed nketbo 7arf b7arf ,nsahlo 3lina lomor
for i in range(len(product_names)):           #lmohim derna i b range len(product name) ye3ni ch7al mkayna men product kina 40 ye3ni loop ghadar 40 mera
    product_name.append(product_names[i].text)    #ghayb9a ydkhoul wa7ed b wa7ed
    links.append('https://www.jumia.ma/' + linke[i].find('a').attrs['href'])
    price.append(prices[i].text)

for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    marques = soup.find_all('div', {'class': '-phs'})[2].find('a', {'class': '_more'})
    marque.append(str(marques.text))


    
file_list = [product_name, price, marque, urls]
exported = zip_longest(*file_list)
with open(r'C:\Users\nalml\OneDrive\Bureau\JUMIA File Scraping\{}.csv'.format(pathx), 'w', encoding='utf-8') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(['Name','Price','Marque','Link'])
    wr.writerows(exported)


done = "\033[1mScraping is Done\033[0m"
print('{} \u2705'.format(done))


input("Press Enter to exit...")