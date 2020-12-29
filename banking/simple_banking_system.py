# Write your code here
import random
import sqlite3

def luhnalgocheck(account):
    sum_num = 0
    counter = 0
    cardnumtoprocess = list(str(account))
    check_sum_control = cardnumtoprocess.pop(-1)
    for i in cardnumtoprocess:
        if counter % 2 == 1:
            dig = int(i)
        else:
            if int(i) * 2 < 9:
                dig = int(i) * 2
            else:
                dig = int(i) * 2 - 9

            # print("Counter dig and i", counter, dig, i)
        sum_num += dig
        counter += 1

    if sum_num % 10 == 0:
        check_sum_dig = 0
    else:
        check_sum_dig = 10 - (sum_num % 10)

    return int(check_sum_dig) == int(check_sum_control)
    # print("Debugging resulting sum", sum_num)
    # print("Debugging input_card_num", input_card_num)
    # print("Debugging check_sum_dig", check_sum_dig)
    # result_card_num = input_card_num + str(check_sum_dig)

def checkcardexistance(account):
    allcardnumbersquery = """
                        SELECT id, number, pin, balance FROM card
                    """
    allcards = cur.execute(allcardnumbersquery).fetchall()
    allcardslist =[]
    for item in allcards:
        allcardslist.append(item[1])
    return account in allcardslist

def check_pin(number, pin):
    checksum = 0
    allentriesquery = """
                        SELECT id, number, pin, balance FROM card
                    """
    allcards = cur.execute(allentriesquery).fetchall()
    for item in allcards:
        # print("Checking card Number", item.number, "vs input with number", number, "and pin", pin, "vs", item.pin)
        if str(number) == str(item[1]) and str(pin) == str(item[2]):
            print("You have successfully logged in!")
            checksum = 1
            mycardobj = Card(number=item[1],pin=item[2],balance=item[3])
            mycardobj.myaccount()

    # If previous cycle didn't find any card with the pin and number from query the checksum will remain 0
    if checksum == 0:
        print("Wrong card number or PIN!")

def insert_card(number, pin):
    query = """
    INSERT INTO card (number, pin) 
    VALUES 
    ('{}', '{}');
    """.format(number, pin)
    cur.execute(query)
    conn.commit()

class Card:
    all_cards = []

    def __init__(self, number, pin, balance):
        self.number = number
        self.pin = pin
        self.balance = balance
        # Card.all_cards.append(self)
    def luhn_alg(self):
        # Generate random 15 digit number for the card
        input_card_num = "40000" + "%0.10d" % random.randrange(000000000, 999999999)
        card_num_processed = list(input_card_num)
        sum_num = 0
        # calculate the sum of all digits in the card number multiplying all odd indexes:
        counter = 0
        dig = 0
        for i in card_num_processed:
            if counter % 2 == 1:
                dig = int(i)
            else:
                if int(i) * 2 < 9:
                    dig = int(i) * 2
                else:
                    dig = int(i) * 2 - 9

            # print("Counter dig and i", counter, dig, i)
            sum_num += dig
            counter += 1

        if sum_num % 10 == 0:
            check_sum_dig = 0
        else:
            check_sum_dig = 10 - (sum_num % 10)
        # print("Debugging resulting sum", sum_num)
        # print("Debugging input_card_num", input_card_num)
        # print("Debugging check_sum_dig", check_sum_dig)
        result_card_num = input_card_num + str(check_sum_dig)
        return result_card_num

    def get_card_number(self):
        # invoke Luhn algorithm
        self.number = self.luhn_alg()

    def get_pin(self):
        self.pin = "%0.4d" % random.randrange(0000, 9999)

    def update_balance(self):
        updatebalancequery = """
        UPDATE card
        SET balance = '{}'
        WHERE number = '{}';
        """.format(self.balance, self.number, self.pin)
        cur.execute(updatebalancequery)
        conn.commit()
        print("Income was added!")

    def get_balance(self,account):
        getbalancequery = """
        SELECT balance FROM card
        WHERE number = '{}';
        """.format(account)
        return cur.execute(getbalancequery).fetchone()[0]

    def removeaccount(self):
        removeaccountquery = """
        DELETE FROM card
        WHERE number = '{}';
        """.format(self.number)
        cur.execute(removeaccountquery)
        conn.commit()

    def do_transfer(self, account, amount):
        updatebalancequery = """
        UPDATE card
        SET balance = '{}'
        WHERE number = '{}';
        """.format(amount, account)
        cur.execute(updatebalancequery)
        conn.commit()
        print("Success!")
        

    def myaccount(self):
        while True:
            print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
            """)
            n = int(input())
            if n == 1:
                print("Balance:", self.balance)
            elif n == 2:
                print("Enter income:")
                income = int(input())
                self.balance += income
                self.update_balance()

            elif n == 3:
                print("Enter card number:")
                account = int(input())
                if account == self.number:
                    print("You can't transfer money to the same account!")
                elif not luhnalgocheck(account):
                    print("Probably you made a mistake in the card number. Please try again!")
                elif not checkcardexistance(str(account)):
                    print("Such a card does not exist.")

                else:
                    print("Enter how much money you want to transfer")
                    amount = int(input())
                    # add the calculation of resulting balance for the target card here
                    # (sql query to return the current balance and add an amount from the value above
                    # add the validation
                    if self.balance - amount >= 0:
                        self.balance -= amount
                        targetamount = int(self.get_balance(account)) + amount
                        self.update_balance()
                        self.do_transfer(account, targetamount)
                    else:
                        print("Not enough money!")





            elif n == 4:
                print("Closing account")
                self.removeaccount()
                print("The account has been closed!")
                break
            elif n == 5:
                break
            elif n == 0:
                exit()

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
# cur.execute(query)
query = """CREATE TABLE card ( 
 id INTEGER PRIMARY KEY, 
 number TEXT, 
 pin TEXT, 
 balance INTEGER DEFAULT 0
);
"""
# cur.execute(query)

# Print menu and start a cycle to run through the menu
while True:
    print("""
1. Create an account
2. Log into account
0. Exit
    """)
    n = int(input())
    if n == 1:
        mycard = Card(0,0,0)
        print("Your card has been created")
        mycard.get_card_number()
        lastnum = mycard.number
        print("Your card number:")
        print(mycard.number)
        mycard.get_pin()
        print("Your card PIN")
        print(mycard.pin)
        insert_card(mycard.number, str(mycard.pin))



    elif n == 2:
        print("Enter your card number:")
        mycardnumber = str(input())
        print("Enter your PIN:")
        mypin = str(input())
        check_pin(mycardnumber, mypin)
    elif n == 0:
        break
    else:
        continue



# print(checkcardexistance('4000006735337270'))

allentriesquery = """
                    SELECT id, number, pin FROM card 
                """
#allcards = cur.execute(allentriesquery).fetchall()
#for card in allcards:
#    print(card)



