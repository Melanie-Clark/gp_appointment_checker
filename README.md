# GP Appointment Checker

_Note: App currently under development_

_Designed for macOS and TPP SystmOnline users only_

This MacOS app sends an **e-mail notification** when **new GP appointments** become available via **SystmOnline**:

https://systmonline.tpp-uk.com/2/MainMenu

It uses Selenium to automate logging in to your GP surgery’s SystmOnline portal, checks the appointment list, and notifies you when a new appointment becomes available.

When the application is first run, the app will initially e-mail you a list of all available appointments, followed by e-mail notifications when new appointments become available (_only while the app is running_).

## Benefits
As we all know GP surgeries are increasingly busy, and it can be difficult to get an appointment. This app helps by:
- Reduction in manual effort from repetitive logging in and navigating to find new appointments
- No need to remember your login details - Helpful if like me you keep forgetting them!
- Perfect opportunity to grab that next available appointment before someone else
- Saves valuable time to continue with your day
- Sends a notification e-mail with new appointments

## Important Note
Please use this app in accordance with TPP's usage policy. This tool is intended for responsible, personal use only. It's recommended to run checks for a limited period of time or run checks hourly to avoid overloading the SystmOnline service.

_"1.2 You may not use SystmOnline in an unlawful manner or any manner that could damage, disable, overburden, or impair SystmOnline (or servers or networks connected to SystmOnline), nor may you use SystmOnline in any manner that could interfere with any other party’s use and enjoyment of SystmOnline (or servers or networks connected to SystmOnline)"_

<strong>Reference: </strong>\
<em>[SystmOnline Terms of Use](https://systmonline.tpp-uk.com/Safeguarding/privacy/privacy.html)</em>

**Disclaimer:**  
<em>This project is not affiliated with or endorsed by TPP. Users are responsible for ensuring their use complies with all applicable terms, conditions, and laws.</em> 

## Dependencies
- MacOS
- SystmOnline login details


## Set-up Instructions:

### 1. Install Homebrew
`which brew || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

If Homebrew is already installed it will output a path like:

**/usr/local/bin/brew**

### 2. Install Python
How to check if Python is already installed: 

`python3 --version`

Install Python command:

`brew install python3`

### 3. Install Chrome and ChromeDriver
How to check if Chrome is already installed: 

`ls /Applications/Google\ Chrome.app`

Install Chrome command:

`brew install --cask google-chrome`

How to check if ChromeDriver is already installed: 

`which chromedriver`

Install ChromeDriver command:

`brew install --cask chromedriver`

### 4. Install Python Packages
`pip install -r requirements.txt`

### 5. Create a .env file in the project directory

```
USERNAME=myusername
PASSWORD=mypassword
EMAIL_FROM=myemail@gmail.com
EMAIL_TO=myemail@gmail.com
EMAIL_PASSWORD=my_google_app_password
```

Note: Use a Gmail App Password, not your Gmail password:

[Setup a Gmail App password](https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4OTQNPYQgK_TJG1WYmBJ9wLe7CicYCs3AflM7ew7Ft9ttIbiV5Ute5lvWbxsy_8Iwo2Bq7DbrmFh3sZj4xY4jg5RaGhkEEygwHyFV4Ry_V8_atz5mI)
