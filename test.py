
def currency_converter():
    currency_type = (input("Which currency would you like to convert (enter 3-letter code)?"))
    exchange_rate = float(input("What is the value of one Euro in this currency?"))
    print ("Please enter the amount of", currency_type, "to be converted")
    amount = float(input(""))
    print("{0:0.2f} {1} is equal to {2:0.2f} EUR".format(amount, currency_type, amount/exchange_rate))

#Whether to continue conversion rate is implemented in the main function.  A while loop keeps asking user if they
#want to continue, and assumes the user will enter the correct values
def main():
    want_continue = 1
    print("Program to convert money in different currecies to Euro.")
    while (want_continue == 1):
        currency_converter()

        want_continue = int(input("Do you want to continue (1 = yes / 0 = no)?"))



main()
