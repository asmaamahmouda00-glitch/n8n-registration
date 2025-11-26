"""
WorldPosta Complete Automation Suite
All-in-one script for registration, email verification, and login automation
"""

import time
import random
import os
import csv
import json
import argparse
from datetime import datetime
from bs4 import BeautifulSoup

# Selenium / Driver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


# =====================================================
# CONFIGURATION
# =====================================================

REGISTRATION_URL = "https://admin.worldposta.com/auth/register"
EMAIL_LOGIN_URL = "https://mail.worldposta.com/"
LOGIN_URL = "https://admin.worldposta.com/auth/login"

EMAIL_DOMAIN = "@worldposta.com"
EMAIL_SUBJECT_KEYWORD = "Welcome To Worldposta"

EMAIL_WAIT_TIMEOUT = 300
DEFAULT_TIMEOUT = 30

# Save screenshots INSIDE repo
SCREENSHOT_DIR = "screenshots"

CSV_FILE = "registration_results.csv"
JSON_FILE = "registration_results.json"

CUSTOM_TEST_ACCOUNT = {
    'full_name': "AI dexter120",
    'email': "ai.dexter120@worldposta.com",
    'company': "AI Company dexter120",
    'phone': "01095666032",
    'password': "gtzwO@lvr+A82biD5Xdmepf7k/*y1"
}


# =====================================================
# UTILITIES
# =====================================================

def random_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))


def human_like_mouse_move(driver, element):
    try:
        ActionChains(driver).move_to_element(element).perform()
        random_delay(0.2, 0.5)
    except:
        pass


def human_like_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))


def generate_random_account():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    r = random.randint(1000, 9999)

    return {
        'full_name': f"Test User {r}",
        'email': f"testuser{timestamp}_{r}{EMAIL_DOMAIN}",
        'company': f"TestCorp{r}",
        'phone': f"+1555{random.randint(1000000, 9999999)}",
        'password': f"TestPass@{r}123"
    }


def ensure_directory(path):
    os.makedirs(path, exist_ok=True)


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_screenshot_filename(email, status):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = email.replace("@", "_at_").replace(".", "_")
    return f"{safe}_{status}_{ts}.png"


# =====================================================
# AUTOMATION BOT — START
# =====================================================

