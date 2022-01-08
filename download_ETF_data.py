from selenium import webdriver
from time import sleep
import os

def dt_down():
    chromeoptions = webdriver.ChromeOptions()
    chromeoptions.add_experimental_option("prefs", {
      "download.default_directory": str(os.getcwd()),
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(executable_path="C:\chromedriver.exe", options=chromeoptions)

    driver.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201")
    driver.find_element_by_xpath("/html/body/div[2]/section[2]/aside/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[3]/a").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[2]/section[2]/aside/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[3]/ul/li[1]/a").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[2]/section[2]/aside/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[3]/ul/li[1]/ul/li[4]/a").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[2]/section[2]/section/section/div/div/form/div[2]/div/p[2]/button[2]/img").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/div[2]/section[2]/section/section/div/div/form/div[2]/div[2]/div[2]/div/div[1]/a").click()
    sleep(5)
    driver.close()