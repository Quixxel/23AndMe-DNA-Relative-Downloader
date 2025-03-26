# 23AndMe DNA Relative Downloader

A Python script that uses Selenium to download your list of DNA relatives from 23AndMe.

## Features
- Automates the process of downloading DNA relative data
- Uses Selenium for reliable web scraping
- Saves results to PDF and JSON

## Prerequisites
- Python 3.x installed
- Selenium package installed
- Appropriate browser driver (e.g., ChromeDriver)

## Installation
1. Install Python if not already installed: [python.org](https://www.python.org/downloads/)
2. Install required packages: pip install selenium
3. Download and install the Selenium driver for your browser:
   - Chrome: [ChromeDriver](https://developer.chrome.com/docs/chromedriver/get-started)
   - Firefox: [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
   - Edge: [MS Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver?ch=1&form=MA13LH)
   - Safari: [Safaridriver](https://developer.apple.com/documentation/webkit/testing-with-webdriver-in-safari)
4. Download `downloader.py`

## Usage
1. Open `downloader.py` a text editor (vim, notepad, etc.)
2. In `downloader.py`, replace `[path_to_selenium_driver].exe` with the actual path to your downloaded driver. Usually, this can be found at:
    - Edge: C:\\Users\\[YOURUSERNAME]\\Downloads\\edgedriver_win64\\msedgedriver.exe
    - Safari: /usr/bin/safaridriver
    etc. Check the download links for more information on this.
3. Open the terminal, command prompt, etc. Select the location where the script was downloaded using the 'cd' command and run the script by typing the following command: 'python downloader.py'
4. When the 23AndMe login screen appears, enter your credentials
5. Return to the terminal and press Enter
6. Wait approximately 15 minutes for the download to complete
7. Check the script's directory for your DNA relatives list. You should have the following files:
    - 23andme_matches.csv: a list of all your match information in CSV format
    - 23andme_matches.pdf: a PDF with the same content as the CSV
    - page_1.json, page_2.json, ..., page_60.json: data from each page to allow the script to restart if the website crashes partway through; you can delete these once the PDF is generated.
    - successful_captures.csv: a log of which pages were successfully downloaded to enable restarts, you can delete this once complete


## Troubleshooting
- If the script fails, try running it again - the 23AndMe website may occasionally crash
- Ensure your browser driver matches your browser version
- Verify your internet connection is stable
- If you are having difficulties running python scripts / 

## Disclaimer
This script worked for the developer but is provided as-is:
- No warranty
- No refunds, it's worth what you paid for it
- Use at your own risk

## Contributing
Feel free to submit pull requests or open issues for improvements or bug reports.