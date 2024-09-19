# TeleBot Auto Testing

This Appium client was developed to automatically test the TeleBot. It communicates with an Appium server to execute the tests.

### Features:
- **Automated Testing:** This client simulates user interactions to automatically test the TeleBot's functionality.
- **Server Communication:** The client communicates with an Appium server to manage and execute test cases.

### Running the Tests:
You can run the tests either as a Docker container or as a Python program.
### as a docker:
```
   sudo docker run -d maorbarshishat/appium_client_auto_test_maor:2.0
```

### as a python command:
 ```
    git clone https://github.com/MaorBarshishat/telebot_auto_testing.git
    cd telebot_auto_testing/
    pip install -r requirements.txt
    python3 prepare_device.py
    python3 testing.py
```
