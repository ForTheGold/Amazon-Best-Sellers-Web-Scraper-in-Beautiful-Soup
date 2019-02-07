
## A simple program that scrapes data about best selling Amazon            ##
## products directly from the company website.  It gathers the rank,       ##
## title, rating, number of reviews and pricing information and outputs    ##
## that data to a CSV that is titled after the category name of the        ##
## web page.                                                                ##


##  -----------  Imports  ------------  ##
import requests
from bs4 import BeautifulSoup
import csv

##  -----------  Connect to Webpage and Create Soup  ------------  ##
url = "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_electronics_home_all?pf_rd_p=65f3ea14-1275-4a7c-88f8-1422984d7577&pf_rd_s=center-2&pf_rd_t=2101&pf_rd_i=home&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=WXEF0RWZE4B6BB6Q5RFQ&pf_rd_r=WXEF0RWZE4B6BB6Q5RFQ&pf_rd_p=65f3ea14-1275-4a7c-88f8-1422984d7577"
r = requests.get(url)
soup = BeautifulSoup(r.content)

def get_category(soup):
    """A Simple function that takes in the soup,
    and returns the category of the Amazon BSR that
    we are connecting to."""

    category = soup.find_all("span", {"class": "category"})
    category_strip = category[0].text.replace(" ", "_")
    return category_strip

def get_data(soup):

    """This function takes in the soup and returns several
    lists of values with information about product ranking,
    the title, rating, number of reviews and pricing information.
    It scrapes the Amazon website to gather the data, cleans it,
    and appends it to several lists which are returned."""

    ##  -----------  Initialize Lists  ------------  ##
    ranking_out = []
    titles_out = []
    rating_out = []
    number_of_revs_out = []
    prices_out = []

    ##  -----------  Grab Data  ------------  ##
    ranking = soup.find_all("span", {"class": "zg-badge-text"})
    titles = soup.find_all("div", {"aria-hidden": "true"})
    prices = soup.find_all("span", {"class": "p13n-sc-price"})
    full_box = soup.find_all("span", {"class": "aok-inline-block zg-item"})


    for item in full_box:
        ##  -----------  If Data Exists Add it to the List  ------------  ##
        if item.find("span", {"class": "a-icon-alt"}):
            rating_out.append(item.find("span", {"class": "a-icon-alt"}).text.replace(' out of 5 stars', ''))

        ##  -----------  Otherwise Add Zero (Keeps Data Consistent)  ------------  ##
        else:
            rating_out.append("0")

        if item.find("a", {"class": "a-size-small a-link-normal"}):
            number_of_revs_out.append(item.find("a", {"class": "a-size-small a-link-normal"}).text)
        else:
            number_of_revs_out.append("N/A")

    ##  -----------  Clean Data and Append it to the List ------------  ##
    for i in range(len(ranking)):
        ranking_out.append(ranking[i].text)
        titles_out.append(titles[i].text.strip())
        prices_out.append(prices[i].text)

    return (ranking_out, titles_out, rating_out, number_of_revs_out, prices_out)

def write_csv(ranking, titles, rating, number_of_revs, prices):
    """This function writes all of the data that was scraped
       in the previous function to a CSV file.  It does not have
       any return, but will edit an exist file or create and
       populate it if one does not exist."""

    ##  -----------  Open File and Name it Based on the Category Scrapped Above  ------------  ##
    with open('Amz_BSR_Data_' + category + '.csv', 'w', newline='') as file:
        writer1 = csv.writer(file)

        ##  -----------  Add Header to File  ------------  ##
        writer1.writerow(['Ranking', 'Title', 'Rating', 'Number of Reviews', 'Price'])

        ##  -----------  Populate File with Clean Data  ------------  ##
        for i in range(len(ranking)):
            writer1.writerow([ranking[i], titles[i], rating[i], number_of_revs[i], prices[i]])

##  -----------  Run Functions  ------------  ##
category = get_category(soup)
ranking, titles, rating, number_of_revs, prices = get_data(soup)
write_csv(ranking, titles, rating, number_of_revs, prices)
