import time
import random
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.options import Options as FirefoxOptions

Max_Time = 45  # maximale aufrufzeit in sekunden

TIMEOUT = random.randint(35, Max_Time)

THREAD_COUNT = 1  # gleichzeitig geöffnete browserfenster

c = 1  # zum zählen der Aufrufe


def load_session(url):  # Browser einrichten

    # options = FirefoxOptions()
    # options.add_argument("--headless")
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks", "127.0.0.1")
    profile.set_preference("network.proxy.socks_port", 9050)
    profile.set_preference("network.proxy.socks_version", 5)
    profile.set_preference("media.volume_scale", "0.0")
    profile.update_preferences()
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.set_page_load_timeout(20)

    try:  # YouTube Video aufrufen
        driver.get("https://youtube.com")
        time.sleep(3)
        driver.get(url)
        try:

         WebDriverWait(driver, 5).until(
             ec.element_to_be_clickable((By.XPATH,
                                         '/html/body/ytd-app/ytd-popup-container/paper-dialog/yt-upsell-dialog-renderer/div/div[3]/div[1]/yt-button-renderer/a/paper-button/yt-formatted-string'))).click()
         driver.switch_to.frame(0)
         WebDriverWait(driver, 10).until(ec.element_to_be_clickable(
             (By.XPATH, "/html/body/div/c-wiz/div[2]/div/div/div/div/div[2]/form/div/span/span"))).click()
         time.sleep(TIMEOUT)
         driver.quit()
        except:

            actions = ActionChains(driver)
            actions.send_keys("k")
            actions.perform()
            moves = [Keys.DOWN, Keys.UP]
            for i in range(5):
                driver.find_element_by_css_selector('body').send_keys(random.choice(moves))
                time.sleep(0.3)
            time.sleep(TIMEOUT)
            try:

             action = ActionChains(driver)
             playnext = driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[2]/div/div[3]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[1]")
             action.move_to_element(playnext).perform()
             playnextclick = driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[2]/div/div[3]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[1]")
             playnextclick.click()
             time.sleep(3)
            finally:

             driver.quit()

    except:
        driver.quit()
        raise Exception("Website konnte nicht geladen werden")

def main(url):
    global c
    while True:
        try:
            load_session(url)
            print("Generierte Aufrufe:", c)
            c += 1
        except Exception as e:
            print("Wiederhole weil:", str(e))


if __name__ == "__main__":
    url = input("Video url:")
    threads = []
    for i in range(THREAD_COUNT):
        thread = threading.Thread(target=main, args=(url,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

