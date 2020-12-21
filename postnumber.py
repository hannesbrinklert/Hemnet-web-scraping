from selenium import webdriver
from urllib3 import disable_warnings

def getPostNumber(str):
    options = webdriver.ChromeOptions()
    #This path has to be modified for your own computer.
    driver = webdriver.Chrome(
        options=options, executable_path="C:/Windows/ChromeDriver/chromedriver.exe")
    driver.get('https://www.postnord.se/vara-verktyg/sok-postnummer-och-adress')

    driver.implicitly_wait(2)

    submit_button1 = driver.find_elements_by_xpath(
        '//*[@id="onetrust-accept-btn-handler"]')[0]
    submit_button1.click()

    # type text
    text_area = driver.find_element_by_id("SearchAddressAndPostalCode-query")
    text_area.send_keys(str + ", stockholm")

    driver.implicitly_wait(5)

    submit_button = driver.find_elements_by_xpath(
        '//*[@id="form-SearchAddressAndPostalCode"]/fieldset/div/div[3]/button')[0]
    submit_button.click()

    driver.implicitly_wait(2)
    text = ""
    try:
        text = driver.find_element_by_xpath(
            '//html/body/section/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[2]/div/table/tbody/tr/td[3]').text
    except:
        text = "00000"

    driver.close()
    return text
