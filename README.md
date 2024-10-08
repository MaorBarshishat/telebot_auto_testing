# TeleBot Auto Testing

This Appium client was developed to automatically test the [TeleBot](https://github.com/MaorBarshishat/telebot). It communicates with an [Appium server with AVD/ADBE](https://github.com/MaorBarshishat/avd_adb_appium_server) to execute the tests through the Android emulator UI.

### Features:
- **Automated Testing:** This client simulates user interactions to automatically test the TeleBot's functionality.
- **Server Communication:** The client communicates with an Appium server to manage and execute test cases.

### Three automated tests are supported:
1. Sending a *.jpg image should pass the test
2. Sending text instead of an image will cause an error (The bot replies with an error message)
3. Sending files that are not *.jpg/*.jpeg will cause an error (The bot replies with an error message)
   
### Running the Tests:
Each execution of the python script will execute the three tests and the results will be printed out.
The tests can be executed either as a Docker container or as a Python program on host.

### as a docker:
```
   sudo docker network create --subnet=172.18.0.0/16 net_maor
   sudo docker run -ti --net net_maor --ip 172.18.0.3  maorbarshishat/appium_client_auto_test_maor:2.2
```
note: if net_maor was already created, an error message will appear, so plz ignore it.

### executed on host using python command:
Please make sure you have python3 and pip3 installed on your machine.<br />
The installation
 ```
    git clone https://github.com/MaorBarshishat/telebot_auto_testing.git
    cd telebot_auto_testing/
    pip install -r requirements.txt
 ```
The following will be executed to apply the tests
 ```
    python3 testing.py
```

