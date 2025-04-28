import time
import random
import csv
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import re
import pandas as pd

# ✅ Function to simulate human-like scrolling and interactions
def human_interaction(page):
    def human_scroll():
        scroll_pause_time = random.uniform(0.3, 0.8)
        for _ in range(random.randint(1, 2)):
            page.mouse.move(random.randint(100, 800), random.randint(100, 800))
            page.keyboard.press("PageDown")
            time.sleep(scroll_pause_time)

    def move_mouse_randomly():
        for _ in range(random.randint(1, 3)):
            page.mouse.move(random.randint(100, 800), random.randint(100, 800))
            time.sleep(random.uniform(0.2, 0.5))

    move_mouse_randomly()
    human_scroll()

# ✅ Function to scrape aircraft listing links from each page
def scrape_listings(page):
    page.wait_for_selector("td[colspan='3']", timeout=5000)
    listings = page.query_selector_all("td[colspan='3']")

    if not listings:
        print("⚠️ No listings found on this page.")

    links = []
    for listing in listings:
        try:
            aircraft_link_elem = listing.query_selector("a.photoListingsDescription")
            listing_id = aircraft_link_elem.get_attribute("adv_id") if aircraft_link_elem else None
            full_aircraft_url = f"https://www.aso.com/listings/spec/ViewAd.aspx?id={listing_id}&listingType=true" if listing_id else None

            if full_aircraft_url:
                links.append(full_aircraft_url)
                print(f"✅ Found Listing: {full_aircraft_url}")

        except Exception as e:
            print(f"⚠️ Error scraping listing link: {e}")

    return links

# ✅ Function to go through all pages, stopping when "Next" is disabled
def go_through_all_pages(page):
    all_links = []
    page_num = 1  # Start at the first page

    while True:
        print(f"📄 Scraping page {page_num}...")

        human_interaction(page)  # ✅ Simulate human behavior

        # ✅ Scrape listings on the current page
        links = scrape_listings(page)
        all_links.extend(links)

        # ✅ Try clicking "Next"
        next_button = page.query_selector("input[id*='btnNext']")
        if not next_button or next_button.get_attribute("disabled") or not next_button.is_visible():
            print("✅ Reached the last page or 'Next' is unavailable. Moving to individual listings.")
            break  # Stop when the button is disabled or missing

        print(f"🔄 Clicking 'Next' button to go to page {page_num + 1}...")
        next_button.click()
        page.wait_for_load_state("domcontentloaded")
        time.sleep(random.uniform(1, 2))  # ✅ Small delay to prevent bot detection
        page_num += 1  # ✅ Increase page number

    return all_links  # ✅ Return all collected listing links

# ✅ Function to scrape individual aircraft listing details
def scrape_listing_details(page, url):
    retry_attempts = 3  # ✅ Retry up to 3 times if a page fails
    for attempt in range(retry_attempts):
        try:
            page.goto(url, timeout=15000)
            time.sleep(random.uniform(0.5, 1))

            # ✅ Extract Aircraft Name
            name_elem = page.query_selector("div.adSpecView-header-Descr > div")
            aircraft_name = name_elem.inner_text().strip() if name_elem else "N/A"

            # ✅ Extract Registration Number
            reg_elem = page.query_selector("div.adSpecView-header-RegSerialPrice span:text('Reg #')")
            reg_number = reg_elem.inner_text().replace("Reg #", "").strip() if reg_elem else "N/A"

            # ✅ Extract Serial Number (S/N)
            sn_elem = page.query_selector("div.adSpecView-header-RegSerialPrice span:text('Serial #')")
            serial_number = sn_elem.inner_text().replace("Serial #", "").strip() if sn_elem else "N/A"

            # ✅ Extract Price
            price_elem = page.query_selector("div.adSpecView-header-RegSerialPrice span:text('Price:')")
            price = price_elem.inner_text().replace("Price:", "").strip() if price_elem else "Not Listed"

            # ✅ Extract TTAF (Total Time Airframe) **Without "Hrs."**
            tt_elem = page.query_selector("div.adSpecView-header-RegSerialPrice span:text('TTAF:')")
            TTAF = tt_elem.inner_text().replace("TTAF:", "").replace("Hrs.", "").strip() if tt_elem else "N/A"

            # ✅ Extract Landings
            landings_elem = page.query_selector("div[style*='padding:4px']")
            landings_text = landings_elem.inner_text() if landings_elem else "N/A"
            landings_match = re.search(r'Landings:\s*([\d,]+)', landings_text)
            landings = landings_match.group(1) if landings_match else "N/A"

            # ✅ Extract Location
            location_elem = page.query_selector("div.adSpecView-header-RegSerialPrice span:text('Location:')")
            location = location_elem.inner_text().replace("Location:", "").strip() if location_elem else "N/A"

            # ✅ Extract Company Name
            company_elem = page.query_selector("div.adSpecView-dealerLogoDiv img[title]")
            company_name = company_elem.get_attribute("title") if company_elem else "N/A"

            print(f"✅ Scraped: {aircraft_name} | {reg_number} | {serial_number} | {price} | {TTAF} | {landings} | {location} | {company_name} | {url}")
            return [aircraft_name, reg_number, serial_number, price, TTAF, landings, location, company_name, url]

        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1} failed for {url}: {e}")
            time.sleep(2)

    print(f"❌ Failed to scrape {url} after {retry_attempts} attempts")
    return ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", url]

