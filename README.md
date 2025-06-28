# GP New Appointment Notifications

_Note: App currently under development_

_Designed for macOS and TPP SystmOnline users only_

This MacOS app sends an **e-mail notification** when **new GP appointments** become available via **SystmOnline**:

https://systmonline.tpp-uk.com/2/MainMenu

It uses Selenium to automate logging in to your GP surgery’s SystmOnline portal, checks the appointment list, and notifies you when a new appointment becomes available.

When the application is first run, the app will initially e-mail you a list of all available appointments, followed by any new appointments e-mail notifications as and when they become available (_whilst the application is running_).

## Benefits
As we all know GP surgeries are increasingly busy, and it can be difficult to get an appointment. This app helps by:
- Reducing the manual effort of repetitively logging in and checking for new appointments
- No need to remember your login details - Helpful if like me you keep forgetting them!
- Perfect opportunity to grab that next available appointment before someone else
- Saving you valuable time to continue with your day


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
