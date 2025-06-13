# EZ Meal Sync v1.0

A meal planning software that integrates with Google Keep to create a random
list of meals and generates an organized ingredient list, assisting with meal
planning and grocery shopping.

## Features

- Integrates with gkeepapi to manage meal generations and a running grocery list.
- Instead of taking time to choose meals for the week and create a matching
ingredient list, you’ll save much more time by simply removing items from the
list of ingredients you already have in stock.
- Generates a random list of meals without recent repeats.
- Straightforward user interface allows for quick and seamless program setup.

## Getting Started

### Prerequisites

- Designed for Windows (untested on Mac & Linux)
- Python 3.13
- Other libraries (as noted in requirements.txt)
- gkeepapi documentation (https://gkeepapi.readthedocs.io/en/latest/index.html)
(includes information on how to obtain a master token)
- An active internet connection is necessary when the program is running in
order to access Google Keep.

### Steps to Install

1. Clone the repository:
   ```bash
   git clone https://github.com/username/project-name.git

2. An active Google account is necessary along with access to Google Keep. If
more information is needed to on how to create a Google account or Google
Keep, a simple internet/YouTube search will provide you with ample information
on where to get started.

3. After your Google Keep is set up, run the program and access the user
interface and proceed to the settings menu. Within there you will be prompted to
add
your email, oauth token, number of meals to be generated, and the name of your
preferred grocery store.

4. To obtain your oauth token, do as follows:
    - Go to the following website (https://accounts.google.com/EmbeddedSetup).
    - Login with the Google credentials that you will be using for your Google
    Keep.
    - Click "next" and then "I Agree".
    - The page will look like it is endlessly loading but it is functioning as
    it should.
    - Right click on the page and select "Inspect".
        - For Google Chrome, go to "Application" on the top.
        - For Microsoft Edge, there is an unnamed folder on the top that will
        say "Application" when clicked.
    - On the left, select the cookie dropdown and click on the item that is
    below cookies.
    - Scroll down in the list of names until you find "oauth_token" and copy
    the value (ensure you grab every character).
    - Paste your oauth_token when prompted within the user interface and it will
    run through a program and obtain your master token.
        - If at any point in time you change your Google password is changed,
        your oauth and master token will be invalid and need to be regenerated.
        - These token's can be used to access your account and should be kept
        private.
        - The oauth token is time sensitive and will expire in 1 hour, so it
        needs to be plugged in to the program prior to the expiration or it will
        need to be regenerated.
5. After your settings are configured, you will need to access the user
interface and add meals with their respective ingredients.
    - After entering a meal, if an ingredient has not been categorized by
    grocery department, you will be prompted to do so.
    - When a new list of meals is generated, it checks for repeats going back
    two runs ago. Therefore you will need to have enough meals created to
    have meals to be generated x3. For example, if 7 meals are being generated,
    then a minimum of 21 recipes will need to be created or an error will occur,
    preventing the generator from running.

## License
- GNU General Public License v3.0

## Contact
- Creator: Ezra Schier
- Contact: schier.ezra@gmail.com