import requests

from bs4 import BeautifulSoup as bS

# function to execute the translator


def main():
    myword = MultilingualOnlineTranslator()
    if myword.targetlanguage in myword.diclanguages:
        single_language_pair(myword)
    elif myword.targetlanguage == 0:
        all_lang_seq(myword)
    else:
        print("Wrong input")


def single_language_pair(myword):
    outfile = open(f"{myword.translatedword.lower()}.txt", "w", encoding="utf-8")
    myword.translatemessage()
    myword.generatelink()
    myword.getresponse()
    if myword.response.status_code == 200:
        print(str(myword.response.status_code) + " OK")
    else:
        print(str(myword.response.status_code) + " Some weird error")
    # before printing let's check if translations and examples are properly generated
    if myword.translations and myword.examples:
        print('Content examples:\n')
        print(f"{myword.diclanguages[myword.targetlanguage]} Translations:")
        print_translations(myword.translations, 5)
        print(f"\n{myword.diclanguages[myword.targetlanguage]} Example:")
        print_examples(myword.examples, 5)

        outfile.writelines(f"{myword.diclanguages[myword.targetlanguage]} Translations:\n")
        out_translations(outfile, myword.translations, 5)
        outfile.writelines(f"\n{myword.diclanguages[myword.targetlanguage]} Example:\n")
        out_examples(outfile, myword.examples, 5)
    else:
        print(f"Not able to parse {myword.translatepair} translations or/and examples from server using link {myword.translatelink}")
    outfile.close()


def all_lang_seq(myword):
    outfile = open(f"{myword.translatedword.lower()}.txt", "w", encoding="utf-8")
    for i in myword.diclanguages:
        if i != myword.source_language:
            myword.targetlanguage = i
            myword.translatemessage()
            myword.generatelink()
            myword.getresponse()
            if myword.response.status_code != 200:
                print(str(myword.response.status_code) + " Some weird error")
            if myword.translations and myword.examples:
                print(f"{myword.diclanguages[myword.targetlanguage]} Translations:")
                print_translations(myword.translations, 1)
                print(f"\n{myword.diclanguages[myword.targetlanguage]} Example:")
                print_examples(myword.examples, 1)

                outfile.writelines(f"{myword.diclanguages[myword.targetlanguage]} Translations:\n")
                out_translations(outfile, myword.translations, 1)
                outfile.writelines(f"\n{myword.diclanguages[myword.targetlanguage]} Example:\n")
                out_examples(outfile, myword.examples, 1)
    outfile.close()


# I have saved one of the translations to the htm page and use it instead of calling the server every time I troubleshoot


def test():
    myword = MultilingualOnlineTranslator()
    print(myword.translatepair)
    myword.generatelink()
    print(myword.translatelink)

# function to print first 5 items from the list


def print_translations(translations, num):
    for item in translations[:num]:
        print(item)

# function to print first 5 translation pairs from the list


def print_examples(examples, num):
    for i in range(0, num * 2, 2):
        print(examples[i])
        print(examples[i + 1])
        print()

# those 2 functions are outputing the translations and examples to the txt file


def out_translations(file, translations, num):
    for item in translations[:num]:
        file.writelines(item + '\n')


def out_examples(file, examples, num):
    for i in range(0, num * 2, 2):
        file.writelines(examples[i] + '\n')
        file.writelines(examples[i+1] + '\n' + '\n')
# class for storing all objects related to execution. I went to class as it is easier to read the code and add new features.


class MultilingualOnlineTranslator:
    allwords = []

    def __init__(self):
        self.source_language = int(input("""Hello, you're welcome to the translator. Translator supports: 
1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish
Type the number of your language:\n"""))
        self.targetlanguage = int(input("""Type the number of language you want to translate to or '0' to translate to all languages: \n"""))
        self.diclanguages = {1: "Arabic", 2: "German", 3: "English", 4: "Spanish", 5: "French", 6: "Hebrew", 7: "Japanese", 8: "Dutch", 9: "Polish", 10: "Portuguese", 11: "Romanian", 12: "Russian", 13: "Turkish"}
        self.translatedword = input("""Type the word you want to translate:\n""").lower()
        self.translatelink = ""
        self.response = ""
        self.bscontent = ""
        self.translatepair = ""
        self.translations = ""
        self.examples = ""
        MultilingualOnlineTranslator.allwords.append(self)


# this method generates translated pair. it should be invoked for every language in case if selected language is 0

    def translatemessage(self):

        # print(f'You chose "{self.source_language}" as the language to translate "{self.translatedword}" to.')

        self.translatepair = f"{self.diclanguages[self.source_language].lower()}-{self.diclanguages[self.targetlanguage].lower()}"

    def generatelink(self):
        # write a function to generate a proper link basing on init input
        self.translatelink = 'https://context.reverso.net/translation/' + self.translatepair + '/' + self.translatedword

    def getresponse(self):
        self.response = requests.get(self.translatelink, headers={'User-Agent': 'Mozilla/5.0'})
        soup = bS(self.response.text, 'html.parser')
        b = []
        # This piece looks for the first 2 translations:
        # This next piece looks for remaining translations in <a> tag:
        a = soup.find_all('a', class_='translation')
        for i in a:
            if i.text:
                word = i.text.replace("\n", "")
                word = word.lstrip()
                if word != 'Translation':
                    b.append(word)
        # And this piece searches for remaining translations in <div> tag:
        a = soup.find_all('div', class_='translation')
        for i in a:
            if i.text:
                word = i.text.replace("\n", "")
                word = word.lstrip()
                b.append(word)
        self.translations = b
        # This piece searches the all translations and examples:
        examp = soup.find_all("div", {"class": {"src ltr", "trg ltr"}})
        res = []
        for i in examp:
            a = i.text.strip()
            res.append(a)
        self.examples = res


if __name__ == "__main__":
    main()
