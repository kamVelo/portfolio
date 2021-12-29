from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.headless = True

driver = Chrome(options=opts)
driver.get("https://coolors.co/generate")
print(driver.current_url)