class WorldPostaAutomationBot:
    def __init__(self, headless=False):
        print("🌐 Launching Chrome (system installation)...")

        ensure_directory(SCREENSHOT_DIR)

        # Chrome flags
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        if headless:
            options.add_argument("--headless=new")

        # ============================================================
        # ✔ Use system Chrome installed via apt-get on GitHub Actions
        # ============================================================
        browser_executable_path = "/usr/bin/google-chrome"
        print("🌐 Launching Chrome (system installation)...")

        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        if headless:
            options.add_argument("--headless=new")

        # 💡 The correct UC launcher for system Chrome:
        self.driver = uc.Chrome(options=options, driver_executable_path=None, browser_executable_path="/usr/bin/google-chrome")


        # LAUNCH FIXED UC CHROME
        self.driver = uc.Chrome(
            options=options,
            browser_executable_path=browser_executable_path,
            driver_executable_path=driver_executable_path,
            use_subprocess=True
        )

        self.driver.set_page_load_timeout(60)
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)

        print("✅ Chrome launched successfully using system installation")
    # =====================================================
    # STEP 1 — REGISTRATION
    # =====================================================
    def register(self, account_data):
        print("\n" + "="*60)
        print("📝 STEP 1: REGISTRATION")
        print("="*60)

        self.account_data = account_data
        self.status_log = {'email': account_data['email']}

        try:
            print(f"🔗 Navigating to: {REGISTRATION_URL}")
            self.driver.get(REGISTRATION_URL)
            random_delay(3, 5)

            print("📜 Scrolling to registration form...")
            self.driver.execute_script("window.scrollTo(0, 400);")
            random_delay(1, 2)

            # Full name
            full_name_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="FullName"]'))
            )
            human_like_mouse_move(self.driver, full_name_input)
            full_name_input.click()
            human_like_typing(full_name_input, account_data['full_name'])

            # Email
            email_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="Email"]')
            human_like_mouse_move(self.driver, email_input)
            email_input.click()
            human_like_typing(email_input, account_data['email'])

            # Company
            company_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="Customer"]')
            human_like_mouse_move(self.driver, company_input)
            company_input.click()
            human_like_typing(company_input, account_data['company'])

            # Phone
            phone_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="PhoneNumber"]')
            human_like_mouse_move(self.driver, phone_input)
            phone_input.click()
            human_like_typing(phone_input, account_data['phone'])

            # Password
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="Password"]')
            human_like_mouse_move(self.driver, password_input)
            password_input.click()
            human_like_typing(password_input, account_data['password'])

            confirm_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="ConfirmPassword"]')
            human_like_mouse_move(self.driver, confirm_input)
            confirm_input.click()
            human_like_typing(confirm_input, account_data['password'])

            # Submit
            submit_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#create-account"))
            )
            human_like_mouse_move(self.driver, submit_btn)
            self.driver.execute_script("arguments[0].click();", submit_btn)

            random_delay(5, 7)

            # Screenshot
            screenshot_path = os.path.join(
                SCREENSHOT_DIR,
                get_screenshot_filename(account_data['email'], "registration")
            )
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")

            return True

        except Exception as e:
            print(f"❌ Registration failed: {e}")
            self.status_log['error_message'] = str(e)

            screenshot_path = os.path.join(
                SCREENSHOT_DIR,
                get_screenshot_filename(account_data['email'], "registration_error")
            )
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Error screenshot saved: {screenshot_path}")

            return False


    # =====================================================
    # STEP 2 — EMAIL LOGIN (OWA)
    # =====================================================
    def login_to_email(self, email, password):
        print("\n" + "="*60)
        print("📬 STEP 2: EMAIL LOGIN")
        print("="*60)

        try:
            print(f"🔗 Opening: {EMAIL_LOGIN_URL}")
            self.driver.get(EMAIL_LOGIN_URL)
            random_delay(2, 4)

            username = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            username.clear()
            username.send_keys(email)

            pwd = self.driver.find_element(By.ID, "password")
            pwd.clear()
            pwd.send_keys(password)

            pwd.send_keys("\n")
            random_delay(3, 6)

            # Handle first-time timezone page
            self.handle_language_selection()

            print("📄 URL:", self.driver.current_url)
            print("📌 Title:", self.driver.title)

            if "/owa/" not in self.driver.current_url.lower():
                print("❌ Login did NOT reach inbox.")
                screenshot_path = os.path.join(
                    SCREENSHOT_DIR,
                    get_screenshot_filename(email, "email_login_failed")
                )
                self.driver.save_screenshot(screenshot_path)
                return False

            screenshot_path = os.path.join(
                SCREENSHOT_DIR,
                get_screenshot_filename(email, "email_login")
            )
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")

            return True

        except Exception as e:
            print(f"❌ Email login failed: {e}")
            self.status_log['error_message'] = str(e)
            return False


    # =====================================================
    # FIRST LOGIN — LANGUAGE & TIMEZONE PAGE FIX
    # =====================================================
    def handle_language_selection(self):
        try:
            if "languageselection" not in self.driver.current_url.lower():
                return False

            print("🌍 Language/Timezone page detected — applying settings...")

            tz = Select(self.driver.find_element(By.ID, "selTz"))
            tz.select_by_value("Egypt Standard Time")

            save_btn = self.driver.find_element(By.XPATH, "//span[text()='Save']/parent::div")
            save_btn.click()

            WebDriverWait(self.driver, 20).until(EC.url_contains("/owa/"))
            print("📬 Inbox loaded.")
            return True

        except Exception:
            return False


    # =====================================================
    # SHADOW DOM HELPER (used for deep nodes)
    # =====================================================
    def find_in_shadow_dom(self, selectors):
        script = """
        let el = document.querySelector(arguments[0]);
        for (let i=1; i < arguments.length; i++) {
            if (!el) return null;
            el = el.shadowRoot ? el.shadowRoot.querySelector(arguments[i]) : null;
        }
        return el;
        """
        return self.driver.execute_script(script, *selectors)
        # =====================================================
    # STEP 3 — FIND VERIFICATION EMAIL
    # =====================================================
    def find_verification_email(self, timeout=EMAIL_WAIT_TIMEOUT):
        print("\n" + "="*60)
        print("🔍 STEP 3: FINDING VERIFICATION EMAIL (OWA Selector Mode)")
        print("="*60)

        SUBJECT = EMAIL_SUBJECT_KEYWORD.lower()
        start = time.time()
        attempt = 0

        # Outlook Classic UI selectors
        INBOX_CONTAINER = 'div[autoid="_lvv_8"][role="listbox"]'
        ROW = 'div[autoid="_lvv_3"][role="option"]'
        SUBJECT_SPANS = 'span[autoid="_lvv_6"], span[autoid="_lvv_5"], span[autoid="_lvv_7"]'

        while time.time() - start < timeout:
            attempt += 1
            elapsed = int(time.time() - start)
            print(f"\n🔄 Attempt {attempt} (elapsed {elapsed}s/{timeout}s)")

            self.driver.refresh()
            time.sleep(3)

            # 1️⃣ Inbox present?
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, INBOX_CONTAINER))
                )
                print("📦 Inbox container loaded.")
            except:
                print("❌ Inbox container NOT found.")
                time.sleep(6)
                continue

            # 2️⃣ Rows present?
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ROW))
                )
                print("📨 Email rows detected.")
            except:
                print("📭 No rows yet — OWA still loading.")
                time.sleep(7)
                continue

            # 3️⃣ Loop rows
            rows = self.driver.find_elements(By.CSS_SELECTOR, ROW)
            print(f"📩 Found {len(rows)} rows.")

            for row in rows:
                try:
                    subjects = row.find_elements(By.CSS_SELECTOR, SUBJECT_SPANS)
                    full_text = " ".join([s.text.strip() for s in subjects if s.text.strip()])

                    print(f"   • Row text: {full_text[:80]}")

                    if SUBJECT in full_text.lower():
                        print("🎉 FOUND VERIFICATION EMAIL!")

                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior:'smooth',block:'center'});",
                            row
                        )
                        time.sleep(1)

                        row.click()
                        time.sleep(3)

                        screenshot = os.path.join(
                            SCREENSHOT_DIR,
                            get_screenshot_filename(self.account_data['email'], "email_found")
                        )
                        self.driver.save_screenshot(screenshot)
                        print(f"📸 Saved screenshot: {screenshot}")

                        return True

                except Exception as e:
                    print(f"⚠ Row error: {e}")

            # Not found yet
            print("⏳ Not found — retrying in 10 sec...")
            time.sleep(10)

        print("❌ Verification email NOT found.")
        return False



    # =====================================================
    # STEP 4 — EXTRACT VERIFICATION LINK
    # =====================================================
    def extract_verification_link(self):
        print("\n" + "="*60)
        print("🔗 STEP 4: EXTRACTING VERIFICATION LINK")
        print("="*60)

        try:
            time.sleep(3)

            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            print("🔍 Searching email body...")

            # Method 1: clickable text
            link = soup.find("a", string=lambda x: x and "Confirm Email" in x)
            if link and link.get("href"):
                url = link.get("href")
                print(f"✅ Found verification link (by text): {url}")
                return url

            # Method 2: href contains ConfirmEmail
            link = soup.find("a", href=lambda x: x and "ConfirmEmail" in x)
            if link and link.get("href"):
                url = link.get("href")
                print(f"✅ Found verification link (by pattern): {url}")
                return url

            # Method 3: Selenium — text
            try:
                btn = self.driver.find_element(By.XPATH, "//a[contains(text(),'Confirm Email')]")
                url = btn.get_attribute("href")
                if url:
                    print(f"✅ Found via Selenium: {url}")
                    return url
            except:
                pass

            # Method 4: Selenium — href pattern
            try:
                btn = self.driver.find_element(By.XPATH, "//a[contains(@href,'ConfirmEmail')]")
                url = btn.get_attribute("href")
                if url:
                    print(f"✅ Found via href match: {url}")
                    return url
            except:
                pass

            # Not found
            print("❌ Could NOT find verification link.")
            screenshot = os.path.join(
                SCREENSHOT_DIR,
                get_screenshot_filename(self.account_data['email'], "no_link_found")
            )
            self.driver.save_screenshot(screenshot)
            print(f"📸 Saved screenshot: {screenshot}")

            return None

        except Exception as e:
            print(f"❌ Error extracting link: {e}")
            return None
            # =====================================================
    # STEP 5 — CONFIRM EMAIL
    # =====================================================
    def confirm_email(self, verification_url):
        print("\n" + "="*60)
        print("✉️  STEP 5: CONFIRMING EMAIL")
        print("="*60)

        try:
            print(f"🔗 Opening verification URL...")
            self.driver.get(verification_url)
            time.sleep(5)

            screenshot = os.path.join(
                SCREENSHOT_DIR,
                get_screenshot_filename(self.account_data['email'], "email_confirmed")
            )
            self.driver.save_screenshot(screenshot)
            print(f"📸 Saved screenshot: {screenshot}")

            print("✅ Email confirmation complete.")
            return True

        except Exception as e:
            print(f"❌ Email confirmation failed: {e}")

            screenshot = os.path.join(
                SCREENSHOT_DIR,
                get_screenshot_filename(self.account_data['email'], "confirm_error")
            )
            self.driver.save_screenshot(screenshot)
            return False



    # =====================================================
    # STEP 6 — LOGIN TO WEBSITE (ADMIN PORTAL)
    # =====================================================
    def login_to_website(self, email, password):
        print("\n" + "="*60)
        print("🔐 STEP 6: LOGIN TO ADMIN WEBSITE")
        print("="*60)

        try:
            print(f"🔗 Going to login page: {LOGIN_URL}")
            self.driver.get(LOGIN_URL)
            time.sleep(3)

            # Email field
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="Email"]'))
            )
            email_input.clear()
            email_input.send_keys(email)
            time.sleep(1)

            # Password field
            pass_input = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="Password"]')
            pass_input.clear()
            pass_input.send_keys(password)
            time.sleep(1)

            # Submit
            signin_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#sign-in"))
            )
            signin_btn.click()

            time.sleep(5)

            screenshot = os.path.join(
                SCREENSHOT_DIR,
                get_screenshot_filename(email, "website_login")
            )
            self.driver.save_screenshot(screenshot)
            print(f"📸 Screenshot saved: {screenshot}")

            print("✅ Logged into website successfully.")
            return True

        except Exception as e:
            print(f"❌ Website login failed: {e}")

            screenshot = os.path.join(
                SCREENSHOT_DIR,
                get_screenshot_filename(email, "website_login_error")
            )
            self.driver.save_screenshot(screenshot)
            return False



    # =====================================================
    # STEP 7 — POST-LOGIN ACTIONS
    # =====================================================
    def perform_post_login_actions(self):
        print("\n" + "="*60)
        print("🎯 STEP 7: POST-LOGIN ACTIONS")
        print("="*60)

        try:
            time.sleep(4)

            # Scroll dashboard
            self.driver.execute_script("window.scrollTo(0, 600);")
            time.sleep(2)

            print("🔎 Searching for 'View Posta' and 'View CloudEdge' buttons...")

            buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.launch-button")
            print(f"   Found {len(buttons)} launch buttons")

            button_posta = None
            button_cloud = None

            for btn in buttons:
                t = btn.text.strip()
                if "View Posta" in t:
                    button_posta = btn
                if "View CloudEdge" in t:
                    button_cloud = btn

            # ============================
            # VIEW POSTA
            # ============================
            if button_posta:
                print("\n➡️ Opening Posta...")
                self.driver.execute_script("arguments[0].scrollIntoView();", button_posta)
                time.sleep(1)
                button_posta.click()
                time.sleep(4)

                screenshot = os.path.join(
                    SCREENSHOT_DIR,
                    get_screenshot_filename(self.account_data['email'], "view_posta")
                )
                self.driver.save_screenshot(screenshot)
                print(f"📸 Screenshot saved: {screenshot}")

                # Go back if still same tab
                try:
                    self.driver.back()
                    time.sleep(3)
                except:
                    pass

            # ============================
            # VIEW CLOUDEDGE
            # ============================
            if button_cloud:
                print("\n➡️ Opening CloudEdge...")
                button_cloud = self.driver.find_elements(By.CSS_SELECTOR, "button.launch-button")
                for btn in button_cloud:
                    if "View CloudEdge" in btn.text:
                        button_cloud = btn
                        break

                self.driver.execute_script("arguments[0].scrollIntoView();", button_cloud)
                time.sleep(1)
                button_cloud.click()
                time.sleep(4)

                screenshot = os.path.join(
                    SCREENSHOT_DIR,
                    get_screenshot_filename(self.account_data['email'], "view_cloudedge")
                )
                self.driver.save_screenshot(screenshot)
                print(f"📸 Screenshot saved: {screenshot}")

            print("\n✅ Post-login actions finished.")
            return True

        except Exception as e:
            print(f"❌ Post-login actions failed: {e}")

            screenshot = os.path.join(
                SCREENSHOT_DIR,
                get_screenshot_filename(self.account_data['email'], "post_login_error")
            )
            self.driver.save_screenshot(screenshot)

            return False
    # =====================================================
    # FINAL SCREENSHOT
    # =====================================================
    def take_final_screenshot(self):
        print("\n📸 Taking final screenshot...")
        try:
            screenshot_path = os.path.join(
                SCREENSHOT_DIR,
                get_screenshot_filename(self.account_data['email'], 'final_success')
            )
            self.driver.save_screenshot(screenshot_path)
            print(f"✅ Final screenshot saved: {screenshot_path}")
            return screenshot_path

        except Exception as e:
            print(f"⚠ Could not take final screenshot: {e}")
            return None



    # =====================================================
    # SAVE STATUS (CSV + JSON)
    # =====================================================
    def save_status(self):
        print("\n" + "="*60)
        print("💾 SAVING RESULTS")
        print("="*60)

        try:
            self.status_log['timestamp'] = get_timestamp()

            # CSV WRITE
            csv_exists = os.path.exists(CSV_FILE)
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=['timestamp', 'email', 'status', 'error_message', 'screenshot_path']
                )
                if not csv_exists:
                    writer.writeheader()
                writer.writerow(self.status_log)

            print(f"✅ Status saved to CSV: {CSV_FILE}")

            # JSON WRITE
            json_data = []
            if os.path.exists(JSON_FILE):
                try:
                    with open(JSON_FILE, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                except:
                    json_data = []

            json_data.append(self.status_log)

            with open(JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Status saved to JSON: {JSON_FILE}")

            # Display in Actions logs
            print("\n===== BEGIN_REGISTRATION_JSON =====")
            try:
                with open(JSON_FILE, 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                print(f"Cannot read {JSON_FILE}: {e}")
            print("===== END_REGISTRATION_JSON =====\n")

        except Exception as e:
            print(f"⚠ Error saving status: {e}")



    # =====================================================
    # FULL WORKFLOW
    # =====================================================
    def run_full_workflow(self, account_data):
        print("\n" + "="*60)
        print("🚀 STARTING FULL AUTOMATION WORKFLOW")
        print("="*60)

        try:
            print(f"\n📋 ACCOUNT DATA:")
            print(f"   Full Name : {account_data['full_name']}")
            print(f"   Email     : {account_data['email']}")
            print(f"   Company   : {account_data['company']}")
            print(f"   Phone     : {account_data['phone']}")
            print(f"   Password  : {'*' * len(account_data['password'])}")

            # Step 1 – Register
            if not self.register(account_data):
                self.status_log['status'] = 'failed_registration'
                self.save_status()
                return False

            # Step 2 – Login to OWA
            if not self.login_to_email(account_data['email'], account_data['password']):
                self.status_log['status'] = 'failed_email_login'
                self.save_status()
                return False

            # Step 3 – Find email
            if not self.find_verification_email():
                self.status_log['status'] = 'failed_email_not_found'
                self.save_status()
                return False

            # Step 4 – Extract link
            verification_url = self.extract_verification_link()
            if not verification_url:
                self.status_log['status'] = 'failed_no_link'
                self.save_status()
                return False

            # Step 5 – Confirm
            if not self.confirm_email(verification_url):
                self.status_log['status'] = 'failed_confirmation'
                self.save_status()
                return False

            # Step 6 – Login admin portal
            if not self.login_to_website(account_data['email'], account_data['password']):
                self.status_log['status'] = 'failed_website_login'
                self.save_status()
                return False

            # Step 7 – Post-login actions
            if not self.perform_post_login_actions():
                self.status_log['status'] = 'failed_post_login_actions'
                self.save_status()
                return False

            # Final screenshot
            self.take_final_screenshot()

            self.status_log['status'] = 'success'
            self.save_status()

            print("\n🎉 WORKFLOW COMPLETED SUCCESSFULLY!\n")
            return True

        except Exception as e:
            print(f"\n❌ FATAL WORKFLOW ERROR: {e}")
            self.status_log['error_message'] = str(e)
            self.status_log['status'] = 'failed_workflow_crash'
            self.save_status()
            return False



    # =====================================================
    # CLOSE BROWSER
    # =====================================================
    def close(self):
        print("\n🔒 Closing browser...")
        try:
            self.driver.quit()
            print("✅ Browser closed")
        except:
            print("⚠ Could not close browser")
# =====================================================
# WORKFLOW RUNNER
# =====================================================
def run_automation(headless=False, use_random=False):
    bot = None

    try:
        bot = WorldPostaAutomationBot(headless=headless)

        # Decide account type
        if use_random:
            account_data = generate_random_account()
            print(f"\n🎲 Using RANDOM account: {account_data['email']}")
        else:
            account_data = CUSTOM_TEST_ACCOUNT
            print(f"\n🎯 Using FIXED test account: {account_data['email']}")

        success = bot.run_full_workflow(account_data)

        if success:
            print("✨ Automation completed SUCCESSFULLY!")
        else:
            print("⚠ Automation completed with ERRORS.")

        return success

    finally:
        if bot:
            bot.close()



# =====================================================
# MAIN ENTRY POINT
# =====================================================
def main():
    parser = argparse.ArgumentParser(description="WorldPosta Automation Suite")

    parser.add_argument("--random", action="store_true", help="Use random account")
    parser.add_argument("--headless", action="store_true", help="Run without UI")

    args = parser.parse_args()

    print("="*60)
    print("🚀 WORLDPOSTA AUTOMATION SUITE")
    print("="*60)

    run_automation(
        headless=args.headless,
        use_random=args.random
    )


if __name__ == "__main__":
    main()


    
