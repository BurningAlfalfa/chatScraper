import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up Chrome driver service
s = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=s, options=chrome_options)

def save_debug_html(filename, source):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(source)
    print(f"Saved HTML to {filename}")

def find_and_click_join_and_login_button():
    try:
        # Load the main page
        driver.get('https://traderschoice.net/about-traders-choice/')
        save_debug_html("main_page.html", driver.page_source)  # Save main page HTML for debugging

        # Step 1: Locate the main iframe and switch to it
        main_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[data-src*='LetsHaveAConversation']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", main_iframe)
        driver.execute_script("arguments[0].setAttribute('src', arguments[0].getAttribute('data-src'))", main_iframe)
        time.sleep(2)  # Give time for iframe to load
        driver.switch_to.frame(main_iframe)
        print("Switched to the main chat iframe.")
        save_debug_html("chat_iframe.html", driver.page_source)  # Save iframe HTML for debugging

        # Step 2: Locate the nested chat iframe inside the main iframe and switch to it
        nested_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "chat-iframe"))
        )
        driver.switch_to.frame(nested_iframe)
        print("Switched to the nested chat iframe.")
        save_debug_html("nested_chat_iframe.html", driver.page_source)  # Save HTML for debugging if needed

        # Step 3: Attempt to find the "Click to Chat" button in the nested iframe
        try:
            join_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "clickToChatBtn"))
            )
            join_button.click()
            print("Clicked the 'Click to Chat' button.")
            
            # Step 4: Wait for the iframe to reload with the login interface
            time.sleep(2)  # Wait for iframe to reload
            driver.switch_to.default_content()  # Switch back to the main content
            driver.switch_to.frame(main_iframe)  # Switch again to the main iframe
            
            # Step 5: Switch to the nested iframe again after the reload
            updated_nested_iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "chat-iframe"))
            )
            driver.switch_to.frame(updated_nested_iframe)
            print("Switched to the updated nested chat iframe after reload.")
            save_debug_html("updated_nested_chat_iframe.html", driver.page_source)  # Save updated iframe HTML

            # Step 6: Find the dcMessage span and the Login button inside it
            dc_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "dcMessage"))
            )
            print("Found the dcMessage span.")
            login_button = dc_message.find_element(By.CLASS_NAME, "loginBtn")
            login_button.click()
            print("Clicked the login button.")
            
        except TimeoutException:
            print("Join or login button not found in the updated iframe.")
            save_debug_html("join_or_login_button_not_found.html", driver.page_source)

    except (TimeoutException, NoSuchElementException) as e:
        print(f"An error occurred: {e}")
        save_debug_html("error_page.html", driver.page_source)  # Save HTML for troubleshooting if necessary

    finally:
        driver.quit()
        print("Driver closed.")

# Run the function to test
find_and_click_join_and_login_button()

