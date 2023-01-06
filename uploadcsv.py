# coding: UTF-8
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv
from datetime import datetime

def upload_csv(csv_file, group)

  mf_url = "https://moneyforward.com/"
  mf_input_url = "https://moneyforward.com/cf#cf_new"
  username = "Your Username"
  password = "Your Password"

  try:
    # Open Moneyforward
    driver = webdriver.Chrome('./bin/chromedriver')
    driver.implicitly_wait(10)
    driver.get(mf_url)
    driver.implicitly_wait(10)
    elem = driver.find_elements_by_link_text("ログイン")
    elem[0].click()
    driver.implicitly_wait(10)
    elem = driver.find_elements_by_link_text("メールアドレスでログイン")
    elem[0].click()
    driver.implicitly_wait(10)
  
    # Login to moneyforward
    elem = driver.find_element_by_name("mfid_user[email]")
    elem.clear()
    elem.send_keys(username)
    elem.submit()
    driver.implicitly_wait(10)
    elem = driver.find_element_by_name("mfid_user[password]")
    elem.clear()
    elem.send_keys(password)
    elem.submit()

    # Select group
    elem = driver.find_element_by_id("group_id_hash").click()
    sleep(1)
    elem = driver.find_element_by_xpath("//a[text()='" + group + "' and @class='l_c_name']").click()
    sleep(5)

    # Open CSV file
    f = open(csv_file, mode='r', encoding='utf-8')
    reader = csv.reader(f)
    driver.get(mf_input_url)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submit-button")))

    for row in reader:

      # row[x] = [Date, Content, Price, Large-category, Middle-category, Asset_name]

      # Input Price
      if int(row[2]) > 0:
        # Move to income tab
        driver.find_element_by_class_name("plus-payment").click()
      elif int(row[2]) < 0:
        # Default is outcome tab
      else:
        print("Price at row " + str(count) + " has invalid format!")

      elem = driver.find_element_by_id("appendedPrependedInput")
      elem.clear()
      elem.send_keys(abs(int(row[2])))

      # Input date
      elem = driver.find_element_by_id("updated-at")
      elem.clear()
      elem.send_keys(row[0])

      # Select asset
      driver.find_element_by_id("user_asset_act_sub_account_id_hash").click()
      sleep(1)
      driver.find_element_by_xpath("//a[text()='" + row[5] + "' and @class='l_c_name']").click()

      # Input large-category
      driver.find_element_by_id("js-large-category-selected").click()
      sleep(1)
      driver.find_element_by_xpath("//a[text()='" + row[3] + "' and @class='l_c_name']").click()
      sleep(1)

      # Input middle-category
      driver.find_element_by_id("js-middle-category-selected").click()
      sleep(1)
      driver.find_element_by_xpath("//a[text()='" + row[4] + "' and @class='m_c_name']").click()
      sleep(1)

      # Input content
      elem = driver.find_element_by_id("js-content-field")
      elem.clear()
      elem.send_keys(row[1])

      # Save
      driver.find_element_by_id("submit-button").click()
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "confirmation-button")))
      driver.find_element_by_id("confirmation-button").click()
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submit-button")))
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "plus-payment")))
      
      count+=1

    f.close()
    print(csv_file + "was successfully uploaded!")
    driver.quit()
    return 0

  except ValueError:
    print("Error!")
    return 1

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("Usage: python updatecsv.py data.csv group")
    sys.exit()

  csv_file = str(sys.argv[1])
  group = str(sys.argv[2])
  sys.exit(upload_csv(csv_file, group))