# TeleBot Auto Testing

This is an Appium client designed to automatically test the TeleBot. It communicates with the Appium server to perform automated testing.

### Running the Tests
You can execute the tests either as a Docker container or as a Python program.

#### Running as a Docker Container:

1. Clone the repository:
    ```
    git clone https://github.com/MaorBarshishat/telebot_auto_testing.git
    ```

2. Navigate to the project directory:
    ```
    cd telebot_auto_testing/
    ```

3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Prepare the device:
    ```
    python3 prepare_device.py
    ```

5. Run the test script:
    ```
    python3 testing.py
    ```
