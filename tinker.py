from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pathlib
import argparse
import os
import argparse

# Setup Commandline Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--namesfile")
parser.add_argument("--design")
parser.add_argument("--username")
parser.add_argument("--password")
args = parser.parse_args()

# Setup WebDriver via GeckoDriver
driver_binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
driver_profile = webdriver.FirefoxProfile()
driver_profile.set_preference("browser.download.dir", str(pathlib.Path(__file__).absolute()))
driver_profile.set_preference("browser.preferences.instantApply",True)
driver_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
driver_profile.set_preference("browser.helperApps.alwaysAsk.force",False)
driver_profile.set_preference("browser.download.manager.showWhenStarting",False)
driver_profile.set_preference("browser.download.folderList",0)
driver = webdriver.Firefox(firefox_profile=driver_profile, firefox_binary=driver_binary)

wait = WebDriverWait(driver, 5)
driver.get("https://www.tinkercad.com/login")

def login_by_username():
    # LOGIN BUTTON
    login_button_path = "/html/body/div/div/app/div/div/main/ng-component/main/div/div[1]/a[2]"
    # wait until login button is loaded
    wait.until(EC.presence_of_element_located((By.XPATH, login_button_path))) 
    login_button = driver.find_element_by_xpath(login_button_path)
    action = ActionChains(driver)
    # click on login button
    action.move_to_element(login_button).click().perform()
def enter_username(username):
    # USERNAME INPUT
    username_input_path = '//*[@id="userName"]'
    # wait until username input box is loaded
    wait.until(EC.presence_of_element_located((By.XPATH, username_input_path)))
    username_input = driver.find_element_by_xpath(username_input_path)
    # input username
    username_input.send_keys(username)
    # submit username
    driver.find_element_by_xpath('//*[@id="verify_user_btn"]').click()
def enter_password(password):
    # PASSWORD INPUT
    password_input_path = '//*[@id="password"]'
    # wait until password input box is loaded
    wait.until(EC.element_to_be_clickable((By.XPATH, password_input_path)))
    password_input = driver.find_element_by_xpath(password_input_path)
    # click on password box to enable it
    password_input.click()
    # input password
    password_input.send_keys(password)
    # submit password
    driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()
    wait.until(EC.url_matches("https://www.tinkercad.com"))

login_by_username()
enter_username(args.username)
enter_password(args.password)

with open(args.namesfile, 'r') as file:
   for user in file.readlines():
       driver.get("https://www.tinkercad.com/users/" + user)
       try:
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, args.design)))
            design_link = driver.find_element_by_link_text( args.design)
            design_link.click()

            edit_path = "//*[contains(text(), 'Copy and Tinker')]" 
            wait.until(EC.url_contains("things"))
            edit_link = driver.find_element_by_xpath(edit_path)
            edit_link.click()

            wait.until(EC.url_contains("edit"))

            minecraft_path = "/html/body/div[2]/div/div/div[1]/nav/div[2]/div[3]/div[2]/div/a"
            wait.until(EC.element_to_be_clickable((By.XPATH, minecraft_path)))
            minecraft_link = driver.find_element_by_xpath(minecraft_path)
            action = ActionChains(driver)
            action.move_to_element(minecraft_link).click().perform()
            action.move_to_element(minecraft_link).click().perform()

            export_path = "//*[contains(text(), 'Export')]" 
            export_button = driver.find_element_by_xpath(export_path).find_element_by_xpath("..")
            action.move_to_element(export_button).click().perform()


       except exceptions.TimeoutException as error:
           print(f"user: {user} does not have design { args.design}")