#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import libraries, set the url
#pandas is used to easily grab tables from the page
import pandas as pd
#selenium is used to get pages that require javascript code to be executed to get data
from selenium import webdriver
#this is used for parsing information from the html code
from bs4 import BeautifulSoup, SoupStrainer
#this is where the chrome driver is located
driver_path = r"C:/Users/lemar/Desktop/schoolwork/Senior Design 2/chromedriver_win32/chromedriver.exe"
#set the path to the chrome driver
browser = webdriver.Chrome(executable_path = driver_path)
#this is the url we'll visit
url = "https://www.pro-football-reference.com/teams/den/2019_advanced.htm"


# In[ ]:


#first, let's get the tables directly using pandas
#this method returns a list of tables that were on the page
tables = pd.read_html(url)
#print out the tables to see
print("Total of " + str(len(tables)) + " tables")
print()
for table_index, table in enumerate(tables):
    print("Table " + str(table_index))
    print(table.head())
    print()


# In[ ]:


#notice that the above only shows 4 tables. It only grabbed the first 4 on the page concerning QB's.
#that's because the read_html method (and most methods for requesting web pages) will only return
#static html content, not any html that is created by javascript code.
#to fix that, we use selenium
#first, get the page using Selenum:
browser.get(url)
#now pass that to the read_html function
post_js_tables = pd.read_html(browser.page_source)
#now print the tables again to see the difference
print("Total of " + str(len(post_js_tables)) + " tables")
print()
for table_index, table in enumerate(post_js_tables):
    print("Table " + str(table_index))
    print(table.head())
    print()


# In[ ]:


#now let's say we need to get the links in one of the tables
#this is where we'll utilize BeautifulSoup
#we can inspect the html in Chrome using More tools -> Developer tools to find the id of the table we want
#here's the id we're looking for in this case:
table_id = "advanced_rushing"
#get just that table
table_tag =  browser.find_element_by_id(table_id)
#get the html within the table
inner_html = table_tag.get_attribute("innerHTML")
#show the raw html
print(inner_html)


# In[ ]:


#get all of the links in the table's inner html as a list
a_tags =  BeautifulSoup(inner_html, parse_only=SoupStrainer('a'), features="lxml")
#print the links
for each in a_tags:
    print(each)


# In[ ]:


#now let's parse the tag to get the url within it
#this list will hold the links contained in the a tags
links = []
#for each a tag,
for each in a_tags:
    #get what comes after the equals sign
    first_split = str(each).split("=")[1]
    #get what comes before the closing symbol for the a tag
    second_split = first_split.split(">")[0]
    #take off the quotes by cutting out the first and last characters
    links.append(second_split[1:-1])
#print the parsed links
for each in links:
    print(each)

