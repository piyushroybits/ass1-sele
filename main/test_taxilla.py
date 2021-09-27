
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def load_driver(browser):
    # create webdriver object
    if browser == 'firefox':
        return webdriver.Firefox()
    elif browser == "chrome":
        return webdriver.Chrome()
    else:
        return None


def launch_url(driver, url):
    driver.get(url)


def find_element_by_id(driver, id):
    return driver.find_element_by_id(id)


def find_element_by_class(driver, class_name):
    return driver.find_element_by_class_name(class_name)


def enter_text(element, text):
    element.send_keys(text)


def click(driver, button_name):
    element = find_element_by_id(driver, button_name)
    element.click()


def get_page_content(driver, id):
    try:
        page_content = find_element_by_id(driver, id)
        return page_content
    except NoSuchElementException:
        return None


def get_element_if_none(driver, id):
    element = None
    while element is None:
        element = get_page_content(driver, id)
        print("Waiting for page load after login")
        time.sleep(1)
    return element


def verify_navigation(page_content):
    content = page_content.find_element_by_id("block-region-side-pre").find_element_by_class_name("content")
    items = content.find_elements(By.XPATH, "ul/li/ul/li")
    count = 0
    for item in items:
        if "type_system depth_2 contains_branch" == item.get_attribute("class"):
            for course in item.find_elements(By.XPATH, "ul/li"):
                print(course.text)
                count = count + 1
    assert count > 0
    return count


def verify_course_list(page_content):
    main_content = page_content.find_element_by_class_name("course_list")
    courses = main_content.find_elements(By.XPATH, "div")
    count = 0
    for course in courses:
        course_element = course.find_element_by_xpath("div/h2/a")
        print("Name={} Link={}".format(course_element.text, course_element.get_attribute("href")))
        count = count + 1
    assert count > 0
    return count


def verify_user_list(page_content):
    users = page_content.find_element_by_xpath("aside/div[2]/div[2]/ul").find_elements(By.XPATH, "li")
    print("Numbers of Users online {}".format(len(users)))
    count = 0
    for user in users:
        print(user.text)
        count = count + 1
    assert count > 0
    return count


def site_login(browser, username, password):
    login = find_element_by_id(browser, "login")
    user_field = find_element_by_id(login, "username")
    pass_field = find_element_by_id(login, "pass")
    # Enter Credentials
    enter_text(user_field, username)
    enter_text(pass_field, password)
    click(browser, "submitbtn")


def launch_test_browser(browser_name, url, username, password):
    begin = time.time()
    browser = load_driver(browser_name)
    launch_url(browser, url)
    site_login(browser, username, password)
    page_content = get_element_if_none(browser, "page-content")
    count_navi = verify_navigation(page_content)
    count_courses = verify_course_list(page_content)
    assert count_navi == count_courses
    verify_user_list(page_content)
    browser.close()
    end = time.time()
    print("Total runtime of the program for browser={} is {}".format(browser_name, end - begin))


if __name__ == '__main__':
    """
    You need to showcase following tasks:
    
    Navigate to the website
    Login to the portal (login form can be on the different window, or as a dropdown, or as a pop-up)
    Showcase interaction with the Dynamic and Static elements
    Extract web elements such as table or list
    Usage of locator types, whether to use CSS selector or Xpath
    How above variation effects performance of the testing
    Usage of Dynamic Xpath or tags vs Static Xpath
    Need of thread.sleep() functionality, in case of loading page or waiting for search results
    Can same selenium test work in different browsers (chrome or IE)
    Exception handling in case webpage does not load properly as expected
    Bonus point: Measure the performance in terms of time investment for Manual Vs Automated Testing
    """

    url = "http://taxila-aws.bits-pilani.ac.in"
    username = "email"
    password = "pass"

    # Assumption is Chrome and Firefox browsers are installed
    launch_test_browser("chrome", url, username, password)
    launch_test_browser("firefox", url, username, password)
