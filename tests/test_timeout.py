import pyinputplus as pyip

try:
    user_input = pyip.inputStr(
        prompt="Enter something: ",
        timeout=10,  # Waits for 10 seconds
        limit=1      # Limits to one attempt before exiting
    )
    print(f"You entered: {user_input}")
except pyip.TimeoutException:
    print("No input received within 10 seconds. Program terminated.")
except pyip.RetryLimitException:
    print("Retry limit reached. Program terminated.")
