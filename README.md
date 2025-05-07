# Laravel Brute Force Script

This script was designed and developed to brute force Laravel authentication systems that lack proper throttle mechanisms and security protections. It automates login attempts using a wordlist and verifies if the login is successful based on specific success indicators.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

This Python script performs a brute force attack on Laravel login pages that are vulnerable due to the absence of throttle and security mechanisms like rate limiting. It's designed to automate login attempts and check if a correct password is found based on the page's response.

> **Important**: This tool is intended for educational purposes and to raise awareness about common vulnerabilities in Laravel applications. Always ensure you have permission to perform penetration testing on the target system.

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

You can install the required dependencies using pip:

```bash
pip install requests beautifulsoup4
