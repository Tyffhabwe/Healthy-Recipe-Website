from bs4 import BeautifulSoup
import requests
import csv
import os.path
domain = "https://www.foodinaminute.co.nz"

source = requests.get('https://www.foodinaminute.co.nz/Recipe-Categories/Dinner-Ideas').text
soup = BeautifulSoup(source, 'lxml')

recipe_list = soup.find('ul', class_='media-list recipes')
csv_file = open('cms_scrape.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'article_link', 'image', 'ingredients', 'instructions'])



for recipe in soup.find_all('div', class_='col-xs-12 col-sm-6 col-md-3'):
	headline = recipe.h4.text
	article_src = recipe.find('a')['href']
	article_link = domain + article_src

	#Second Part
	recipe_source = requests.get(article_link).text
	recipe_soup = BeautifulSoup(recipe_source, 'lxml')


	image = recipe_soup.find('img', class_='center-block img-responsive')['src']
	instructions = recipe_soup.find('div', class_='instructions').text
	ingredients = recipe_soup.find('div', class_='section-ingredients').text

	#Add content to csv file
	csv_writer.writerow([headline, article_link, image, ingredients, instructions])

print("Done!")
	



	