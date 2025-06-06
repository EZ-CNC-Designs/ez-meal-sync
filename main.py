import time, sys, threading, os
from dotenv import load_dotenv
from pathlib import Path
import pyinputplus as pyip

from ui.ui_run import UserInterface
from gkeep.gkeep_run import run_meal_planning

class MainProgram:
    def __init__(self):
        self.terminate = True
        load_dotenv()
        self.username = os.getenv("GKEEP_USER")
        
        
    def main(self):
        """Main program."""
        # Add a user name if not yet done so
        if not self.username:   
            verify = False
            while verify == False:
                name_input = pyip.inputStr(prompt="\nPlease enter your name.\n\n")
                name_input = name_input.title()
                verify = pyip.inputYesNo(f"\nYou entered {name_input}, is this correct? (yes/no)\n\n")
                if verify == "yes":
                    with open(".env", "a") as file:
                        file.write(f"\nGKEEP_USER={name_input}")
                    self.username = name_input
                    verify = True
                if verify == "no":
                    continue
    
        while self.terminate == True:
            run_countdown = threading.Thread(target=self.countdown, args=[60]) # Args are seconds
            run_countdown.start()
            print(f"\nHi, {self.username}")     
            time.sleep(1)
            # Wait for user input and prompt for a choice
            user_choices = ["UI", "Run", "Exit", "Quit"]
            user_selection = pyip.inputChoice(
                choices=user_choices,
                prompt='''\nWelcome to EZ Meal Sync!\n
    Enter "UI" to access the user interface, "Run" to execute the EZ Meal Sync Program, or "Exit" to terminate the program.
    EZ Meal Sync will auto-run in 60 seconds if a selection is not made.\n\n''')
        
            if user_selection == "UI":
                # Access the UI if the user selects "UI"
                self.terminate = False
                ui_interface = UserInterface(self.username)
                ui_interface.main_menu()
                self.terminate = True
                
            elif user_selection == "Run":
                # Run the meal sync program
                self.terminate = False
                self.run_meal_sync()
                print("\nExiting...")
                time.sleep(1)
                                
            elif user_selection == "Exit" or user_selection == "Quit":
                # Terminate the program
                self.terminate = False
                print("\nExiting...")
                time.sleep(1)
                os._exit(0)
    

    def run_meal_sync(self):
        # Run the meal planning program.
        reboot = 3
        try:
            print("Running EZ Meal Sync Program...")
            run_meal_planning()
            sys.exit()
            
        except ConnectionError:
            # If a connection error occurs, attempt a reboot 3 times before terminating the program
            while reboot != 0:
                print(f"Connection Error; attempting reboot. {reboot} tries left before system exit.")
                reboot -= 1
                if reboot == 0:
                    print("Failed to connect to the internet, exiting now...")
                    time.sleep(3)
                    sys.exit()
                else:
                    # Pause for a break to see if the internet connection will be restored
                    print(f"Taking a 5 minute nap before trying again.")
                    time.sleep(5*60)
                    continue

    
    def countdown(self, time_to_run):
        # Begin the countdown and prompt the user to make a selection or the program will run automatically
        time.sleep(time_to_run)
        if self.terminate == True:
            self.run_meal_sync()
        else:
            sys.exit()

        
if __name__ == "__main__":
    # Create an instance of the program
    run = MainProgram()
    run.main()
    