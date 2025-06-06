import random, sys, math, time

def generate_new_meals(all_meals, current_meals, upcoming_meals, meal_qty):
    """Generates a new meal set while checking that it recently hasn't been selected."""
    meal_qty = int(meal_qty)
    old_meals = current_meals + upcoming_meals

    # If the number of meals generated x3 is greater than the number of meals in the dict., then alert the user and exit.
    if len(all_meals) < meal_qty * 3:
        print(f"You have {meal_qty} new meals selected and only {len(all_meals)} meals created.")
        needed_meal_qty = math.floor(len(all_meals) / 3)
        needed_new_meals = (meal_qty * 3) - len(all_meals)
        print("The number of meals created needs to be the number of meal selections x3.")
        print(f"\033[31mChange your meal quantity to {needed_meal_qty} or create {needed_new_meals} new meals.\033[0m")
        print("Exiting...")
        time.sleep(3)
        sys.exit()

    # If the number of meals in the Current and Upcoming Meals lists + number of meals generated exceeds the number of meals in the dict., then alert the user and exit.
    if len(old_meals) + meal_qty > len(all_meals):
        too_many_old = (len(old_meals) + meal_qty) - (len(all_meals))
        update_qty = len(all_meals)-len(old_meals)
        print("There are too many meals within the Current Meals and Upcoming Meals list in order to generate a new list without repeats.")
        print(f"\033[31mPlease manually remove {too_many_old} meals from the Current or Upcoming Meals Lists or change your meal generation quantity to {update_qty}.\033[0m]")
        print("Exiting...")
        time.sleep(3)
        sys.exit()

    else:
        print(f"You have {meal_qty} meal selections chosen and {len(all_meals)} meals created.")

    new_meal_list = set()
    # Generate a random list of meals and verify they have not been used recently.
    while len(new_meal_list) != meal_qty:
        new_meal = random.choice(all_meals)
        if new_meal not in old_meals:
            new_meal_list.add(new_meal)
    print(f"The following meals have been generated: {new_meal_list}")

    return new_meal_list

def generate_grocery_list(all_meals, grocery_depts, new_meal_list):
    pass
    # For every meal in the new meal list, pull the ingredients from meals.json
    # Compare the items 
