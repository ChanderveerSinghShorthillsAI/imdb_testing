import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import requests
from bs4 import BeautifulSoup

# from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

IMDB_URL = "https://www.imdb.com/"


# Pytest fixture to set up the Firefox WebDriver
@pytest.fixture(scope="class")
def driver():
    """Setup Firefox driver with correct paths"""
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode (remove if debugging)

    # Find the correct geckodriver path
    service = FirefoxService(
        executable_path="/snap/bin/geckodriver"
    )  # Automatically manage GeckoDriver
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(IMDB_URL)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


# Sample test class with automated test cases
class TestIMDb:
    def test_homepage_load(self, driver):
        """Verify IMDb homepage loads successfully"""
        test_case = {
            "Test Case ID": "TC001",
            "Description": "Verify IMDb homepage loads",
            "Expected Result": "IMDb homepage should load with 'IMDb' in the title",
            "Actual Result": "",
            "Status": "",
        }
        try:
            assert "IMDb" in driver.title
            test_case["Actual Result"] = "Homepage loaded successfully"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_search_functionality(self, driver):
        """Verify search bar works"""
        test_case = {
            "Test Case ID": "TC002",
            "Description": "Verify search functionality on IMDb",
            "Expected Result": "Search results should display 'Inception'",
            "Actual Result": "",
            "Status": "",
        }
        try:
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys("Inception")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)  # Allow time for results to load
            assert "Inception" in driver.page_source
            test_case["Actual Result"] = "Search functionality worked as expected"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_movie_details_page(self, driver):
        """Check if clicking a movie link opens the details page"""
        test_case = {
            "Test Case ID": "TC003",
            "Description": "Check if clicking a movie link opens the details page",
            "Expected Result": "Movie details page should open and contain 'Inception'",
            "Actual Result": "",
            "Status": "",
        }
        try:
            movie_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Inception")
            movie_link.click()
            time.sleep(3)  # Wait for the movie page to load
            assert "Inception" in driver.page_source
            test_case["Actual Result"] = "Movie details page loaded successfully"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_navigation_menu(self, driver):
        """Verify navigation menu functionality"""
        test_case = {
            "Test Case ID": "TC004",
            "Description": "Verify the navigation menu is functional",
            "Expected Result": "Navigation menu should open and display options",
            "Actual Result": "",
            "Status": "",
        }
        try:
            menu_button = driver.find_element(By.ID, "imdbHeader-navDrawerOpen")
            menu_button.click()
            time.sleep(2)  # Allow time for menu to open
            assert "Menu" in driver.page_source
            test_case["Actual Result"] = "Navigation menu opened successfully"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_login_button(self, driver):
        """Verify login button redirects to the login page"""
        test_case = {
            "Test Case ID": "TC005",
            "Description": "Verify login button redirects to the login page",
            "Expected Result": "Login button should redirect to the sign-in page",
            "Actual Result": "",
            "Status": "",
        }
        try:
            login_button = driver.find_element(By.LINK_TEXT, "Sign In")
            driver.execute_script(
                "arguments[0].click();", login_button
            )  # Force click via JS
            time.sleep(3)  # Wait for the login page to load
            assert "Sign in" in driver.page_source
            test_case["Actual Result"] = "Redirected to sign-in page"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_watchlist_button(self, driver):
        """Verify Watchlist button navigates correctly"""
        test_case = {
            "Test Case ID": "TC006",
            "Description": "Verify Watchlist button redirects to the watchlist page",
            "Expected Result": "Watchlist page should load successfully",
            "Actual Result": "",
            "Status": "",
        }
        try:
            # watchlist_button = driver.find_element(By.ID, "imdbHeader-navWatchlist")
            # Locate the Watchlist button using its class name
            watchlist_button = driver.find_element(
                By.CLASS_NAME, "imdb-header__watchlist-button"
            )
            watchlist_button.click()
            time.sleep(3)  # Allow time for page to load
            assert "Watchlist" in driver.page_source
            test_case["Actual Result"] = "Navigated to the watchlist page"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_footer_links(self, driver):
        """Verify footer links work as expected"""
        test_case = {
            "Test Case ID": "TC007",
            "Description": "Verify footer links navigate to correct pages",
            "Expected Result": "Footer links should work and redirect to correct pages",
            "Actual Result": "",
            "Status": "",
        }
        try:
            footer_link = driver.find_element(By.LINK_TEXT, "Help")
            footer_link.click()
            time.sleep(3)  # Allow time for page to load
            assert "Help" in driver.page_source
            test_case["Actual Result"] = "Help page loaded successfully"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_search_no_results(self, driver):
        """Verify that no results message appears when searching for a non-existent movie"""
        test_case = {
            "Test Case ID": "TC008",
            "Description": "Verify that a 'no results' message appears when searching for a non-existent movie",
            "Expected Result": "Search results should display 'No results found'",
            "Actual Result": "",
            "Status": "",
        }
        try:
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys("NonExistentMovie123")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)  # Allow time for results to load
            assert "No results found" in driver.page_source
            test_case["Actual Result"] = "Correct 'no results' message displayed"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    
    
    def test_login_error_message(self, driver):
        """Verify that an error message appears if user tries to access a page without logging in"""
        test_case = {
            "Test Case ID": "TC009",
            "Description": "Verify that an error message appears if a user tries to access a page without logging in",
            "Expected Result": "User should be redirected to the login page with an error message",
            "Actual Result": "",
            "Status": "",
        }
        try:
            driver.get(
                IMDB_URL + "/watchlist"
            )  # Try to access Watchlist without logging in
            time.sleep(3)  # Wait for the login prompt
            assert "Sign in" in driver.page_source
            test_case["Actual Result"] = "Redirected to login page as expected"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    
    
    def test_page_title_contains_imdb(self, driver):
        """Verify that the page title contains 'IMDb'"""
        test_case = {
            "Test Case ID": "TC010",
            "Description": "Verify that the page title contains 'IMDb'",
            "Expected Result": "Page title should contain 'IMDb'",
            "Actual Result": "",
            "Status": "",
        }
        try:
            driver.get("https://www.imdb.com")
            title = driver.title
            assert "IMDb" in title
            test_case["Actual Result"] = "Page title contains 'IMDb'"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_search_bar_present(self, driver):
        """Verify that the search bar is present on the homepage"""
        test_case = {
            "Test Case ID": "TC011",
            "Description": "Verify that the search bar is present on the homepage",
            "Expected Result": "Search bar should be present on the homepage",
            "Actual Result": "",
            "Status": "",
        }
        try:
            driver.get("https://www.imdb.com")
            search_bar = driver.find_element(By.ID, "suggestion-search")
            assert search_bar.is_displayed()
            test_case["Actual Result"] = "Search bar is present on the homepage"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_sign_in_button_present(self, driver):
        """Verify that the 'Sign In' button is present on the homepage"""
        test_case = {
            "Test Case ID": "TC012",
            "Description": "Verify that the 'Sign In' button is present on the homepage",
            "Expected Result": "'Sign In' button should be present on the homepage",
            "Actual Result": "",
            "Status": "",
        }
        try:
            driver.get("https://www.imdb.com")
            sign_in_button = driver.find_element(By.LINK_TEXT, "Sign In")
            assert sign_in_button.is_displayed()
            test_case["Actual Result"] = "'Sign In' button is present on the homepage"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    
    def test_footer_present(self, driver):
        """Verify that the footer is present on the homepage"""
        test_case = {
            "Test Case ID": "TC013",
            "Description": "Verify that the footer is present on the homepage",
            "Expected Result": "Footer should be visible on the homepage",
            "Actual Result": "",
            "Status": "",
        }
        try:
            driver.get("https://www.imdb.com")
            footer = driver.find_element(By.TAG_NAME, "footer")
            assert footer.is_displayed()
            test_case["Actual Result"] = "Footer is visible on the homepage"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def save_test_case_to_excel(self, test_case):
        """Save test case result to Excel file"""
        df = pd.DataFrame([test_case])
        try:
            existing_df = pd.read_excel("test_results.xlsx")
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass  # If file doesn't exist, we will create a new one
        df.to_excel("IMDB_Automation_Test_Cases.xlsx", index=False)


    def test_footer_social_links_section_exists(self, driver):
        """Verify the 'Follow IMDb on social' section exists"""

        test_case = {
            "Test Case ID": "TC014",
            "Description": "Verify that the 'Follow IMDb on social' section is present in the footer",
            "Expected Result": "The 'Follow IMDb on social' section should be displayed",
            "Actual Result": "",
            "Status": "",
        }
        try:
            social_section = driver.find_element(By.XPATH, "//div[contains(text(), 'Follow IMDb on social')]")
            assert social_section.is_displayed()
            test_case["Actual Result"] = "Social section is displayed"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_footer_help_link_exists(self, driver):
        """Verify the 'Help' link exists"""

        test_case = {
            "Test Case ID": "TC015",
            "Description": "Verify that the 'Help' link is present in the footer",
            "Expected Result": "The 'Help' link should be displayed",
            "Actual Result": "",
            "Status": "",
        }
        try:
            help_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Help')]")
            assert help_link.is_displayed()
            test_case["Actual Result"] = "Help link is displayed"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_footer_imdbpro_link_exists(self, driver):
        """Verify the 'IMDbPro' link exists"""

        test_case = {
            "Test Case ID": "TC016",
            "Description": "Verify that the 'IMDbPro' link is present in the footer",
            "Expected Result": "The 'IMDbPro' link should be displayed",
            "Actual Result": "",
            "Status": "",
        }
        try:
            imdbpro_link = driver.find_element(By.XPATH, "//a[contains(text(), 'IMDbPro')]")
            assert imdbpro_link.is_displayed()
            test_case["Actual Result"] = "IMDbPro link is displayed"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_footer_conditions_of_use_link_exists(self, driver):
        """Verify the 'Conditions of Use' link exists"""

        test_case = {
            "Test Case ID": "TC017",
            "Description": "Verify that the 'Conditions of Use' link is present in the footer",
            "Expected Result": "The 'Conditions of Use' link should be displayed",
            "Actual Result": "",
            "Status": "",
        }
        try:
            conditions_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Conditions of Use')]")
            assert conditions_link.is_displayed()
            test_case["Actual Result"] = "Conditions of Use link is displayed"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)
        
    def test_navbar_logo_exists(self, driver):
        """Verify the IMDb logo is present"""
        test_case = {
            "Test Case ID": "TC018",
            "Description": "Verify that the IMDb logo is displayed in the navbar",
            "Expected Result": "The IMDb logo should be visible",
            "Actual Result": "",
            "Status": "",
        }
        try:
            logo = driver.find_element(By.ID, "home_img_holder")
            assert logo.is_displayed()
            test_case["Actual Result"] = "Logo is displayed"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_navbar_menu_button_exists(self, driver):
        """Verify the menu button is present"""
        test_case = {
            "Test Case ID": "TC019",
            "Description": "Verify that the menu button is displayed in the navbar",
            "Expected Result": "The menu button should be visible",
            "Actual Result": "",
            "Status": "",
        }
        try:
            menu_button = driver.find_element(By.ID, "imdbHeader-navDrawerOpen")
            assert menu_button.is_displayed()
            test_case["Actual Result"] = "Menu button is displayed"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)

    def test_navbar_search_box_exists(self, driver):
        """Verify the search input box is present"""

        test_case = {
            "Test Case ID": "TC020",
            "Description": "Verify that the search input box is displayed in the navbar",
            "Expected Result": "The search input box should be visible",
            "Actual Result": "",
            "Status": "",
        }
        try:
            search_box = driver.find_element(By.ID, "suggestion-search")  # Or a more specific selector
            assert search_box.is_displayed()
            test_case["Actual Result"] = "Search box is displayed"
            test_case["Status"] = "Pass"
        except Exception as e:
            test_case["Actual Result"] = str(e)
            test_case["Status"] = "Fail"

        self.save_test_case_to_excel(test_case)
        
 

    

# Run the script
if __name__ == "__main__":
    pytest.main(["-v", __file__])  # Use __file__ to refer to this script dynamically
