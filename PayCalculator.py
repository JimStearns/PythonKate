__author__ = 'katestearns'
# PayCalculator.py: Calculate pay, including overtime
try:
    while True:
        # Define Globals
        pay = raw_input("How much do you get paid per hour?")
        if pay == "done":
            break
        float_pay = float(pay)
        hours = raw_input("How many hours did you work?")
        float_hours = float(hours)
        overtime_pay = float_pay * 1.5  ## A little clearer than adding a half
        ## "max_regular_hours" might be clearer. Overtime is under the max, yes?
        max_regular_hours = 40

        # Calculate pay and overtime pay
        if float_hours <= 40:
            ## Use parentheses with print - get ready for Python 3
            print("Your paycheck is", float_pay * float_hours, "Dollars.")
        elif float_hours > 40:
            print("Your paycheck is", (max_regular_hours * float_pay)
                  + ((float_hours - max_regular_hours) * overtime_pay), "Dollars.")
        else:
            ## Users do the strangest things :-)
            print("Negative hours?!?")

        print("Who's next?")

except:
    print("Enter a valid number.")
