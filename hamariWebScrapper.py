import time
from datetime import datetime


# Import pandas
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


def formatNum(num):
    num = str(num).replace('.', '')
    length = len(str(num))
    if length == 6:
        return num
    for i in range(6 - length):
        num = "0" + str(num)
    return num[:6]


def checkSingleNumbers(driver, bondNumbers):
    for num in bondNumbers:
        numberField = driver.find_element_by_id("txtNumber")
        numberField.send_keys(formatNum(num))
        time.sleep(0.3)

        addBtn = driver.find_element(by=By.CLASS_NAME, value="btn_add")
        addBtn.click()
        time.sleep(0.3)

    time.sleep(1)


def checkSeriesNumbers(driver, bondNumbers):
    for num in bondNumbers:
        frm, to = str(num).split("-")
        fromNum = driver.find_element_by_id("txtFrm")
        fromNum.send_keys(formatNum(frm))
        time.sleep(0.7)

        toNum = driver.find_element_by_id("txtTo")
        toNum.send_keys(formatNum(to))
        time.sleep(0.7)

        addBtn = driver.find_element(by=By.CLASS_NAME, value="btn_add")
        addBtn.click()
        time.sleep(0.7)

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
    time.sleep(0.8)


def clickClearBtn(driver):
    clearBtn = driver.find_element(by=By.CLASS_NAME, value="btn_clear")
    clearBtn.click()
    time.sleep(0.8)


def clickRadioBtn(driver, name):
    radioBtn = driver.find_element(by=By.ID, value=name)
    radioBtn.click()
    time.sleep(0.8)


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

    if(len(rows) > 2 and rows[2][0] != "Sorry No Win"):
        createFile(rows, "bond_result_{}_{}_{}".format(
            bondValue, type, datetime.now().strftime("%m_%Y_%H_%M_%S")))


def readFileData(bondValue):
    # Assign spreadsheet filename to `file`
    file = 'LIST.csv'
    data = pd.read_csv(file, low_memory=False, skiprows=1)
    # data.columns = data.columns.str.strip()
    cols = list(data)
    print(cols)

    # Load spreadsheet
    # suffix = ".2"
    suffix = ""
    colName = "RS {:,}{}".format(int(bondValue), suffix)
    if colName not in cols:
        return [], []

    numbers = [x for x in data[colName] if str(x) != 'nan']

    print("Numbers: ", numbers)
    single = []
    series = []
    for number in numbers:
        if "-" in str(number):
            series.append(str(number).strip())
        else:
            single.append(str(number).strip())

    return single, series


if __name__ == '__main__':
    SINGLE = "single"
    SERIES = "series"

    driver = webdriver.Chrome("/Users/apple/Downloads/chromedriver")
    url = 'https://hamariweb.com/finance/prizebonds/'
    driver.get(url)

    # 100, 200, 750

    for bondValue in ["100", "200", "750", "1500", "7500", "15000", "25000", '40000']:
        single, series = readFileData(bondValue)

        selectDomination(driver, bondValue)

        for bond in [(single, SINGLE), (series, SERIES)]:
            nums, type = bond

            if type == SINGLE:
                if(len(nums) == 0):
                    break
                clickRadioBtn(driver, "radio_input")
                clickClearBtn(driver)
                checkSingleNumbers(driver, nums)
            else:
                if(len(nums) == 0):
                    break
                clickRadioBtn(driver, "radio_input_2")
                clickClearBtn(driver)
                checkSeriesNumbers(driver, nums)

            clickCheckBtn(driver)
            parseResults(driver, bondValue, type)

    driver.close()
