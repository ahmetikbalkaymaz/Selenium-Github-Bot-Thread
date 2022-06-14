from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from user_info import username, password
from threading import Thread
import pandas as pd

baseUrl = "https://github.com/"

driver_path = "/Users/ahmetikbalkaymaz/Documents/Drivers/chromedriver"


def signIn():
    driver = webdriver.Chrome(driver_path)
    driver.get(baseUrl+"login")
    usernameInput = driver.browser.find_element(by=By.NAME, value="login")
    usernameInput.send_keys(username)
    passwordInput = driver.find_element(by=By.NAME, value="password")
    passwordInput.send_keys(password)
    btn = driver.find_element(by=By.NAME, value="commit")
    btn.click()

def findRepositories():
    driver = webdriver.Chrome(driver_path)
    driver.get(baseUrl)
    searchInput = driver.find_element(by=By.NAME, value="q")
    searchInput.send_keys("python")
    searchInput.send_keys(Keys.ENTER)

    repos = driver.find_elements(by=By.CSS_SELECTOR, value=".repo-list-item")
    repoNames = []
    repoLinks = []
    desc = []
    for repo in repos:
        anchor = repo.find_elements(by=By.TAG_NAME, value="a")[0]
        paragraf = repo.find_elements(by=By.TAG_NAME, value="p")[0]
        repoName = anchor.text
        repoLink = anchor.get_attribute('href')
        description = paragraf.text
        repoNames.append(repoName)
        repoLinks.append(repoLink)
        desc.append(description)

        r = {
            "name": repoNames,
            "description": desc,
            "link": repoLinks
        }
        df1 = pd.DataFrame(r)
        df1.to_csv("repos.csv")
    driver.close()
    # return repoNames, repoLinks, desc


def loadFollowers():
    driver = webdriver.Chrome(driver_path)
    driver.get(f"{baseUrl}{username}?tab=followers")
    items = driver.find_elements(by=By.CSS_SELECTOR, value=".d-table.table-fixed")
    names_user = []
    nickname = []
    for item in items:
        name = item.find_elements(by=By.TAG_NAME, value="div")[1].find_elements(by=By.TAG_NAME, value="span")[
            0].text
        usernames = item.find_elements(by=By.TAG_NAME, value="div")[1].find_elements(by=By.TAG_NAME, value="span")[
            1].text

        names_user.append(name)
        nickname.append(usernames)

        names = {
            "name": names_user,
            "username": nickname
        }

        df2 = pd.DataFrame(names)
        df2.to_csv('follower.csv')
    # return names_user, nickname


def prog_language(driver, username):
    driver.get(f"{baseUrl}{username}?tab=repositories")

    repos = driver.find_elements(by=By.CSS_SELECTOR, value=".py-4")
    reposito = []
    user = []
    for i in range(len(repos)):
        lang = driver.find_elements(by=By.XPATH, value='//span[@itemprop="programmingLanguage"]')[i - 1]
        language = lang.text

        reposito.append(language)
        user.append(username)

        repo = {
            "user": user,
            "language": reposito
        }
        df2 = pd.DataFrame(repo)
        df2.to_csv('reposito.csv')


# deneme(webdriver.Chrome(driver_path), "TurkishCodeMan")

user_list = ["TurkishCodeMan", "ahmetikbalkaymaz", "YildirimSelahattin"]

for i in range(len(user_list)):
    browserThread = Thread(target=prog_language, args=(webdriver.Chrome(driver_path), user_list[i],))
    browserThread.start()


def run_threaded(job_func):
    job_threaded = Thread(target=job_func)
    job_threaded.start()
    #job_threaded.join()

run_threaded(loadFollowers)
run_threaded(findRepositories)