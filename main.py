import json
from playwright.sync_api import Playwright, sync_playwright, ElementHandle

DOMAIN_PREFIX = 'https://www.balenciaga.com/'

def get_product_name(product_page) -> str:
    return product_page.locator('h1.c-product__name').inner_text()

def scrape_section(all_page, curr_product_page, section_link):
    all_page.set_default_navigation_timeout(100000)
    all_page.goto(section_link)
    curr_products = all_page.locator('div.l-productgrid__wrapper').get_by_role('link').all()
    print('Length of products: ', len(curr_products))

    product_data_all = []
    for i, p in enumerate(curr_products):
        product_data = {}

        link = p.get_attribute('href')

        done = False
        while not done:
            try:
                curr_product_page.goto(DOMAIN_PREFIX + link)
                done = True
            except Exception as e:
                print(e)
        print('Product name: ' + get_product_name(curr_product_page))
        print(i)
        print('Images: ')

        product_data['link'] = DOMAIN_PREFIX + link
        product_data['name'] = get_product_name(curr_product_page)
        product_data['img_srcs'] = []
        for i, img in enumerate(curr_product_page.locator('ul.c-productcarousel__wrapper').get_by_role('img').all()):
            img_src = img.get_attribute('data-src')
            product_data['img_srcs'].append(img_src)
            product_data_all.append(product_data)

    return product_data_all

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    curr_product_page = context.new_page()

    MEN_VIEW_ALL = 'https://www.balenciaga.com/en-us/men/ready-to-wear/view-all?start=0&sz=1000'
    WOMEN_VIEW_ALL = 'https://www.balenciaga.com/en-us/women/ready-to-wear/view-all?start=0&sz=1000'

    # Open the file in write mode ('w')
    with open('data.json', 'a') as file:
        # Write the JSON data to the file
        json.dump({
            'men': scrape_section(page, curr_product_page, MEN_VIEW_ALL),
            'women': scrape_section(page, curr_product_page, WOMEN_VIEW_ALL),
        }, file)


with sync_playwright() as playwright:
    run(playwright)
