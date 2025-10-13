from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bot import PadelBot, WebDriverWait, settings, EC, By
from config import print_log


def main():
    driver = webdriver.Chrome()
    driver.get(settings.LOGIN_PAGE)

    pb = PadelBot(driver)
    pb.login_and_wait()

    while True:
        try:
            pb.login()
            pb.make_reservation()
            print_log("Success: reservation selected")
            print_log("Looking for checkout page...")
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3.recap-title"))
            )
            print_log("Website redirecting us to checkout")
            break
        except Exception as e:
            if isinstance(e, TimeoutException):
                print_log("Website redirected us to login...")
            else:
                print_log("Error: ", e)

    try:
        pb.input_gymlib_codes()
        pb.confirm_cart()
        # pb.payment_info()

    except Exception as e:
        print_log("Error: ", e)

    input("PRESS ENTER TO CLOSE WINDOW AND QUIT")
    driver.quit()


if __name__ == "__main__":
    main()
