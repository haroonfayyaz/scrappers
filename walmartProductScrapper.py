import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome("/Users/apple/Downloads/chromedriver")
productLink = "https://www.walmart.com/ip/Great-Value-2-Reduced-Fat-Milk-128-Fl-Oz/10450115?athcpid=10450115&athpgid=AthenaHomepageDesktop__gm__-1.0&athcgid=null&athznid=bs&athieid=v0&athstid=CS020&athguid=7yicfUx1h1SxX25udTUslHIM7Igqmzrq7g6b&athancid=null&athena=true"
driver.get(productLink)
print("title: ", driver.title)
# assert "Walmart.com" in driver.title
time.sleep(3)
# elem = driver.find_element(by=By.XPATH, value='//*[@id="intent-banner-section"]/button/div/div[1]/i')
try:
  element = driver.find_element(by=By.CSS_SELECTOR, value="#px-captcha")
  print("Element: ", element)
  action = ActionChains(driver)
  click = ActionChains(driver)
  action.click_and_hold(element)
  print("after click and hold")
  action.perform()
  print("action performed")
  time.sleep(10)
  print("after sleep")
  action.release(element)
  action.perform()
  time.sleep(2)
  action.release(element)
  time.sleep(5)
except:
  print("action failed")


try:
  elem = driver.find_element(by=By.XPATH, value='//*[@id="intent-banner-section"]/button/div/div[1]/i')
  elem.click()
  time.sleep(5)
except:
  print("action 2 failed")

# driver.close()

