from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    JavascriptException,
    WebDriverException,
    ElementClickInterceptedException,
    TimeoutException,
)
from config import settings, print_log
from datetime import datetime, timedelta
import time

MAX_ATTEMPTS = 30


class PadelBot:
    def __init__(self, driver):
        self.driver = driver
        self.slot_time = settings.SLOT.split(":")
        self.target_slot = datetime(
            settings.YEAR,
            settings.MONTH_NBR,
            int(settings.DATE),
            int(self.slot_time[0]),
            int(self.slot_time[1]),
            0,
        )

    def find_date(self, target_day: str, target_date: int, target_month: str):
        """Return the target date button"""
        date_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.day-btn"))
        )

        for button in date_buttons:
            try:
                day_elem = button.find_element(By.CSS_SELECTOR, "p.day")
                date_elem = button.find_element(By.CSS_SELECTOR, "p.day-number")
                month_elem = button.find_element(By.CSS_SELECTOR, "p.month")

                day_text = day_elem.text.strip()
                date_text = date_elem.text.strip()
                month_text = month_elem.text.strip()

                if (
                    day_text == target_day
                    and date_text == str(target_date)
                    and month_text == target_month
                ):
                    return button
            except:
                continue

        raise Exception("Can't find the date you are looking for")

    def find_slot(self, target_slot: str):
        """Return the target slot button"""
        slot_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button.slot-button-small")
            )
        )

        for slot in slot_buttons:
            text = slot.text.strip()
            print_log("Found slot: ", repr(text))
            if target_slot == text:
                return slot

        raise Exception("Can't find the slot you are looking for")

    def find_resa(self):
        """Return the target reservation button"""
        resa_infos = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.card-body-session-description")
            )
        )
        resa_infos = self.driver.find_elements(
            By.CSS_SELECTOR, "div.card-body-session-description"
        )

        for resa in resa_infos:
            info = resa.find_element(By.CSS_SELECTOR, "p.time").text
            split = [p.strip() for p in info.split("-")]
            if len(split) >= 3:
                duration = split[-1]
                print_log("Found resa: ", duration)
                if duration == settings.DURATION:
                    button = resa.find_element(
                        By.XPATH, "../../following-sibling::div[@class='tarif']//button"
                    )
                    return button

        raise Exception("Can't find the resa you are looking for")

    def connection(self):
        """Log in to the website"""
        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))
        )
        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
        )

        username.clear()
        password.clear()
        username.send_keys(settings.USERNAME)
        password.send_keys(settings.PASSWORD)

        self.driver.find_element(By.CSS_SELECTOR, "button.email-link-btn").click()

    def input_gymlib_codes(self):
        """Input and submit Gymlib codes"""
        promo_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.addCodePromo"))
        )
        promo_btn.click()

        gymlib_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.gymlib.club"))
        )
        gymlib_btn.click()

        for i in range(len(settings.GYMLIB_CODES)):
            gym_code = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        f"input.input[placeholder='Code gymlib du joueur {i + 1}']",
                    )
                )
            )
            gym_code.clear()
            gym_code.send_keys(settings.GYMLIB_CODES[i])

            email = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        f"input.input[placeholder='Email gymlib du joueur {i + 1}']",
                    )
                )
            )
            email.clear()
            email.send_keys(settings.EMAILS[i])

        self.click_btn(By.CSS_SELECTOR, "button.submit.mx-auto", "submit_btn")

    def payment_info(self):
        """Input and submit payment informations"""
        first_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "firstname"))
        )
        first_name.clear()
        first_name.send_keys(settings.FIRST_NAME)

        last_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "lastName"))
        )
        last_name.clear()
        last_name.send_keys(settings.LAST_NAME)

        self.click_btn(By.ID, "submit", "confirm_btn")
        print_log("Success: personal info filled")

        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (
                    By.CSS_SELECTOR,
                    "iframe[title='Cadre de saisie sécurisé pour le paiement']",
                )
            )
        )

        card_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-value="card"]'))
        )
        card_btn.click()

        card_nbr = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "number"))
        )
        card_nbr.click()
        card_nbr.clear()
        card_nbr.send_keys(settings.CARD_NUMBER)

        exp = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Field-expiryInput"))
        )
        exp.clear()
        exp.send_keys(settings.EXP_DATE)

        cvc = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Field-cvcInput"))
        )
        cvc.clear()
        cvc.send_keys(settings.CVC)

        print_log("Success: credit card info filled")
        self.click_btn(By.ID, "submit", "checkout")

    def click_with_js(self, by: By, value: str, description: str) -> bool:
        """Finds element and clicks on it"""
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            print_log(f"Clicked on {description}")
            return True
        except NoSuchElementException:
            print_log(f"Error: {description} not found")
        except JavascriptException as e:
            print_log(f"Error: JS click failed for {description}")
        except WebDriverException as e:
            print_log(f"Error: webdriver exception while trying to click {description}")
        except Exception as e:
            print_log(f"Error: unexpected error clicking {description}: {e}")
        return False

    def get_date(self):
        """Search and click target date"""
        MONTHS = [
            "Jan.",
            "Feb.",
            "Mar.",
            "Apr.",
            "May.",
            "Jun.",
            "Jul.",
            "Aug.",
            "Sep.",
            "Oct.",
            "Nov.",
            "Dec.",
        ]
        MONTH = MONTHS[settings.MONTH_NBR - 1]
        attempts = 0

        while attempts < MAX_ATTEMPTS:
            try:
                date_btn = self.find_date(settings.DAY, settings.DATE, MONTH)
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(date_btn)
                )
                time.sleep(0.2)
                date_btn.click()
                print_log("Success: date found")
                return
            except Exception as e:
                print_log("Error: date not found: ", e)
                self.driver.refresh()
                time.sleep(0.5)
                attempts += 1

    def get_slot(self):
        """Search and click target slot"""
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            try:
                slot_btn = self.find_slot(settings.SLOT)
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(slot_btn)
                )
                slot_btn.click()
                print_log("Success: slot found")
                return
            except Exception as e:
                print_log("Error: slot not found: ", e)
                self.driver.get(settings.RESERVATION_PAGE)
                time.sleep(0.5)
                self.get_date()
                attempts += 1

    def get_resa(self):
        """Search and click target reservation"""
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            try:
                resa_btn = self.find_resa()
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(resa_btn)
                )
                resa_btn.click()
                print_log("Success: resa found")
                return
            except Exception as e:
                print_log("Error: resa not found: ", e)
                self.driver.get(settings.RESERVATION_PAGE)
                time.sleep(0.5)
                self.get_date()
                self.get_slot()
                attempts += 1

    def login(self):
        """Go to log in page and log in"""
        if self.driver.current_url.startswith(settings.RESERVATION_PAGE):
            print_log("No need to log in")
            return

        try:
            if not self.driver.current_url.startswith(settings.LOGIN_PAGE):
                self.driver.get(settings.LOGIN_PAGE)
            self.connection()
            print_log("Success: connection")
        except:
            raise Exception("connection failed")

    def make_reservation(self):
        """Go to reservation page and make the reservation"""
        if not self.driver.current_url.startswith(settings.RESERVATION_PAGE):
            self.driver.get(settings.RESERVATION_PAGE)

        self.get_date()
        self.get_slot()
        self.get_resa()

    def click_btn(self, by: By, value: str, description: str):
        """Wait for element to be clickable and click"""
        while True:
            try:
                pay_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, value))
                )
                pay_btn.click()
                break
            except NoSuchElementException:
                print_log(f"ERROR: {description} not found")
            except ElementClickInterceptedException:
                print_log(f"ERROR: {description} not clickable")
            except TimeoutException:
                print_log(f"ERROR: timeout while trying to click {description}")
            except Exception as e:
                print_log(
                    f"ERROR: unexpected error while trying to click {description}: {e}"
                )

    def confirm_cart(self):
        """Click the checkbox and click the submit button"""
        ret = False
        while not ret:
            ret = self.click_with_js(By.XPATH, "//input[@type='checkbox']", "checkbox")
            if not ret:
                time.sleep(0.3)

        self.click_btn(By.CSS_SELECTOR, "button.rcorners.btn-marginTop", "pay_btn")

    def bot_wait(self, action: str, start_time: any):
        """Wait until start_time"""
        print_log("Target slot = ", self.target_slot, settings.DURATION)
        print_log(f"{action} start time = ", start_time)

        print_log("Waiting...")
        while datetime.now() < start_time:
            time.sleep(0.5)
        print_log("Wait is over")

    def login_and_wait(self):
        """Logs in 1 minute before the slot release and waits for the slot"""
        login_time = self.target_slot - timedelta(days=6, minutes=1)
        self.bot_wait("Login", login_time)
        self.login()

        start_time = self.target_slot - timedelta(
            days=6, seconds=settings.SECONDS_BEFORE_START
        )
        self.bot_wait("Make reservation", start_time)
