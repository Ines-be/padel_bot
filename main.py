from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bot import PadelBot, WebDriverWait, settings, EC, By
from config import start_bot

def main():
    start_bot()

    driver = webdriver.Chrome()
    driver.get(settings.LOGIN_PAGE)

    pb = PadelBot(driver)

    while True:
        try:
            pb.co_and_resa()
            print("Success: reservation selected")
            print("Looking for checkout page...")
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3.recap-title"))
            )
            print("Website redirecting us to checkout")
            break
        except Exception as e:
            if isinstance(e, TimeoutException):
                print("Website redirected us to login...")
            else:
                print("Error: ", e)

    try:
        pb.input_gymlib_codes()

        accept = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']"))
        )
        accept.click()
        print("Terms accepted")

        pay = driver.find_element(By.CSS_SELECTOR, "button.rcorners.btn-marginTop")
        pay.click()
        print("Pay btn clicked")

        # pb.payment_info()

    except Exception as e:
        print("Error: ", e)

    input("PRESS ENTER TO CLOSE WINDOW AND QUIT")
    driver.quit()


if __name__ == "__main__":
    main()
