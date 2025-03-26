from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from fpdf import FPDF
import json
import csv
import os

# Set up Edge WebDriver
service = Service(executable_path="[path_to_selenium_driver].exe")
driver = webdriver.Edge(service=service)

# Base URL for DNA Relatives with pagination
base_url = "https://you.23andme.com/family/relatives/?sort=strength&page="
total_pages = 61  # Total pages you specified

# File to track successful pages
success_file = "successful_captures.csv"

# Load already successful pages
successful_pages = set()
if os.path.exists(success_file):
    with open(success_file, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header if exists
        for row in reader:
            if row:
                successful_pages.add(int(row[0]))

try:
    # Navigate to 23andMe login page
    driver.get("https://you.23andme.com/")
    print("Please manually log in to 23andMe in the browser window.")
    print("Once logged in, return here and press Enter to continue...")
    
    input("Press Enter when ready to proceed...")
    print("Login detected, proceeding to DNA Relatives...")

    for page_count in range(1, total_pages + 1):
        if page_count in successful_pages:
            print(f"Skipping page {page_count} (already captured)")
            continue

        print(f"Attempting page {page_count} of {total_pages}")
        driver.get(f"{base_url}{page_count}")
        
        # Wait for the matches to load
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "dna-relatives-list-item")))
        except Exception as e:
            print(f"Failed to load page {page_count}: {e}")
            continue

        # Scroll to the bottom and wait
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Find all match items
        match_items = driver.find_elements(By.CLASS_NAME, "dna-relatives-list-item")
        page_matches = []
        for item in match_items:
            match_data = {}
            try:
                name = item.find_element(By.CLASS_NAME, "relative-link").text.strip()
                match_data["name"] = name
            except NoSuchElementException:
                match_data["name"] = "Unknown Name"

            # Capture all relationship-label texts as a list
            relationship_elems = item.find_elements(By.CLASS_NAME, "relationship-label")
            relationships = [elem.text.strip() for elem in relationship_elems if elem.text.strip()]
            match_data["relationships"] = relationships if relationships else ["No Relationship Text"]

            # Clean small-detail fields
            small_details = item.find_elements(By.CLASS_NAME, "small-detail")
            match_data["small_details"] = [detail.text.strip() for detail in small_details if detail.text.strip() and detail.tag_name == "span"]

            # Clean segment fields
            segment_details = item.find_elements(By.CSS_SELECTOR, "span.shared-dna.hide-for-mobile")
            match_data["segment_details"] = [detail.text.strip() for detail in segment_details if detail.text.strip() and detail.tag_name == "span"]

            page_matches.append(match_data)

        # Save page data to JSON
        json_file = f"page_{page_count}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(page_matches, f, ensure_ascii=False, indent=4)
        print(f"Successfully saved page {page_count} to {json_file}")

        # Log successful capture
        with open(success_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if os.stat(success_file).st_size == 0:
                writer.writerow(["page_number"])
            writer.writerow([page_count])

finally:
    driver.quit()

# Compile all pages into PDF and CSV if complete
captured_pages = len(successful_pages) + sum(1 for _ in range(1, total_pages + 1) if _ not in successful_pages)
if captured_pages == total_pages:
    print("All pages captured, compiling into PDF and CSV...")
    all_matches = []
    for page_count in range(1, total_pages + 1):
        json_file = f"page_{page_count}.json"
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                page_data = json.load(f)
                all_matches.extend(page_data)

    # Save to PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for match in all_matches:
        # Use the first non-empty relationship for PDF
        relationship = next((r for r in match["relationships"] if r), "Unknown")
        line = f"{match['name']} - {relationship}"
        if match['small_details']:
            line += " (" + ", ".join(match['small_details']) + ")"
        if match['segment_details']:
            line += " (" + ", ".join(match['segment_details']) + ")"
        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))
    pdf.output("23andme_matches.pdf")
    print(f"Compiled {len(all_matches)} matches into 23andme_matches.pdf")

    # Save to CSV
    with open("23andme_matches.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["name", "relationship_1", "relationship_2", "small_detail_1", "small_detail_2", "small_detail_3","segment_details"])
        writer.writeheader()
        for match in all_matches:
            row = {
                "name": match["name"],
                "relationship_1": match["relationships"][0] if len(match["relationships"]) > 0 else "",
                "relationship_2": match["relationships"][1] if len(match["relationships"]) > 1 else "",
                "small_detail_1": match["small_details"][0] if len(match["small_details"]) > 0 else "",
                "small_detail_2": match["small_details"][1] if len(match["small_details"]) > 1 else "",
                "small_detail_3": match["small_details"][2] if len(match["small_details"]) > 2 else "",
                "segment_details": match["segment_details"][0] if len(match["segment_details"]) > 0 else ""
            }
            writer.writerow(row)
    print(f"Compiled {len(all_matches)} matches into 23andme_matches.csv")
else:
    print(f"Only captured {captured_pages} of {total_pages} pages. Rerun to complete.")
