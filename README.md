# Laravel Brute Force Script

## Introduction

This Python script performs a brute force attack on Laravel login pages that are vulnerable due to the absence of throttle and security mechanisms like rate limiting and most importantly using common passwords. It's designed to automate login attempts and check if a correct password is found based on the page's response.

**Important**: This tool is intended for educational purposes and to raise awareness about common vulnerabilities in Laravel applications. Always ensure you have permission to perform penetration testing on the target system.

## Features

- **Automated Brute Force**: Uses a wordlist to attempt login with various passwords.
- **CSRF Token Handling**: Automatically fetches and handles CSRF tokens for each request.
- **Success Verification**: Checks for successful login by inspecting redirects or session cookies.
- **Customizable Parameters**: Allows customization for URL, username, wordlist path, and other parameters.

## Installation

To use this script, ensure you have the following dependencies installed:

- Python 3.x
- `requests` library
- `beautifulsoup4` library

You can install the required dependencies using `pip`:

```bash
pip install requests beautifulsoup4

```Python
python3 laravel_brute.py

Disclaimer: This tool should only be used on systems where you have explicit permission to conduct penetration testing. Unauthorized use of this tool is illegal and unethical.


