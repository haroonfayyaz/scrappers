import time
import pandas as pd
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def createFile(data, fileName):
    print("fileName: ", fileName)
    with open('{}.csv'.format(fileName), 'w') as f:
        write = csv.writer(f)
        write.writerows(data)


def checkSingleNumbers(driver, bondNumbers):
    for num in bondNumbers:
        numberField = driver.find_element_by_id("txtNumber")
        numberField.send_keys(num)
        time.sleep(1)

        addBtn = driver.find_element(by=By.CLASS_NAME, value="btn_add")
        addBtn.click()
        time.sleep(1)

    time.sleep(1)


def checkSeriesNumbers(driver, bondNumbers):
    for num in bondNumbers:
        fromNum = driver.find_element_by_id("txtFrm")
        fromNum.send_keys(num[0])
        time.sleep(1)

        toNum = driver.find_element_by_id("txtTo")
        toNum.send_keys(num[1])
        time.sleep(1)

        addBtn = driver.find_element(by=By.CLASS_NAME, value="btn_add")
        addBtn.click()
        time.sleep(1)

    time.sleep(1)


def selectDomination(driver, bondValue):
    i = 0
    while True and i < 3:
        try:
            expand_element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'PageContent_ddPB')))
            expand_element.click()

            time.sleep(1)
            select = Select(driver.find_element_by_id('PageContent_ddPB'))
            select.select_by_value(bondValue)
            time.sleep(2)
            # if len(select.options) > 0:
            #     select.options[2].click()

            for option in select.options:
                if option.get_attribute("value") == bondValue:
                    option.click()
                    break
            draw = Select(driver.find_element_by_id('PageContent_ddDraws'))
            draw.select_by_value("")
            break
        except:
            i += 1
            continue
    time.sleep(1)


def clickCheckBtn(driver):
    checkBtn = driver.find_element(by=By.CLASS_NAME, value="btn_check")
    checkBtn.click()
    time.sleep(3)


def parseResults(driver, bondValue, type):
    table_data = driver.find_elements(
        By.XPATH, '//*[@id="result"]/table/tbody/tr')

    rows = []
    for row in table_data:
        # Use dot in the xpath to find elements with in element.
        columns = row.find_elements(By.XPATH, "./td")
        table_row = []
        for column in columns:
            table_row.append(column.text)
        rows.append(table_row)

    createFile(rows, "bond_result_{}_{}".format(bondValue, type))


def readFileData():
    df = pd.read_excel (r'LIST.xlsx')
    print (df)

if __name__ == '__main__':
    readFileData()
    # driver = webdriver.Chrome("/Users/apple/Downloads/chromedriver")

    # url = 'https://hamariweb.com/finance/prizebonds/'
    # driver.get(url)

    # bondValue = "750"

    # selectDomination(driver, bondValue)


    # checkSingleNumbers(driver, bondNumbers)

    # clickCheckBtn(driver)
    # parseResults(driver, bondValue, "single")

    # driver.close()
