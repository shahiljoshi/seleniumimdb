import time
from selenium import webdriver
from imdbseries import get_series_links
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from dbconnection import connection
import re
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()

series_links = get_series_links()

seriesdata = {}
role_name = []
original_name = []
cast_id = []
directors = []
director_id = []
series_genres = []

def series_data():
    driver.get(series_links)

    series_id = series_links.split("/")[4]
    print(series_id)
    seriesdata['series_id'] = series_id
    # movie_title = driver.find_element_by_tag_name("h1").text
    series_title = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    ).text
    print(series_title)
    seriesdata['series_title'] = series_title


    series_year = driver.title.split(" ")[5]
    print(series_year.split(")")[0])
    seriesdata['series_year'] = series_year

    series_runtime = WebDriverWait(driver,30).until(
        EC.presence_of_element_located((By.TAG_NAME,"time"))
    ).text
    print(series_runtime)
    seriesdata['series_runtime'] = series_runtime

    series_genre = WebDriverWait(driver,30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"div.subtext"))
    ).text.split('|')[2]
    series_genres = series_genre.split(",")
    print("generelst",series_genres)
    print(series_genre)
    seriesdata['series_genre'] = series_genre

    # for i in range(len(series_genres)):
    #     insert_genres = "INSERT OR IGNORE INTO movie_genre_tbl VALUES(?,?)", (seriesdata['series_id'], series_genres[i])
    #     connection(insert_genres)



    series_desc = WebDriverWait(driver,30).until(
        EC.presence_of_element_located((By.CLASS_NAME,"summary_text"))
    ).text
    print(series_desc)
    seriesdata['series_desc'] = series_desc
    section = driver.find_element_by_css_selector('div.plot_summary')
    credit_sec = section.find_elements_by_css_selector('div.credit_summary_item')

    for i in credit_sec:
        if i.find_element_by_css_selector('h4.inline').text == 'Creators:':
            all_a = i.find_elements_by_css_selector('a')
            for name in all_a:
                print(name.get_attribute('href').split("/")[4])
                director_id.append(name.get_attribute('href').split("/")[4])
                directors.append(name.text)
                # data['director']

    print(directors)
    seriesdata['directors'] = directors


    series_rating = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ratingValue span"))
    ).text
    print(series_rating)
    seriesdata['series_rating'] = series_rating

    series_storyline = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.article p span"))
    ).text
    print(series_storyline)
    seriesdata['series_storyline'] = series_storyline

    series_language = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.txt-block:nth-child(5) > a:nth-child(2)"))
    ).text
    print(series_language)
    seriesdata['series_language'] = series_language


    time.sleep(5)
    seasons_link=[]
    seasons = driver.find_elements_by_css_selector("div.seasons-and-year-nav > div:nth-child(4)")
    # links = seasons.find_elements_by_css_selector('a')
    # print(len(links))
    for i in seasons:
        # if i.find_element_by_css_selector('h4.float-left') == "Seasons":
        for link in i.find_elements_by_css_selector('a'):
            seasons_link.append(link.get_attribute('href'))
        print(seasons_link)
        print(len(seasons_link))

    seriesdata['seasons_link'] = len(seasons_link)


    time.sleep(15)

    # for crew team

    try:
        cast_list = WebDriverWait(driver, 30).until(EC.presence_of_element_located
                                                    ((By.XPATH, "//table[contains(@class, 'cast_list')]")))
        trows = cast_list.find_elements_by_tag_name('tr')
        for tr in trows:
            td = tr.find_elements_by_tag_name('td')
            if len(td) == 4:
                row = [ele for ele in td]
                # print(row[1].find_element_by_tag_name('a').get_attribute('href').split('/')[4])
                cast_id.append(row[1].find_element_by_tag_name('a').get_attribute('href').split('/')[4])
                # print(re.sub("[^a-zA-Z' ]+", '', row[1].text).strip())
                original_name.append(re.sub("[^a-zA-Z' ]+", '', row[1].text).strip())
                # print( re.sub("[^a-zA-Z' ]+", '', row[3].text).strip().replace('episodes', ''))
                role_name.append(re.sub("[^a-zA-Z' ]+", '', row[3].text).strip().replace('episodes', ''))
        print(cast_id)
        print(original_name)
        print(role_name)


    except (NoSuchElementException, TimeoutException):
        pass

    return seasons_link






# for i in series_links:
#     series_data(i)

series_data()

# insertseries = "INSERT OR IGNORE INTO movie_tbl VALUES(?,?,?,?,?,?,?,?,?)", (seriesdata['series_id'],
#                                                                            seriesdata['series_title'],
#                                                                            seriesdata['series_year'],
#                                                                            seriesdata['series_runtime'],
#                                                                            seriesdata['series_desc'],
#                                                                            seriesdata['series_rating'] ,
#                                                                            seriesdata['series_storyline'],
#                                                                            seriesdata['seasons_link'],
#                                                                            seriesdata['series_language']
#                                                                            )
#
# connection(insertseries)
#
# for i in range(len(cast_id)):
#     insert_cast= "INSERT OR IGNORE INTO starcast_tbl VALUES(?,?,?)", (cast_id[i], original_name[i], role_name[i])
#     connection(insert_cast)
#     insertseries_cast = "INSERT OR IGNORE INTO movie_cast VALUES(?,?)", (seriesdata['series_id'],cast_id[i])
#     connection(insertseries_cast)

# for i in range(len(director_id)):
#     insert_director = "INSERT OR IGNORE INTO directors_tbl VALUES(?,?)", (director_id[i], directors[i])
#     connection(insert_director)
#     insert_director_movie = "INSERT OR IGNORE INTO directors_cast_tbl VALUES(?,?)", (seriesdata['series_id'], director_id[i])
#     connection(insert_director_movie)




