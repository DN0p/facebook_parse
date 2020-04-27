import csv
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

with open('credentials.txt') as f:
    BROWSER_EXE = f.readline().split('"')[1]
    GECKODRIVER = f.readline().split('"')[1]
    email = f.readline().split('"')[1]
    password = f.readline().split('"')[1]
    path = f.readline().split('"')[1]

    if email == "" or password == "":
        print(
            "Your email or password is missing. Kindly write them in credentials.txt")
        exit()

FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)
PROFILE = webdriver.FirefoxProfile()
PROFILE.set_preference("dom.webnotifications.enabled", False)
PROFILE.set_preference("app.update.enabled", False)
PROFILE.update_preferences()

browser = webdriver.Firefox(executable_path=GECKODRIVER,
                            firefox_binary=FIREFOX_BINARY,
                            firefox_profile=PROFILE, )
browser.maximize_window()
browser.get('https://www.facebook.com/')
browser.find_element_by_name('email').send_keys(email)
browser.find_element_by_name('pass').send_keys(password)
login_button = browser.find_element_by_id('loginbutton')

login_button.click()


def exceptions(xpath, index):
    time.sleep(5)
    element_list = browser.find_elements(By.XPATH, xpath)
    element_list[index].click()


def clear_comment(href):
    if 'php' in href:
        part_for_delete = href.find('&')
        user_id = href[24:part_for_delete]
        return user_id
    else:
        part_for_delete = href.find('?')
        user_id = href[24:part_for_delete]
        return user_id


def comments_post(comments):
    comment = ''
    for comm in comments:
        full_comment = comm.get_attribute('href')
        comment += (clear_comment(full_comment)) + ','
    return comment


def click_void():
    ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    time.sleep(2)


def like_click():
    try:
        wait_list_and_click("//a[@class='_3dlf']", -1)
        time.sleep(5)

        all_reactions = browser.find_elements_by_xpath("//a[@class='_5i_s _8o _8r lfloat _ohe']")
        clean_likes_id = get_all_likes(all_reactions)

        wait_and_click("//a[@data-testid='reactions_profile_browser:close']")
        return clean_likes_id
    except:
        return 'No Likes'


def get_all_likes(react):
    likes = ''
    for rec in react:
        like_id = rec.get_attribute('href')
        likes += (clear_comment(like_id)) + ','
    return likes


def click_shared():
    try:
        wait_list_and_click("//a[@class='_3rwx _42ft']", -1)
        time.sleep(5)

        all_reposts = browser.find_elements_by_xpath("//div[@class='_4-i2 _pig _5ki2 _50f4']//span[@class='fwb fcg']/a")
        clean_repost_id = get_all_shared(all_reposts)

        wait_and_click("//a[@data-testid='dialog_title_close_button']")

        return clean_repost_id
    except:
        return 'No reposts'


def get_all_shared(share):
    repost = ''
    for rep in share:
        share_id = rep.get_attribute('href')
        repost += (clear_comment(share_id)) + ','
    return repost


def get_location(href):
    try:
        location = href[2].get_attribute("textContent")
        return location
    except:
        return 'No Location'


def create_write_csv(path):
    with open(path, 'w', newline='') as csv_file:
        csv_file.write('Ссылка на пост;Локация;Дата публикации;Видимость;ID кто прокомментировал запись;ID кто '
                       'лайкнул запись;ID кто сделал репост\n')


def append_csv(data, path):
    with open(path, 'a+', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(data)


def wait_and_click(xpath):
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

    element.location_once_scrolled_into_view

    actions = ActionChains(browser)
    actions.move_to_element(element).perform()
    actions.click().perform()


def wait_list_and_click(xpath, index):
    element = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    element[index].location_once_scrolled_into_view

    actions = ActionChains(browser)
    actions.move_to_element(element[index]).perform()
    actions.click().perform()


create_write_csv(path)


def scroll_and_click_grid_element(elem):
    elem.location_once_scrolled_into_view

    actions = ActionChains(browser)
    actions.move_to_element(elem).perform()
    actions.click().perform()

    time.sleep(5)


user_page = '//a[@class="_2s25 _606w"]'
exceptions(user_page, -1)

user_grid = "//a[@class='_4jy0 _4jy4 _517h _51sy _42ft']"
exceptions(user_grid, -1)

your_posts = "//a[@class='_1xx7 _1xx8 _2pi2']"
exceptions(your_posts, 0)

all_data_users = []

time.sleep(3)
all_posts = browser.find_elements_by_xpath("//td[contains(@class,'_2pij _2pio _51m')]")

for i in all_posts:
    if i == all_posts[-1]:
        break
    else:
        data_post = []

        elements = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//td[contains(@class,'_2pij _2pio _51m')]")))

        scroll_and_click_grid_element(i)

        post_link = browser.find_elements_by_class_name("_5pcq")[-1].get_attribute('href')
        data_post.append(post_link)

        profile_link = browser.find_elements_by_xpath('//a[@class="profileLink" and not(@title)]')
        data_post.append(get_location(profile_link))

        published_date = browser.find_elements_by_class_name("_5ptz")[-1].get_attribute('title')
        data_post.append(published_date)

        visibility = browser.find_elements_by_xpath(
            '//a[contains(@class,"_42ft _4jy0 _55pi _5vto _55_p _2agf _4o_4 _401v _p _1zg8")]')[-1].get_attribute(
            'aria-label')
        data_post.append(visibility)

        user_comments = browser.find_elements_by_xpath("//div[@class='_72vr']//a[@class='_6qw4']")[3:]
        if len(user_comments) > 0:
            data_post.append(comments_post(user_comments))
        else:
            data_post.append('No comments')

        data_post.append(like_click())

        data_post.append(click_shared())

        all_data_users.append(data_post)

        wait_and_click("//div[contains(@class, 'uiOverlayFooter')]//a[contains(@class, 'layerCancel uiOverlayButton')]")

        append_csv(data_post, path)

        click_void()

browser.quit()

