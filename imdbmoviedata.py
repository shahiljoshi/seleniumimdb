import time
from selenium import webdriver
from imdbmovies import get_movie_links
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import re
from dbconnection import connection

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()

movie_links = get_movie_links()

director_id=[]
writers_id=[]
role_name = []
original_name = []
cast_id = []
season=0
directors = []
writers = []
moviedata ={}

def movie_data(i):
    driver.get(i)

    movie_id = i.split("/")[4]
    print(movie_id)
    moviedata['movie_id']=movie_id
    # movie_title = driver.find_element_by_tag_name("h1").text
    movie_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    ).text
    print(movie_title)
    moviedata['movie_title']=movie_title

    movie_year = movie_title.split(" ")[-1]
    print(movie_year)
    moviedata['movie_year'] = movie_year

    movie_runtime = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.TAG_NAME,"time"))
    ).text
    print(movie_runtime)
    moviedata['movie_runtime'] = movie_runtime

    movie_genre = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"div.subtext"))
    ).text.split('|')[2]
    print(movie_genre)
    movie_genres = movie_genre.split(",")
    print("generelst", movie_genres)

    # for i in range(len(movie_genres)):
    #     insert_genres = "INSERT OR IGNORE INTO movie_genre_tbl VALUES(?,?)", (  moviedata['movie_id'], movie_genres[i])
    #     connection(insert_genres)
    #


    movie_desc = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CLASS_NAME,"summary_text"))
    ).text
    print(movie_desc)
    moviedata['movie_desc'] = movie_desc

    try:
        section = driver.find_element_by_css_selector('div.plot_summary')
        credit_sec = section.find_elements_by_css_selector('div.credit_summary_item')
        directors = []
        writers = []
        for i in credit_sec:
            if i.find_element_by_css_selector('h4.inline').text == 'Director:':
                all_a = i.find_elements_by_css_selector('a')
                for name in all_a:
                    print(name.get_attribute('href').split("/")[4])
                    director_id.append(name.get_attribute('href').split("/")[4])
                    directors.append(name.text)
            elif i.find_element_by_css_selector('h4.inline').text == 'Writers:':
                all_a = i.find_elements_by_css_selector('a')

                for name in all_a:
                    print(name.get_attribute('href').split("/")[4])
                    writers_id.append(name.get_attribute('href').split("/")[4])
                    writers.append(name.text)
        print(director_id)
        print(writers_id)
        print(directors)
        print(writers)
        # if len(director_id) > 1:
        #     for i in range(len(director_id)):
        #         insert_director = "INSERT OR IGNORE INTO directors_tbl VALUES(?,?)", (director_id[i], directors[i])
        #         connection(insert_director)
        #         insert_director_movie = "INSERT OR IGNORE INTO directors_cast_tbl VALUES(?,?)", (
        #         moviedata['movie_id'], director_id[i])
        #         connection(insert_director_movie)
        # else:
        #     insert_director = "INSERT OR IGNORE INTO directors_tbl VALUES(?,?)", (director_id[0], directors[0])
        #     connection(insert_director)
        #     insert_director_movie = "INSERT OR IGNORE INTO directors_cast_tbl VALUES(?,?)", (
        #     moviedata['movie_id'], director_id[0])
        #     connection(insert_director_movie)
        #
        # if len(writers_id) > 1:
        #     for i in range(len(writers_id)):
        #         insert_writer = "INSERT OR IGNORE INTO writers_tbl VALUES(?,?)", (writers_id[i], writers[i])
        #         connection(insert_writer)
        #         insert_writer_movie = "INSERT OR IGNORE INTO writers_cast_tbl VALUES(?,?)", (
        #         moviedata['movie_id'], writers_id[i])
        #         connection(insert_writer_movie)
        # else:
        #     insert_writer = "INSERT OR IGNORE INTO writers_tbl VALUES(?,?)", (writers_id[0], writers[0])
        #     connection(insert_writer)
        #     insert_writer_movie = "INSERT OR IGNORE INTO writers_cast_tbl VALUES(?,?)", (
        #     moviedata['movie_id'], writers_id[0])
        #     connection(insert_writer_movie)
    except NoSuchElementException:
        directors = None
        writers = None


    movie_rating = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ratingValue span"))
    ).text
    print(movie_rating)
    moviedata['movie_rating'] = movie_rating


    movie_storyline = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.article p span"))
    ).text
    print(movie_storyline)
    moviedata['movie_storyline'] = movie_storyline

    movie_language = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#titleDetails > div:nth-child(5) > a:nth-child(2)"))
    ).text
    print(movie_language)
    moviedata['movie_language'] = movie_language

    time.sleep(15)

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


for i in movie_links:
    movie_data(i)


# insertmovie = "INSERT OR IGNORE INTO movie_tbl VALUES(?,?,?,?,?,?,?,?,?)", ( moviedata['movie_id'],
#                                                                               moviedata['movie_title'],
#                                                                               moviedata['movie_year'],
#                                                                               moviedata['movie_runtime'] ,
#                                                                               moviedata['movie_desc'],
#                                                                               moviedata['movie_rating'],
#                                                                               moviedata['movie_storyline'] ,
#                                                                               season,
#                                                                               moviedata['movie_language']
#                                                                             )
#
# connection(insertmovie)
#
# for i in range(len(cast_id)):
#     insert_cast= "INSERT OR IGNORE INTO starcast_tbl VALUES(?,?,?)", (cast_id[i], original_name[i], role_name[i])
#     connection(insert_cast)
#     insertseries_cast = "INSERT OR IGNORE INTO movie_cast VALUES(?,?)", (moviedata['movie_id'],cast_id[i])
#     connection(insertseries_cast)
#







