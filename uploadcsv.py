# coding: UTF-8
import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.support.select import Select
from time import sleep

def upload_csv(csv_file, group):

  mf_url = "https://moneyforward.com/"
  mf_input_url = "https://moneyforward.com/cf#cf_new"
  username = "Your Username"
  password = "Your Password"

  try:
    # Open Moneyforward
    chrome_service = fs.Service(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=chrome_service)
    driver.implicitly_wait(10)
    driver.get(mf_url)
    driver.implicitly_wait(10)
    elem = driver.find_element(By.LINK_TEXT, 'ログイン')
    elem.click()
    driver.implicitly_wait(10)
    elem = driver.find_element(By.LINK_TEXT, "メールアドレスでログイン")
    elem.click()
    driver.implicitly_wait(10)

    # Login to moneyforward
    elem = driver.find_element(By.NAME, "mfid_user[email]")
    elem.clear()
    elem.send_keys(username)
    elem.submit()
    driver.implicitly_wait(10)
    elem = driver.find_element(By.NAME, "mfid_user[password]")
    elem.clear()
    elem.send_keys(password)
    elem.submit()
    driver.implicitly_wait(10)

    # Select group
    elem = driver.find_element(By.ID, "group_id_hash")
    select=Select(elem)
    select.select_by_visible_text(group)
    driver.implicitly_wait(10)

    # Open CSV file
    with open(csv_file, mode='r', encoding='utf-8') as f:
      reader = csv.reader(f)
      driver.get(mf_input_url)
      element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submit-button")))

      for row in reader:
        # row[x] = [YYYY/MM/DD, Content, Price, Large-category, Middle-category, Asset_name]
        # Input Price
        if int(row[2]) < 0:
          # Move to income tab
          driver.find_element(By.CLASS_NAME, "plus-payment").click()
        elif int(row[2]) == 0:
          print("Price at row " + str(count) + " has invalid format!")

        elem = driver.find_element(By.ID, "appendedPrependedInput")
        elem.clear()
        elem.send_keys(abs(int(row[2])))
        sleep(1)

        # Input date
        elem = driver.find_element(By.ID, "updated-at")
        elem.clear()
        elem.send_keys(row[0])
        elem.click()
        sleep(1)
        elem.click()
        sleep(1)

        # Select asset
        elem = driver.find_element(By.ID, "user_asset_act_sub_account_id_hash")
        select=Select(elem)
        for option in select.options:
          if row[5] in option.text:
            select.select_by_visible_text(option.text)
        sleep(1)
        
        # Input large-category
        if row[3] != '':
          driver.find_element(By.ID, "js-large-category-selected").click()
          sleep(1)
          driver.find_element(By.XPATH, "//a[text()='" + row[3] + "' and @class='l_c_name']").click()
          sleep(1)

          # Input middle-category
          if row[4] != '':
            driver.find_element(By.ID, "js-middle-category-selected").click()
            sleep(1)
            driver.find_element(By.XPATH, "//a[text()='" + row[4] + "' and @class='m_c_name']").click()
            sleep(1)

        # Input content
        elem = driver.find_element(By.ID, "js-content-field")
        elem.clear()
        elem.send_keys(row[1])
        sleep(1)

        # Save
        driver.find_element(By.ID, "submit-button").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "confirmation-button")))
        driver.find_element(By.ID, "confirmation-button").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submit-button")))

        print('  ' + str(row) + ' was uploaded.')

    print(csv_file + " was uploaded!")
    driver.close()
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