from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import csv

start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("chromedriver.exe")
browser.get(start_url)
time.sleep(10)

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planet_data = []
new_planet_data = []

def scrape():
    for i in range(50):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
            if current_page_num < i:
                browser.find_element("xpath", "/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a").click()
            elif current_page_num > i:
                browser.find_element("xpath", "/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[1]/a").click()
            else:
                break

        for u in soup.find_all("ul", attrs={"class", "exoplanet"}):
            liTags = u.find_all("li")
            templist = []
            #enumerate is a function that returns the index along with the element.
            for index, liTag in enumerate(liTags):
                if index == 0:
                    templist.append(liTag.find_all("a")[0].contents[0])
                else:
                    try: 
                        templist.append(liTag.contents[0])
                    except:
                        templist.append("")
            hyperlink = liTags[0]
            templist.append("https://exoplanets.nasa.gov"+hyperlink.find_all("a", href=True)[0]["href"])
            planet_data.append(templist)
        browser.find_element("xpath", "/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a").click()
        print(f"{i} page done")

def scrapeMoreData(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        templist = []
        for t in soup.find_all("tr", attrs={"class", "fact_row"}):
            tdTags = t.find_all("td")
            for y in tdTags:
                try:
                    templist.append(y.find_all("div", attrs = {"class", "value"})[0].contents[0])
                except:
                    templist.append("")
        new_planet_data.append(templist)
    except:
        time.sleep(2)
        scrapeMoreData(hyperlink)
scrape()

for index, data in enumerate(planet_data):
    scrapeMoreData(data[5])

final_planet_data = []
for index, data in enumerate(planet_data):
    e = new_planet_data[index]
    e = [elem.replace("\n", "") for elem in e  ]
    e = e[:7]
    final_planet_data.append(data + e)
with open("ScrapePlanet.csv", "w") as f:
    c = csv.writer(f)
    c.writerow(headers)
    c.writerows(final_planet_data)