#!/bin/bash

# Get the current Google Chrome version
CHROME_VERSION=$(google-chrome --version | grep -oP '(\d+)\.(\d+)\.(\d+)\.(\d+)' | head -1)
CHROME_DRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")

# Download the ChromeDriver
wget https://chromedriver.storage.googleapis.com/123.0.6312.122/chromedriver_linux64.zip

# Unzip the ChromeDriver and move it to /usr/local/bin
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/

# Clean up
rm chromedriver_linux64.zip

# Verify installation
chromedriver --version
