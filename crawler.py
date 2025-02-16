from bs4 import BeautifulSoup
import requests
import queue
import time
import random
import os


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
}

#here we are getting the queue of all URLs from the main page
def get_content_main_page(url):
    response = requests.get(url, headers=headers)
    url_queue = queue.Queue()
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div_elements = soup.find_all('div', class_='col-100 col-sm-33 col-md-25')
        for div in div_elements:
            a_tag = div.find('a', href=True)
            if a_tag:
                href = a_tag['href']
                url_queue.put(href)
    else:
        print("error")
    return url_queue


def get_depth_0_urls(base_url):
    combined_queue = queue.Queue()

    # Initialize a variable to track the time of the previous request, to fool the webpage
    previous_request_time = time.time()

    for i in range(1, 25):
        url = f"{base_url}{i}"
        individual_queue = get_content_main_page(url)

        while not individual_queue.empty():
            combined_queue.put(individual_queue.get())

        current_time = time.time()
        time_elapsed = current_time - previous_request_time

        #random delay between requests
        if time_elapsed < 2:
            time.sleep(random.uniform(1, 2) - time_elapsed)


        previous_request_time = time.time()


    return combined_queue


def get_content_article(url, save_dir):

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Create a filename for the HTML file based on the article URL
        filename = os.path.join(save_dir, article_url.replace('/', '', 1).replace('/', '_') + '.html')

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        return
    return


def write_visited_urls(visited_urls, filename):
    with open(filename, 'a') as file:
        for url in visited_urls:
            file.write(url + '\n')
    return

#list of visited main pages
#'https://www.britannica.com/browse/Mammals/'
#'https://www.britannica.com/browse/Birds/'
#'https://www.britannica.com/browse/Fish/'
#'https://www.britannica.com/browse/Reptiles/'
#'https://www.britannica.com/browse/Amphibians/'
#'https://www.britannica.com/browse/Bugs-Mollusks-Invertebrates/'
#'https://www.britannica.com/browse/Nature-Reserve-Region/'
#'https://www.britannica.com/browse/Geographic-Regions/'
#'https://www.britannica.com/browse/Physical-Geography-Water/'
#'https://www.britannica.com/browse/Physical-Geography-Land/'
base_url = 'https://www.britannica.com/browse/Countries-of-the-World/'
combined_queue = get_depth_0_urls(base_url)

# Create needed articles with desired names here
save_dir = 'countries_not_clean'
os.makedirs(save_dir, exist_ok=True)

visited_urls = []

while not combined_queue.empty():
    previous_request_time = time.time()
    article_url = combined_queue.get()
    url = f"https://www.britannica.com{article_url}"
    get_content_article(url, save_dir)
    visited_urls.append(url)
    print(url)
    current_time = time.time()
    time_elapsed = current_time - previous_request_time

    if time_elapsed < 2:
        sleep_time = random.uniform(1, 2) - time_elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    # Update the time of the previous request
write_visited_urls(visited_urls, 'visited_urls.txt')
