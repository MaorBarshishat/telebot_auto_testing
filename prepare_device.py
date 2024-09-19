from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
import os
import dotenv

# initializing the connnection parameters with the device
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'Samsung Galaxy S10'
options.udid = 'emulator-5554'
options.automation_name = 'UiAutomator2'
options.auto_grant_permissions = True

dotenv.load_dotenv()
appium_server_url =os.getenv('APPIUM_SERVER_URL')

def prepare_bot_session():
    try:
        """
         the function prepare the device to make a telegram session with the bot
         """
        driver = webdriver.Remote(appium_server_url, options=options)

        if str(driver.current_package) == "org.telegram.messenger.web":      # in case the device already in telegram
            print ("Telegram is active, bye.")
            return

        wait = WebDriverWait(driver, 60)  # Waiter - up to 60 seconds

        # enter the app
        element = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Telegram")))
        element.click()

        sleep(3)

        # click on the search bar
        element = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                           value="""new UiSelector().className("android.widget.ImageView").instance(1)""")
        element.click()

        # enter the bot name
        element = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
        element.send_keys("@maor_practice_bot")

        # enter to the bot chat
        element = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                           value="""new UiSelector().text("Maor's Bot, bot")""")
        element.click()

        print("The session with the bot is ready")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    prepare_bot_session()