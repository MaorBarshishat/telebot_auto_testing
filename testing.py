from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
import unittest
import os
from selenium.webdriver.support import expected_conditions as EC        # for 'wait until' precess
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
import dotenv

BAD_MESSAGE_TYPE = 'ERROR'
BAD_VIDEO_MESSAGE = "Such video is not supported"
BAD_TEXT_MESSAGE = "Such text is not supported"

CORRECT_MESSAGE_TYPE = 'SUCCESS'
CORRECT_PHOTO_HASHED = "dcd777da5adf6371486e2b75572ebb46"

PHOTO_INDEX_MEDIA = 1
VIDEO_INDEX_MEDIA = 0

WAIT_FOR_VIDEO = 10

# define headers session
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'
options.automation_name = 'UiAutomator2'
options.no_reset = True
options.app_package = "org.telegram.messenger.web"
options.app_activity = "org.telegram.ui.LaunchActivity"


dotenv.load_dotenv()
appium_server_url = os.getenv('APPIUM_SERVER_URL')


def is_element_present(by, value, driver):
    """
    the function check if the element exist
    :param by: selector
    :param value: value
    """
    try:
        driver.find_element(by, value)
        return True
    except Exception as e:
        return False


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.driver = None  # connect to the appium server

        except Exception as e:
            print('ERROR: ', str(e))
            self.driver.quit()

        # sleep(3)        # wait until the device loaded

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def reset_driver(self):
        try:
            """
             the function reset the driver instance (in case not None), than enter to telegram and the The intended chat 
             this function is called in every test - the purpose - prevent any effect on another tests, so every test starts from "restart"
             """
            if self.driver:
                self.driver.quit()

            self.driver = webdriver.Remote(appium_server_url, options=options)
            sleep(3)

            # click on the search bar
            element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                          value="""new UiSelector().className("android.widget.ImageView").instance(1)""")
            element.click()

            # enter the bot name
            element = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
            element.send_keys("@maor_practice_bot")

            # enter to the bot chat
            element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                          value="""new UiSelector().text("Maor's Bot, bot")""")
            element.click()

            print("The session with the bot is ready")
            return
        except Exception as e:
            print(e)

    def send_media(self, index_media):
        """
        the function send media (photo/video) to the telegram bot
        :param index_media: index in the gallery of the device.
                         PHOTO_INDEX_MEDIA - index of photo
                         VIDEO_INDEX_MEDIA - index of video
        """

        wait = WebDriverWait(self.driver, 50)  # Wait up to 30 seconds until specified element is available

        # press on the send media type message
        element = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Attach media')
        element.click()

        # select media (photo/video) by index_media
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                           value=f'new UiSelector().className("android.view.View").instance({index_media})')
        element.click()

        # send the media to the bot
        element = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Send')))
        element.click()

    def send_message(self, message):
        """
        the function send message to the bot
        :param message: text to send
        :return:
        """

        wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds until specified element is available

        # put the message in the writing bar
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                           value='new UiSelector().description("Web tabs ")')
        element.click()

        element = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
        element.click()
        element.send_keys(message)

        # send the message
        element = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Send')))
        element.click()

    def check_received_message(self, type_message_expected, sec_to_sleep = 5):
        """
        the function get the received message from the bot and compare the expected type with the output
        :param sec_to_sleep:  seconds to sleep
        :param type_message_expected: CORRECT_MESSAGE_TYPE/BAD_TEXT_MESSAGE
        :return: the received message
        """
        sleep(sec_to_sleep)        # Wait 10 seconds to the message received

        # get the text of the last message sent
        received_message = self.driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.view.ViewGroup')[-1].text

        # fail the test in case the message does not start with the type_message_expected
        self.assertTrue(received_message.startswith(type_message_expected),
                        f'Expected {type_message_expected} type message')

        return received_message



    def test_send_photo(self) -> None:
        """
        the function test the bot in case the client want to hash jpg/jpeg photo.
        the test check about right case.
        the expected answer is: SUCCESS: your file hashed by md5 algorithm: 10ce70127c9dcd8bdfa017920af67ba9
        """
        self.reset_driver()
        self.send_media(PHOTO_INDEX_MEDIA)
        received_message = self.check_received_message(CORRECT_MESSAGE_TYPE)

        # check if the hash is correct
        self.assertTrue(CORRECT_PHOTO_HASHED in received_message,
                        f'''Wrong hash for photo, expected: '{CORRECT_PHOTO_HASHED}' ''')

        print("send photo test - success")


    def test_send_video(self) -> None:
        """
        the function test the bot in case the client send video.
        the test check about wrong case, the bot hash only jpg/jpeg files - any other file returns error.
        the expected answer is: ERROR: Such video is not supported, Only .jpg or .jpeg files
        """
        self.reset_driver()
        self.send_media(VIDEO_INDEX_MEDIA)
        received_message = self.check_received_message(BAD_MESSAGE_TYPE, WAIT_FOR_VIDEO)

        self.assertTrue(BAD_VIDEO_MESSAGE in received_message,
                        f'''Wrong error message, expected: '{BAD_VIDEO_MESSAGE}' ''')

        print("send video test - success")


    def test_send_text(self) -> None:
        """
        the function test the bot in case the client send video.
        the test check about wrong case, the bot hash only jpg/jpeg files - any other message includes text will get error.
        the expected answer is: ERROR: Such text is not supported, Only .jpg or .jpeg files
        """
        self.reset_driver()
        self.send_message('this is text that should get an error')
        received_message = self.check_received_message(BAD_MESSAGE_TYPE)

        # check if the error message is correct
        self.assertTrue(BAD_TEXT_MESSAGE in received_message,
                        f'''Wrong error message, expected: '{BAD_TEXT_MESSAGE}' ''')

        print("send text test - success")


if __name__ == '__main__':
    unittest.main()
