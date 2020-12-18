# -*- coding: utf-8 -*-

# Author: Xuzhou Yin
# Adapted and Edited by William(Peijian) Ding

# Changes have been made to the original file to account for the following changes:
# 1. that Weibo has changed its html script since the package has been created.
# 2. some lines in the orignal script do not run anymore 
from bs4 import BeautifulSoup
import struct
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import urllib
import urllib.parse
from selenium import webdriver
import datetime
import time as systime
from selenium.webdriver.firefox.webdriver import FirefoxProfile
import unicodecsv as csv
base_url = 'http://s.weibo.com/weibo/'
file = "query"
file_index = 9
def scrap():
	global file_index
	with open('query.txt') as f:
		each_query = f.readlines()
	each_query = [x.strip() for x in each_query]
	# print urllib.quote(urllib.quote(each_query[0]))
	for each in each_query:
		query = each
		s = each.split(';')
		keyword = s[0]# urllib.quote(urllib.quote(s[0]))
# 		date = s[1]
		start = s[1]
		end = s[2]
		page = s[3]
		scrap_each_query(keyword, start, end, page, query)
		file_index = file_index + 1

def scrap_each_query(keyword, start, end, page, query):
	real_keyword = keyword
	keyword = urllib.parse.quote(urllib.parse.quote(keyword))
	print(keyword)
	all_content = []
	all_time = []
	profile = FirefoxProfile("/Users/williamding/Library/Application Support/Firefox/Profiles/6irszdj9.default-release")
	driver = webdriver.Firefox(profile)
	url = base_url + keyword + "&typeall=1&suball=1&timescope=custom:" + start + ":" + end + "&page=" + "1"
	driver.get(url)
	systime.sleep(5)
	for i in range(int(page)):
		url = base_url + keyword + "&typeall=1&suball=1&timescope=custom:" + start + ":" + end + "&page=" + str(i + 1)
		driver.get(url)
		page_source = driver.page_source
		soup = BeautifulSoup(page_source, "lxml")
		content = soup.find_all("p", { "class" : "txt" ,"node-type":"feed_list_content"})
		time = soup.find_all( "a", {"suda-data" :re.compile(".*wb_time.*")})
# 		href =re.compile("//weibo.com/"), target = "_blank"
		for each in content:
			all_content.append(each.get_text())
		for each in time:
			each.get_text()
# 			each = each.encode('utf-8')
			t = ""
			if "月" in each:
				t = each[(each.index("月")-1):(each.index("月"))]+ each[(each.index("月") + 1):(each.index("月") + 3)]
# =============================================================================
# 			else:
# 				time = each[0:each.index()]
# =============================================================================
			all_time.append(t)
	driver.close()
	save_to_csv(file + str(file_index), real_keyword, all_content, all_time, query)

def save_to_csv(filename, keyword, content, time, query):
	with open('./output/' + filename + '.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, dialect='excel', encoding='utf-8')
		spamwriter.writerow(["query", "Post ID", "keyword", "Post Time", "Post Content" ])
		for i in range(len(content)):
			spamwriter.writerow([query, i +1, keyword, time[i],content[i]])

scrap()


#url = base_url + keyword + "&typeall=1&suball=1&timescope=custom:" + start + ":" + end + "&page=" + str(int(page) + 1)
# driver = webdriver.Chrome()
# driver.get("http://s.weibo.com/weibo/%25E5%2585%2583%25E6%2597%25A6&typeall=1&suball=1&timescope=custom:2016-12-31:2016-12-31&Refer=g")
# page_source = driver.page_source
