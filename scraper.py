from playwright.sync_api import sync_playwright
import time
import csv, json
import datetime

# define function to export data as .csv
def export_to_csv(parsed_data, datetime): 
	with open(f'data_{datetime}.csv', 'w', newline='') as csvfile: 
		fields = ['product_name', 'category', 'colors_count', 'price'] 
		writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL) 
		writer.writeheader() 
		writer.writerows(parsed_data)


# define function to export data as .json
def export_to_json(parsed_data, datetime):
    with open(f'data_{datetime}.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(parsed_data, jsonfile, indent=4)


# define function to extract data from website
def parse_data():

    # initialize maximum scrolls as input
    max_scrolls = int(input("Max scrolls: "))

    # define 
    with sync_playwright() as p:
        # initialize browser, launce driver, go to the url, and wait 5 secs
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.nike.com/id/w/mens-shoes-nik1zy7ok')
        time.sleep(5)
        
        # page.click('#hf_cookie_text_cookieAccept')
        page.wait_for_selector('#skip-to-products')

        stream_boxes = None
        num_scrolls = 0

        # looping to get all elements and store it to the stream_boxes, while looping perform the scroll process  
        while num_scrolls < max_scrolls:
            stream_boxes = page.locator("//div[contains(@class,'css-hvew4t')]/div[@data-testid]")
            stream_boxes.element_handles()[-1].scroll_into_view_if_needed()
            items_on_page = len(stream_boxes.element_handles())
            page.wait_for_timeout(2_000) 
            items_on_page_after_scroll = len(stream_boxes.element_handles())
            if items_on_page_after_scroll > items_on_page:
                num_scrolls += 1  
            else:
                break

            print(f"Page {num_scrolls} completed")

        # initialize list to store data
        parsed = []

        # looping to extract data as text from selector
        for box in stream_boxes.element_handles():
            parsed.append(
                {
                    'product_name': box.query_selector('.product-card__title').inner_text(),
                    'category': box.query_selector('.product-card__subtitle').inner_text(), 
                    'colors_count': box.query_selector('.product-card__product-count').inner_text(),
                    'price': box.query_selector('.product-price').inner_text()
                }
            )
        # for i in parsed:
        #     print(i)

        now = datetime.datetime.today().strftime('%d-%m-%Y')

        # export as .csv and .json
        export_to_json(parsed, now)
        export_to_csv(parsed, now)

        # terminate the driver
        browser.close()

def main():
    parse_data()

if __name__ == "__main__":
    main()