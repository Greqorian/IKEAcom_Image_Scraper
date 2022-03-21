# -*- coding: utf-8 -*-
"""IKEAcom_Image_Scraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Lv0xU9PGw4lm1DM49nQAqwYcq2vU1ULJ

# IKEA.com Image Scraper  
### Python script to retrieve images from the ikea online store
---
This scraper is based on a list of ikea products from an extensive dataset CrawlFeeds on Kaggle: https://www.kaggle.com/crawlfeeds/ikea-us-products-dataset

Download this dataset and save it to your google drive.
Scraping images from an online store website is done in 3 steps:

## 1. Create IKEA product list

1.1 Import libraries
"""

# package imports
#basics
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import json # json files

#visualisation
from matplotlib import pyplot as plt

#scraping
from bs4 import BeautifulSoup
import requests

"""1.2 Mount data storage"""

from google.colab import drive
drive.mount('/content/drive')

"""1.3 Open the dataset file from your Google Drive. Use the filepath of the CrawlFeeds file."""

# Opening JSON file
f = open('/content/drive/MyDrive/DATA/ikea_sample_file.json', "r")
# a dictionary
data = json.load(f)

print(data[0])
print(len(data))

"""1.4 Write your list of IKEA products, extracting only relevant keys."""

ikeaProducts = []

for x in data:
  id = x['sku'].replace('.','')
  name = x['product_title'].split(" ")[0]
  title = x['product_title']
  url = x['product_url']
  currency = x['currency']
  price = x['product_price']

  breadcrumbs = x['breadcrumbs'].split("/")
  print(breadcrumbs)

  if len(breadcrumbs)>3:
    category = breadcrumbs[1]
    group = breadcrumbs[2]
    subgroup = breadcrumbs[3]

    ikeaProducts.append({
        'id': id, 
        'name': name,
        'title': title, 
        'url': url, 
        'currency': currency, 
        'price': price, 
        'category': category, 
        'group': group, 
        'subgroup': subgroup})

"""1.5 Create new directory for your files, by simply adding the new folder in your Google Drive


"""

# change directory to selected folder
os.chdir('/content/drive/MyDrive/DATA/IKEAProductLists')

"""Save the newly created list to the JSON file for later use"""

with open('ikeaProducts.json', 'w', encoding='utf-8') as outfile:
    json.dump(ikeaProducts, outfile, ensure_ascii=False)

"""##2. Create a list of image sources

2.1 In case you start from this point, load the list from a file (optional)
"""

# Opening JSON file
f = open('/content/drive/MyDrive/DATA/IKEAProductLists/ikeaProducts.json', "r")
# a dictionary
ikeaProducts = json.load(f)
print(len(ikeaProducts))

"""2.2 Extract only the furniture from product list """

# Extract only the furniture images from images list 
category = 'Furniture'
selectedCategoryList = [x for x in ikeaProducts  if x['category'] == category]
print(len(selectedCategoryList))

"""2.3 Extracting image sources for products in the selected range, using BeautifulSoup """

ikeaImagesList = []
# choose your range from 1 to 1719 (mnumber of furniture from FeedCrawlers dataset)
range = [0,30]

# select pictures of products
for x in selectedCategoryList[range[0]:range[1]]:
  print(x['url'])

  url = x['url']
  id = x['id']
  name = x['name']
  title = x['title'].replace(' ', '_').replace('/', '-').replace(',', '').replace('"', '')
  category = x['category']
  group = x['group']
  subgroup = x['subgroup']

# download of html code
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  images = soup.find_all('img')

# save all source links of pictures to an array
  for image in images:

    if hasattr(image, 'alt') and hasattr(image, 'src') and name in image['alt']:

      ikeaImagesList.append({
          'id': id, 
          'name': name, 
          'title': title, 
          'category':category, 
          'group':group, 
          'subgroup':subgroup, 
          'src': image['src']  
          })
      
  print(len(ikeaImagesList))

"""2.4 You can save list of souces from IKEA Store to the JSON file. (optional)"""

# change directory
os.chdir('/content/drive/MyDrive/DATA/furnitureImages/100-furniture')
 
with open('100-furniture-imagesList.json', 'w', encoding='utf-8') as outfile:
     json.dump(ikeaImagesList, outfile, ensure_ascii=False)

"""##3. Download images from ikea.com

3.1 In case you start from this point, load the list of sources from the JSON file (optional)
"""

# Opening JSON file
f = open('/content/drive/MyDrive/DATA/furnitureImages/100-furniture/100-furniture-imagesList.json', "r")
# a dictionary
ikeaImagesList = json.load(f)

"""3.2 Choose your directory for images"""

# make sure your images will be savred to 'train' folder for AI model recognition purposes
os.chdir('/content/drive/MyDrive/DATA/furnitureImages/100-furniture/train')
!pwd

"""3.3 Dowload images"""

imagesListInput = ikeaImagesList
# list for images labels
IkeaOnlineImagesList = []

for index, image in enumerate(imagesListInput):
  
    title = image['title']
    id = image['id']
    # some symbols cannot be saved to the name of file, make sure they are replaced
    name = image['name'].replace('/','_')
    link = image['src']

    for index, src in enumerate(link):
      # images will be saved with names: index_id_name_ikeaOnline.jpg
      fileName = str(index) + '_' + id + '_' + name + '_' + 'ikeaOnline' +'.jpg'
      IkeaOnlineImagesList.append({'title': fileName, 'name':name})

      with open(fileName, 'wb') as f:
        im = requests.get(link)
        f.write(im.content)
        f.close()
        print('Writing: ', fileName)

"""3.4 Save list of labels to JSON file. Important for AI Model training"""

# change directory for the labels list
os.chdir('/content/drive/MyDrive/DATA/furnitureImages/30-furniture')
!pwd
# save the ebayImagesList to JSON file
with open('IkeaOnlineImagesList.json', 'w', encoding='utf-8') as outfile:
    json.dump(IkeaOnlineImagesList, outfile, ensure_ascii=False)