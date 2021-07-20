from selenium import webdriver
import time
name = input("Enter Series Name You Want To Search:")

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()

driver.get(f'https://www.imdb.com/find?q={name}&ref_=nv_sr_sm')


def get_series_links():
    series_links=[]
    section = driver.find_element_by_css_selector('table.findList')
    for link in section.find_elements_by_css_selector('td.result_text'):
              flag = link.text
              if "Series" in flag:
                  series_link = link.find_element_by_tag_name('a').get_attribute('href')
                  print(series_link)
                  series_links.append(series_link)
                  print(series_links)
              else:
                  continue

    return series_link


get_series_links()