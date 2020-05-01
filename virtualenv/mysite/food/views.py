from django.shortcuts import render, get_object_or_404, HttpResponse
from bs4 import BeautifulSoup
from .models import Post
from django.utils import timezone
from background_task import background
import os
import requests
import csv
import os.path
import logging


logger = logging.getLogger(__name__)

def recipe_main():
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

		_, created = Post.objects.get_or_create(
                title=headline,
                image=image,
                article_link=article_link,
                ingredients=ingredients,
                text=instructions,
                )

		#Add content to csv file
		#csv_writer.writerow([headline, article_link, image, ingredients, instructions])


	
# Create your views here.
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'food/post_detail.html', {'post': post})


def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'food/post_list.html', {'posts': posts})

def home_page(request):
	return render(request, 'food/home_page.html')

def background_view(request):
	recipe_main()

	return HttpResponse("Done!")

def contact(request):
	return render(request, 'food/contact.html')
			

