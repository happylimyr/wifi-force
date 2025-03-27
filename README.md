# Wi-Fi Auto Connect

## Description

This project is a Python-based Wi-Fi connection automation tool that attempts to connect to a specified Wi-Fi network by iterating through a generated list of passwords. It is designed for testing purposes and ensures that available networks are displayed before attempting a connection.

## Features

- Retrieves and displays available Wi-Fi networks.
- Automatically generates passwords from `00000000` to `99999999`.
- Attempts to connect to a specified Wi-Fi network using generated passwords.
- Uses Windows `netsh` commands for managing Wi-Fi profiles and connections.

## Requirements

- Windows OS
- Python 3.x
- `keyboard` module (for handling key events)

## Installation

1. Install required dependencies:
   ```sh
   pip install keyboard
   ```

## Usage

1. Run the script:
   ```sh
   python wifi.py
   ```
2. Select an available network and start the connection process.
3. The script will attempt to connect using generated passwords.
4. Press `ESC` to exit the program at any time.

## Disclaimer

This tool is strictly for educational and testing purposes. Unauthorized attempts to access networks without permission may violate laws and regulations.

##

