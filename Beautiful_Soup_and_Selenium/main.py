from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import bs4
import re
import csv


driver = webdriver.Chrome()
driver.get("https://ieeexplore.ieee.org/Xplore/home.jsp")
res_list = []


def parse_info(input_string):
    # Define the regular expression pattern
    pattern1 = r'Year: (\d{4}) \| Volume: (\d+), Issue: (\d+) \| ([^|]+) \| Publisher: ([^|]+)'
    # pattern1 -> full
    pattern2 = r'Year: (\d{4}) \| (Volume: (\d+), )?((Issue: (\d+), )?)([^|]+) \| Publisher: (.+)'
    # pattern2 -> no volume and issue
    pattern3 = r'Year: (\d{4}) \| Volume: (\d+) \| ([^|]+) \| Publisher: ([^|]+)'
    # pattern3 -> no issue
    # Use re.search to find the pattern in the input string
    match1 = re.search(pattern1, input_string)

    if match1:
        # Extract information from the matched groups
        year = match1.group(1)
        volume = match1.group(2) or '0'  # If no volume, set to '0'
        issue = match1.group(3) or '0'  # If no issue, set to '0'
        paper = match1.group(4).strip()
        publisher = match1.group(5).strip()

        return {
            'Year': year,
            'Volume': volume,
            'Issue': issue,
            'Paper': paper,
            'Publisher': publisher
        }
    else:
        match2 = re.search(pattern2, input_string)
        if match2:
            # Extract information from the matched groups
            year = match2.group(1)
            volume = match2.group(3) or '0'  # If no volume, set to '0'
            issue = match2.group(6) or '0'  # If no issue, set to '0'
            paper = match2.group(7).strip()
            publisher = match2.group(8).strip()

            return {
                'Year': year,
                'Volume': volume,
                'Issue': issue,
                'Paper': paper,
                'Publisher': publisher
            }
        else:
            match3 = re.search(pattern3, input_string)
            if match3:
                # Extract information from the matched groups
                year = match3.group(1)
                volume = match3.group(2) or '0'  # If no volume, set to '0'
                issue = '0'  # If no issue, set to '0'
                paper = match3.group(3).strip()
                publisher = match3.group(4).strip()

                return {
                    'Year': year,
                    'Volume': volume,
                    'Issue': issue,
                    'Paper': paper,
                    'Publisher': publisher
                }
            else:
                return None


# Check if the element exists
def check_exists(path):
    try:
        driver.find_element(By.CLASS_NAME, path)
    except NoSuchElementException:
        return False
    return True


# Wait for the element to show up
def wait_for_element():
    delay = 10
    try:
        # Wait for the element with the ID of wrapper
        wrapper = WebDriverWait(driver, delay).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'text-md-md-lh'))
        )
        print("Element is present in the DOM now... You can crawl the thing that you want.")
    except TimeoutException:
        print("Element did not show up")
    # use BeautifulSoup to parse the source of the page
    source = bs4.BeautifulSoup(driver.page_source, "lxml")
    title_list = []
    # Get the title of all the papers
    for title in source.find_all("h3", class_="text-md-md-lh"):
        title_list.append(title.text.strip())
    idx = int(0)
    sw = True
    # Get the information of all the papers
    for detail in source.find_all("div", class_="publisher-info-container"):
        if not sw:
            sw = True
            continue
        text = parse_info(detail.text.strip())
        res = {'Title': title_list[idx]}
        idx += 1
        # Merge the two dictionaries, Title and the information of the paper
        res.update(text)
        sw = False
        # Append the result to the list
        res_list.append(res)
    sleep(1)


# input the keyword and search
element = driver.find_element(By.CLASS_NAME, "Typeahead-input")
element.send_keys("Minecraft")
sleep(0.5)
element.send_keys(Keys.ENTER)
wait_for_element()

for i in range(2, 100):
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Click the next button, if there is no next button, break the loop
    if not check_exists("stats-Pagination_arrow_next_" + str(i)):
        break
    driver.find_element(By.CLASS_NAME, "stats-Pagination_arrow_next_" + str(i)).click()
    wait_for_element()
    sleep(1)

print("Crawling is done. Writing the file into file.csv...")

csv_file = 'file.csv'
# Define the fields of the csv file
fields = ['Title', 'Year', 'Volume', 'Issue', 'Paper', 'Publisher']
# Write the csv file
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(res_list)

sleep(1)
print("Writing the file is done.")

driver.close()