# ✅ Launch Playwright and scrape ASO listings
def main():
    print("🚀 Starting ASO scraper...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  
            args=["--disable-blink-features=AutomationControlled", "--disable-web-security", "--start-maximized"]
        )
        context = browser.new_context()
        page = context.new_page()
        stealth_sync(page)

        base_url = "https://www.aso.com/listings/AircraftListings.aspx?searchId=61631244"
        page.goto(base_url, timeout=40000)

        filename = "ASOlistings.csv"
        today_date = time.strftime("%Y%m%d")
        filename = f"ASOlistings_{today_date}.csv"
        with open(filename, mode="w", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Aircraft Name", "Reg #", "Serial Number", "Price", "TTAF", "Landings", "Location", "Company", "URL"])

            # ✅ Collect all listing URLs first by navigating through all pages
            all_links = go_through_all_pages(page)

        print(f"✅ Collected {len(all_links)} listing URLs. Now scraping individual listings...")

        with open(filename, mode="a", newline='') as file:
            csv_writer = csv.writer(file)
            for link in all_links:
                details = scrape_listing_details(page, link)
                csv_writer.writerow(details)

        print("✅ All aircraft listings saved successfully!")
        browser.close()

    clean_csv(filename)

def clean_csv(filename):
    df = pd.read_csv(filename)

    # Debugging: Print sample aircraft names before splitting
    print("Sample Aircraft Names Before Splitting:")
    print(df['Aircraft Name'].head(10))  # Print first 10 rows to check the format

    # Split into Year, Make, and Model (Simple 3-Part Split)
    df[['Year', 'Make', 'Model']] = df['Aircraft Name'].str.split(n=2, expand=True)

    # Remove the original 'Aircraft Name' column
    df.drop(columns=['Aircraft Name'], inplace=True)

    # Clean Price and TTAF columns
    df['Price'] = df['Price'].astype(str).str.replace(',', '').str.replace('$', '').str.strip()
    df['TTAF'] = df['TTAF'].astype(str).str.replace(',', '').str.strip()
    df['Landings'] = df['Landings'].astype(str).str.replace(',', '').str.strip()

    # Ensure final column order
    final_columns = ['Year', 'Make', 'Model', 'Reg #', 'Serial Number', 'Price', 'TTAF', 'Landings', 'Location', 'Company', 'URL']
    
    # Keep only the relevant columns & reorder them
    df = df[final_columns]

    # Save the cleaned CSV
    cleaned_filename = f"Cleaned_{filename}"
    df.to_csv(cleaned_filename, index=False)
    print(f"\n✅ Cleaned CSV file saved as {cleaned_filename}")

if __name__ == "__main__":
    main()