from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import argparse
import os

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--names")
parser.add_argument("--design")
parser.add_argument("--username")
parser.add_argument("--password")
args = parser.parse_args()

names_file = args.names
password = args.password
cad_file = args.design
username=args.username

binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.preferences.instantApply",True)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
fp.set_preference("browser.helperApps.alwaysAsk.force",False)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.folderList",0)
browser = webdriver.Firefox(firefox_profile=fp, firefox_binary=binary)
wait = WebDriverWait(browser, 5)
base_path = "https://www.tinkercad.com/users/"
login_path = "https://www.tinkercad.com/login"
browser.get(login_path)

def login_by_username():
    # LOGIN BUTTON
    login_button_path = "/html/body/div/div/app/div/div/main/ng-component/main/div/div[1]/a[2]"
    # wait until login button is loaded
    wait.until(EC.presence_of_element_located((By.XPATH, login_button_path))) 
    login_button = browser.find_element_by_xpath(login_button_path)
    action = ActionChains(browser)
    # click on login button
    action.move_to_element(login_button).click().perform()
def enter_username(username):
    # USERNAME INPUT
    username_input_path = '//*[@id="userName"]'
    # wait until username input box is loaded
    wait.until(EC.presence_of_element_located((By.XPATH, username_input_path)))
    username_input = browser.find_element_by_xpath(username_input_path)
    # input username
    username_input.send_keys(username)
    # submit username
    browser.find_element_by_xpath('//*[@id="verify_user_btn"]').click()
def enter_password(password):
    # PASSWORD INPUT
    password_input_path = '//*[@id="password"]'
    # wait until password input box is loaded
    wait.until(EC.element_to_be_clickable((By.XPATH, password_input_path)))
    password_input = browser.find_element_by_xpath(password_input_path)
    # click on password box to enable it
    password_input.click()
    # input password
    password_input.send_keys(password)
    # submit password
    browser.find_element_by_xpath('//*[@id="btnSubmit"]').click()

login_by_username()
enter_username(username)
enter_password(password)
wait.until(EC.url_matches("https://www.tinkercad.com"))
with open(names_file, 'r') as file:
   for user in file.readlines():
       browser.get(base_path + user)
       try:
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, cad_file)))
            design_link = browser.find_element_by_link_text(cad_file)
            design_link.click()

            edit_path = "//*[contains(text(), 'Copy and Tinker')]" 
            wait.until(EC.url_contains("things"))
            edit_link = browser.find_element_by_xpath(edit_path)
            edit_link.click()

            wait.until(EC.url_contains("edit"))
            print("made it to the edit page")

            minecraft_path = "/html/body/div[2]/div/div/div[1]/nav/div[2]/div[3]/div[2]/div/a"
            print("waiting for mc clickable")
            wait.until(EC.element_to_be_clickable((By.XPATH, minecraft_path)))
            minecraft_link = browser.find_element_by_xpath(minecraft_path)
            action = ActionChains(browser)
            print("clicking on mc")
            action.move_to_element(minecraft_link).click().perform()
            action.move_to_element(minecraft_link).click().perform()

            export_path = "//*[contains(text(), 'Export')]" 
            wait.until(EC.visibility_of_element_located((By.XPATH, export_path)))
            # get the parent element which is a link
            export_button = browser.find_element_by_xpath(export_path).find_element_by_xpath("..")
            action.move_to_element(export_button).click().perform()


       except exceptions.TimeoutException as error:
           print(f"user: {user} does not have design {cad_file}")