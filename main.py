import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import os

chromedriver_path = ""

options = Options()
options.add_argument("--window-size=1920x1080")
options.add_argument("--verbose")

driver = webdriver.Chrome(options=options)

c = 0

def download_images(urls, limit, c):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    for image_url in urls:
        if c[0] >= limit:
            exit()

        local_image_path = "/Users/nikita_filin/Desktop/Programming/Coding/Python/parser/imgs/" + os.path.basename(image_url)
        try:
            response = requests.get(image_url, headers=headers, verify=False)
            if response.status_code == 200:
                with open(local_image_path, 'wb') as file:
                    file.write(response.content)
                print(f'Image successfully downloaded: {local_image_path}')
                c[0] += 1

            else:
                print(f'Error downloading image: HTTP Status Code {response.status_code}')

        except requests.exceptions.RequestException as e:
            print(f'Error downloading image: {e}')


def watch_car_adv(url):
    image_links = []

    driver.get(url)
    image_section = driver.find_element_by_class_name("topSection__images")
    first_image = image_section.find_element_by_class_name("vImages__first")
    first_image_link = first_image.find_element_by_class_name("vImages__item").get_attribute("href")
    image_links.append(first_image_link)

    other_images_block = image_section.find_element_by_class_name("vImages__other")
    other_images = other_images_block.find_elements_by_class_name("vImages__item")

    for image in other_images:
        image_links.append(image.get_attribute("href"))

    return image_links



def visit_make_model(make_url):
    driver.get(make_url)
    all_models = driver.find_elements_by_class_name("details")
    all_models_list = []
    for model in all_models:
        model_link = model.find_element_by_css_selector(".b-makesList__item a.all")
        all_models_list.append(model_link.get_attribute("href"))

    return all_models_list


def get_adv(image_num, c):

    most_popular_cars_links = ["https://www.auto24.ee/ferrari", "https://www.auto24.ee/audi", "https://www.auto24.ee/bmw", "https://www.auto24.ee/honda", "https://www.auto24.ee/mercedes-benz", "https://www.auto24.ee/mazda", "https://www.auto24.ee/volkswagen", "https://www.auto24.ee/toyota"]
    for make in most_popular_cars_links:
            driver.get(make)
            all_models_links = visit_make_model(make)
            get_all_model_adv(all_models_links, image_num, c)


def get_all_model_adv(make_models_links, image_num, c):
    for url in make_models_links:
        driver.get(url)

        button = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/div[4]/div/button[2]")
        counter = 0

        while counter < 2:
            if counter == 0:
                button_onclick = button.get_attribute("onclick")
                if button_onclick is not None:
                    start_index = button_onclick.find("location.href='") + len("location.href='")
                    end_index = button_onclick.find("'", start_index)
                    link_location = "https://www.auto24.ee" + button_onclick[start_index:end_index]
                    print(link_location)

                else:
                    counter += 1

            all_links = driver.find_elements_by_class_name("row-link")
            all_links_formated = []
            for i in all_links:
                all_links_formated.append(i.get_attribute("href"))

            for link in all_links_formated:
                links = (watch_car_adv(link))
                print(links)
                download_images(links, image_num, c)

            if counter == 0:
                driver.get(link_location)
                button = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/div[4]/div/button[2]")

            else:
                break

            if "disabled" in button.get_attribute("class"):
                counter += 1
            else:
                break



def main():
    image_num = int(input("Insert image number "))
    c = [0]
    get_adv(image_num, c)

main()