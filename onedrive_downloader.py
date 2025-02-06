from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Set up the Chrome WebDriver with Selenium
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": "E:\\OneDrive Backup 24.10.2024",  # Path where you want to download the files
    "download.prompt_for_download": False,
    "directory_upgrade": True
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Replace this URL with your OneDrive URL
onedrive_url = "https://universiteittwente-my.sharepoint.com/my"

# Ensure the download folder exists
download_path = "E:\\OneDrive Backup 24.10.2024"
os.makedirs(download_path, exist_ok=True)


# Log in to OneDrive and navigate to the files page
def login_and_navigate():
    driver.get(onedrive_url)

    # Wait for the user to log in manually if not logged in automatically
    input("Please log in to OneDrive in the browser and press Enter here once done...")


# Function to determine if an item is a folder
def is_folder(item):
    if "." in item.text.lower():
        return False
    else:
        return True

# Recursive function to download files and explore subfolders
def download_files_recursively(current_local_path):
    try:
        # Wait until the items are loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@data-automationid, 'row-')]"))
        )

        while True:
            # Locate all items (files and folders) on the current page
            items = driver.find_elements(By.XPATH,
                                         "//div[contains(@data-automationid, 'row-')]//span[@data-id='heroField']")

            for index, item in enumerate(items):
                # Refresh the reference to the item in case the page changed
                try:
                    item = items[index]
                    item_name = item.text

                    if is_folder(item):
                        print(f"Exploring folder: {item_name}")

                        # Create a local folder for this folder
                        new_local_path = os.path.join(current_local_path, item_name)
                        os.makedirs(new_local_path, exist_ok=True)

                        # Double-click to open the folder
                        ActionChains(driver).click(item).perform()
                        time.sleep(2)

                        # Recursive call to explore the subfolder with the updated local path
                        download_files_recursively(new_local_path)

                        # After exploring the subfolder, go back to the parent folder
                        time.sleep(1)
                        driver.back()
                        time.sleep(1)

                        # Re-fetch items after navigating back
                        items = driver.find_elements(By.XPATH,
                                                     "//div[contains(@data-automationid, 'row-')]//span[@data-id='heroField']")
                    else:
                        print(f"Downloading file: {item_name}")

                        # Right-click on the file to open context menu
                        action_chains = ActionChains(driver)
                        action_chains.context_click(item).perform()

                        # Wait for the "Download" option to appear and click it
                        download_option = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//span[text()='Download']"))
                        )
                        download_option.click()
                        time.sleep(2)  # Allow time for the download to start

                        # Move the file to the correct local path if needed
                        # This step might depend on your setup, as downloads may not happen instantly or be traceable directly
                        move_downloaded_file(item_name, current_local_path)  # You will implement this function

                except Exception as e:
                    print(f"Failed to process item '{item_name}': {e}")
                    continue

            break  # Exit the while loop if no more items to process

    except Exception as e:
        print(f"Failed to locate items on the page: {e}")


def move_downloaded_file(file_name, destination_path, download_timeout=6000, check_interval=2):
    """
    Moves a downloaded file to the destination path after ensuring the download is complete.

    Parameters:
    - file_name: Name of the file to move
    - destination_path: Path to move the file to
    - download_timeout: Maximum time to wait for the download to complete (in seconds)
    - check_interval: Time interval to check the file size stability (in seconds)
    """
    default_download_dir = "E:\\OneDrive Backup 24.10.2024"  # Set this to your default download location
    source_file = os.path.join(default_download_dir, file_name)
    destination_file = os.path.join(destination_path, file_name)

    start_time = time.time()
    file_last_size = -1

    while time.time() - start_time < download_timeout:
        if os.path.exists(source_file):
            current_size = os.path.getsize(source_file)

            # Check if the file size is stable, indicating download completion
            if current_size == file_last_size:
                try:
                    os.rename(source_file, destination_file)
                    print(f"Moved '{file_name}' to '{destination_path}'")
                    return True
                except Exception as e:
                    print(f"Failed to move '{file_name}' to '{destination_path}': {e}")
                    return False
            else:
                file_last_size = current_size

        time.sleep(check_interval)

    print(f"Timeout reached. File '{file_name}' was not fully downloaded.")
    return False


def main():
    login_and_navigate()

    # Start the recursive download process from the base download path
    base_local_path = download_path  # Root download path where the script will mirror the OneDrive structure
    download_files_recursively(base_local_path)

    driver.quit()


if __name__ == "__main__":
    main()


