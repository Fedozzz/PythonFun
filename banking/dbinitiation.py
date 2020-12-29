# this is just a file which i used to play around with SQLite database during writing of the project.

import sqlite3

# This function allows to validate any input number by luhn algorythm.

def luhnalgocheck(account):
    sum_num = 0
    counter = 0
    dig = 0
    cardnumtoprocess = list(str(account))
    print("input card number ", cardnumtoprocess)
    print(len(cardnumtoprocess))
    check_sum_control = cardnumtoprocess.pop(-1)
    print(len(cardnumtoprocess))
    print(check_sum_control)
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
    print(check_sum_dig)

    return int(check_sum_dig) == int(check_sum_control)



conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
query = """CREATE TABLE card ( 
 id INT, 
 number VARCHAR(30), 
 pin VARCHAR(30), 
 balance INT DEFAULT 0
);
"""


deleteallentries = """
DELETE FROM Card
"""

allentriesquery = """
SELECT number FROM card 
"""

# cur.execute(query)
# cur.execute(query2)
# cur.execute(deleteallentries)
# entries = cur.execute(allentriesquery).fetchall()
entries = cur.execute(allentriesquery).fetchall()
allnumbers = []
for item in entries:
    allnumbers.append(item[0])

# print(allnumbers)
#print(input() in allnumbers)
print(luhnalgocheck("4000003972196501"))
#conn.commit()
#for item in entries:
#    print(item)
