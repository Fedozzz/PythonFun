# Write your code here
import random

engletters = set('qwertyuioplkjhgfdsazxcvbnm')


print("H A N G M A N")
while True:
    menu = input('Type "play" to play the game, "exit" to quit:')
    if menu == "play":
        words = 'python', 'java', 'kotlin', 'javascript'
        answer = random.choice(words)
        not_guessed_letters = set(answer)
        wrong_attempt_letter = set()
        displayed_answer = "-" * len(answer)
        attempted_answer = []
        miss = 0

        while miss < 8:
            print()
            print(displayed_answer)
            char = input("Input a letter:")
            if len(char) > 1:
                print("You should input a single letter")
                continue
            elif char not in engletters:
                print('Please enter a lowercase English letter')
                continue
            if char in answer:
                not_guessed_letters.discard(char)
                if char in displayed_answer:
                    # miss += 1
                    print("You've already guessed this letter")
                displayed_answer = answer
                for c in not_guessed_letters:
                    displayed_answer = displayed_answer.replace(c, "-")
                if "-" not in displayed_answer:
                    print(displayed_answer)
                    print("You guessed the word!")
                    print("You survived!")
                    print()
                    break
            else:

                if char in wrong_attempt_letter:
                    print("You've already guessed this letter")
                else:
                    print("That letter doesn't appear in the word")
                    miss += 1
                    wrong_attempt_letter.add(char)


        else:
            print("You lost!")
            print()
    elif menu == "exit":
        break
