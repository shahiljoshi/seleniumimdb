import time
from selenium import webdriver


from imdbseriesdata import series_data,seriesdata
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from dbconnection import connection

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()
series_id = seriesdata['series_id']
episode_links = series_data()



def episode_data(i):
    driver.get(i)

    season_id = i.split("_")[-1]
    print(season_id)

    for episode in driver.find_elements_by_css_selector("div.info"):

        # episode_number = WebDriverWait(episode, 30).until(
        #     EC.presence_of_element_located((By.TAG_NAME, 'meta'))
        # ).text
        # time.sleep(5)
        try:
                episode_number = episode.find_element_by_tag_name('meta').get_attribute('content')
                print(episode_number)
        except (NoSuchElementException, TimeoutException):
            pass


        episode_title = WebDriverWait(episode, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "strong"))
        ).text
        print(episode_title)

        episode_date = WebDriverWait(episode, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.airdate"))
        ).text
        print(episode_date)

        episode_rating = WebDriverWait(episode, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.ipl-rating-widget div.ipl-rating-star.small span.ipl-rating-star__rating"))
        ).text
        print(episode_rating)

        episode_desc = WebDriverWait(episode, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.item_description"))
        ).text
        print(episode_desc)
        # insert_season = "INSERT OR IGNORE INTO season_tbl VALUES(?,?,?,?,?)", (series_id,episode_title, episode_date, episode_rating,episode_desc)
        insert_season = "INSERT OR IGNORE INTO season VALUES(?,?,?,?,?,?,?)", (series_id,season_id,episode_number,episode_title, episode_date, episode_rating,episode_desc)
        connection(insert_season)


for i in episode_links:
    episode_data(i)




