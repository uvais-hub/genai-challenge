from selenium import webdriver


driver = webdriver.Chrome()

driver.get("https://the-internet.herokuapp.com/")
driver.back()
driver.forward()
driver.refresh()