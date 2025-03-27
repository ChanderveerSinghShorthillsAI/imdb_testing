from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# IMDb URL for testing
IMDB_URL = "https://www.imdb.com"

@pytest.fixture
def driver():
    """Setup Firefox driver with correct paths"""
    options = Options()
    # options.binary_location = "/snap/bin/firefox"  # Correct path for snap Firefox

    # Initialize Firefox using Service
    service = FirefoxService(executable_path="/snap/bin/geckodriver")  # Correct path for geckodriver
    driver = webdriver.Firefox(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_imdb_homepage(driver):
    """ Test if IMDb homepage loads."""
    driver.get(IMDB_URL)
    assert "IMDb" in driver.title, "❌ IMDb homepage did not load!"

def test_imdb_search(driver):
    """ Test IMDb search."""
    driver.get(IMDB_URL)
    
    # Locate search box and enter "Inception"
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "suggestion-search"))
    )
    search_box.send_keys("Inception")
    search_box.send_keys(Keys.RETURN)

    # Wait for the results page to load
    results_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section[@data-testid='find-results-section-title']"))
    )

    # Verify if "Titles" section is displayed
    titles_section = results_section.find_element(By.XPATH, ".//h3[contains(text(), 'Titles')]")
    assert titles_section.is_displayed(), "❌ No search results found for 'Inception'"

    # Check if the first result is "Inception (2010)"
    first_result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'ipc-metadata-list')]/li[1]//a"))
    )
    assert "Inception" in first_result.text, "❌ 'Inception' was not found in search results"

    print(" Search for 'Inception' was successful!")

def test_invalid_search(driver):
    """ Test search for an invalid term."""
    driver.get(IMDB_URL)
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("ajsdhfjksdhfkjashdfkljashdf")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    no_results_text = driver.find_element(By.XPATH, "//*[contains(text(), 'No results found')]")
    assert no_results_text.is_displayed(), "❌ Error message not displayed for invalid search!"
