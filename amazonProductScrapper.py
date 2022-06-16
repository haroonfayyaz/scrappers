import time
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome("/Users/apple/Downloads/chromedriver")

url = 'https://www.amazon.com/Moisturizer-Hydrating-Moisturizing-Non-Comedogenic-Non-Greasy/dp/B099N1LC4R/?_encoding=UTF8&pd_rd_w=yAFNe&content-id=amzn1.sym.78a9bb32-e95c-4d94-bff2-386a1bc8fd49&pf_rd_p=78a9bb32-e95c-4d94-bff2-386a1bc8fd49&pf_rd_r=NX3RDABEZF4H8S2DJXW7&pd_rd_wg=gXw0D&pd_rd_r=9211bbb0-60ba-45dd-9103-55aac0aab0e5&ref_=pd_gw_trq_ed_tb8bjdoo'
driver.get(url)

qtyRequired = 3

assert "amazon.com" in driver.title.lower()

title = driver.find_element_by_id("productTitle").text
price = driver.find_element_by_id("sns-base-price").text.strip().split("\n")[0].strip()

stock = driver.find_element_by_css_selector("#availability>span").text.strip()

assert "in stock" in stock.lower()


qtyButton = driver.find_element_by_css_selector("#selectQuantity > span > div > div > span").click()
time.sleep(2)
selectedQty = driver.find_element_by_id("quantity_{}".format(qtyRequired - 1)).click()
time.sleep(2)
buyNow = driver.find_element_by_id("buy-now-button").click()
time.sleep(2)



print("title: ", title)
print("price: ", price)
print("stock: ", stock)
# print("stock: ", stock)

driver.close()



