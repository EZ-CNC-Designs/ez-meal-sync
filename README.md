# EZ Meal Sync v1.0

EZ Meal Sync is meal planning app that integrates with Google Keep to create a random list of meals and generates an organized ingredient list, assisting with meal planning and grocery shopping.

## Features

- Integrates with gkeepapi to manage meal generations and a running grocery list.
- Instead of taking time to choose meals for the week and create a matching
ingredient list, you’ll save much more time by simply removing items from the
list of ingredients you already have in stock.
- Generates a random list of meals without recent repeats.
- Straightforward user interface allows for quick and seamless program setup.

## Why Use EZ Meal Sync
In the past, my wife & myselfs weekly meal planning went as follows: Someone suggests a meal, the other shoots it down & this discussion loops until a list of meals can be agreed upon. We'd scribble the meal names on a note pad & then go through the painstakingly annoying process of seaching Pinterest to gather up a list of ingredients for the corresponding meals. Those ingredients would then be added to our notepad. We would then go through the fridge & pantry & remove any ingredients that we have in stock. Then off to the grocery store we would go. We'd arrive at the grocery store & oops... we forgot the list at home... Guess we'll have to go off our memory.  

No longer will this process exist. Our new way of grocery shopping goes as follows. Open EZ Meal Sync, click a button to generate a new meal list, go through the fridge & pantry & remove any ingredients we have in stock, drive to the grocery store, & finally open our phones to view our grocery list.  

Meal planning does not get much easier than this. We recently have been generating enough meals for 2 weeks so we can save on impulse buys. Long gone are the time consuming days of meal planning.


## Getting Started

### Prerequisites

- Designed for Windows (untested on Mac & Linux)
- Python 3.13
- Other libraries (as noted in requirements.txt)
- gkeepapi documentation (https://gkeepapi.readthedocs.io/en/latest/index.html)
(includes information on how to obtain a master token)
- An active internet connection is necessary when the program is running in
order to access Google Keep.

### Steps to Install (or Non Programmers)

1. Create a Google Account  
An active Google account is necessary along with access to Google Keep. If
more information is needed to on how to create a Google account, a simple internet/YouTube search will provide you with ample information
on where to get started.


2. Download EZ Meal Sync  
Go the the following address to find the 


3. Obtain an Oauth Token  
A master token is needed as a sort of remote passkey to access your Google account. After an oauth token is obtained, it will be converted to a master token as seen in the following step.  

- To obtain your oauth token, do as follows:
    - Go to the following website (https://accounts.google.com/EmbeddedSetup).  
    - Login with the Google credentials that you will be using for your Google Keep.  
    - Click "next" and then "I Agree".  
    - The page will look like it is endlessly loading but it is functioning as it should.
    - Right click on the page and select "Inspect".  
    - For Google Chrome, go to "Application" on the top.  
    - For Microsoft Edge, there is an unnamed folder on the top that will say Application" when clicked.  
    - On the left, select the cookie dropdown and click on the item that is below cookies.  
    - Scroll down in the list of names until you find "oauth_token" and copy the value (ensure you grab every character). 
    - Open up the EZ Meal Sync program and click on "Settings". 
    - Paste your oauth_token within EZ Meal Sync's setting menu in the oauth token field. Enter the email address associated with your Google account & click on the button to generate a master token.
    - The master token will be generated & save within the app.
    - If at any point in time you change your Google password, your oauth and master token will become invalid and need to be regenerated. Otherwise a master token will only need to be generated once.
    - These token's can be used to access your account and should be kept private.  
    - The oauth token is time sensitive and will expire in 1 hour, so it needs to be plugged in to the program prior to the expiration or it will need to be regenerated.  


4. Configure Your Settings  
- Within EZ Meal Syncs menu, find your way to the settings menu. Enter how many meals you want to be generated at a time. This field will autosave after your quantity is entered.
- Next, enter the name of your prefered grocery store. This value will only be used to create a title for your grocery list. If you ever change the name, it will create a new grocery list. This field will also autosave.


5. Create Meal Sets  
- The final step is to create your meal sets.
    - You will need to provide a meal name, as well as any associated ingredient names. At this point in time, EZ Meal Sync cannot check for similar text occurances such as carrot and carrots or chicken & chicken breasts, so you will need to be vigilant about your naming conventions to eliminate repeat items with similar names. Names can always be modified if a mistake is made.
    - Before a meal list can be generated, you will need to ensure that you create enough meals so that the number of meals is a minimum of 3x the number of meals to be generated. A meal will not repeat for 3 consecutive generations. So if the number of meals to generate is 5, you will need to have 15+ meal options. There is a small amount of falseness to this rule though. If you generate 5 meals one week & then 10 meals the next week, this will cause an error if you only have 15 meal options.


6. Generate a Meal List  
The final step is to create a meal list. Click on the generate button & within a few seconds, the magic will happen. Items from your "Current Meals" will be removed & be replaced with the items from your "Upcoming Meals". A new list without repeats wlll be generated and added to "Upcoming Meals". The ingredients from these items will be pulled & cross referenced with your grocery departments. This list will then be added to your "Grocery List". 





## License
- GNU General Public License v3.0

## Contact
- Creator: Ezra Schier
- Contact: schier.ezra@gmail.com