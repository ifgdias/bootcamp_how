#%%
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

import time
#%%

log_path = "./tmp/geckodriver.log"
capabilities = DesiredCapabilities.FIREFOX
capabilities["marionette"] = True
firefox_bin = "/usr/bin/firefox"

options = Options()
options.headless = False  # If you want to enable headless mode.

browser = webdriver.Firefox(
    firefox_binary=firefox_bin, capabilities=capabilities, options=options)

print('opening the page', browser)
browser.get("https://www.globo.com")
html = browser.page_source
print('returned html size: ', len(html))
open('gecko_test_wsl.html', 'w').write(html)  # See the html if you want.

time.sleep(10)

browser.close()
# %%
