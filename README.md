# OneDrive Recursive Downloader

## Overview

This project provides a Python script that automates the download of an entire OneDrive folder—including all its nested subfolders and files—directly to a specified local (external) drive. The script is designed to work around limitations of built-in OneDrive download methods, especially when local storage is minimal and the data exists only in the cloud.

## Problem

I needed to download massive OneDrive folders (in my case, around 350GB) and faced some issues:

- **Limited Local Storage:**  
  The computer does not have enough storage to temporarily hold the data, as the files are exclusively in the cloud.

- **Folder Structure Preservation:**  
  It is essential to maintain the original folder and subfolder hierarchy during the download process.

- **Ineffective Built-in Methods:**  
  The OneDrive web interface or client often fails to download very large folders or preserve the nested structure, sometimes splitting files into zipped archives or stopping mid-download.

- **API and Permission Constraints:**  
  Alternatives like PowerShell or the Microsoft Graph API require administrative permissions or special configurations that where not available to me (as a student).

## What the Script Does

The script uses Python with Selenium WebDriver to simulate browser interactions. It performs the following:

- **Login and Navigation:**  
  - Opens the OneDrive URL and waits for manual login.  
  - Once logged in, the script begins processing the OneDrive file list.

- **Recursive Folder Traversal and Structure Replication:**  
  - Recursively navigates through the OneDrive interface, identifying folders and files.  
  - Uses a simple heuristic (if an item’s name contains a period, it is treated as a file; otherwise, it’s considered a folder) to distinguish between files and folders.  
  - For each folder encountered, it creates a corresponding local directory on the external drive and recursively processes its contents.
  - After processing a folder, it navigates back to the parent folder.

- **File Downloading:**  
  - For each file, the script simulates a right-click to open the context menu and selects the "Download" option.
  - It waits for the download to complete by polling the file’s size until it stabilizes.
  - Once confirmed, the file is moved from the default download directory to its respective subfolder, thus preserving the original OneDrive hierarchy.

## Requirements

- Python 3.x
- Selenium
- webdriver-manager
- Google Chrome (or another supported browser configured for Selenium)
- Sufficient space on the target (external) drive

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
	```
2. **Install Dependencies:**

   ```bash	
   pip install selenium webdriver-manager
   ```
# Usage

## Configuration

- Update the onedrive_url variable with your OneDrive login page URL.
- Ensure that the download_path variable points to your local directory (e.g., your external drive).

## Run the Script
   ```bash
   python onedrive_downloader.py
   ```
## Manual Login

When prompted, log in to your OneDrive account manually in the browser window.

## Download Process

The script will recursively traverse your OneDrive folders, downloading files and replicating the folder structure locally.

# Limitations and Considerations

## Folder vs. File Detection

The script currently distinguishes folders from files by checking if the item’s name contains a period (.). If your OneDrive naming conventions differ, modify the is_folder() function accordingly.

## Dynamic Content Loading

OneDrive’s web interface loads elements asynchronously. The script uses explicit waits (via Selenium's WebDriverWait) to handle this. Depending on your network speed and system performance, you might need to adjust the wait times.

## Download Completion

The script monitors the default download directory and waits until a file's size becomes stable before moving it to its designated folder. Adjust the timeout and check intervals if necessary for larger files or slower downloads.

# Contributing

Contributions, suggestions, and improvements are welcome! Please open an issue or submit a pull request with any improvements or bug fixes.

# License

This project is licensed under the MIT License.





