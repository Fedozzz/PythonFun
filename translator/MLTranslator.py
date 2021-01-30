import requests

from bs4 import BeautifulSoup as bS

# function to execute the translator

def main():
    myword = MultilingualOnlineTranslator()
    myword.translatemessage()
    myword.generatelink()
    myword.getresponse()
    if myword.response.status_code == 200:
        print(str(myword.response.status_code) + " OK")
    else:
        print(str(myword.response.status_code) + "Some weird error")
    print('Content examples:\n')
    print(f"{myword.diclanguages[myword.targetlanguage]} Translations:")
    print_translations(myword.translations)
    print(f"\n{myword.diclanguages[myword.targetlanguage]} Examples:")
    print_examples(myword.examples)

# I have saved one of the translations to the htm page and use it instead of calling the server every time I troubleshoot


def test():
    myword = MultilingualOnlineTranslator()
    print(myword.translatepair)
    myword.generatelink()
    print(myword.translatelink)



# function to print first 5 items from the list


def print_translations(translations):
    for item in translations[:5]:
        print(item)

# function to print first 5 translation pairs from the list


def print_examples(examples):
    for i in range(0, 10, 2):
        print(examples[i])
        print(examples[i + 1])
        print()

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
        self.targetlanguage = int(input("""Type the number of language you want to translate to: \n"""))
        self.diclanguages = {1:"Arabic", 2:"German", 3:"English", 4:"Spanish", 5:"French", 6:"Hebrew", 7:"Japanese", 8:"Dutch", 9:"Polish", 10:"Portuguese", 11:"Romanian", 12:"Russian", 13:"Turkish"}
        self.translatedword = input("""Type the word you want to translate:\n""").lower()
        self.translatelink = ""
        self.response = ""
        self.bscontent = ""
        self.translatepair = ""
        self.translations = ""
        self.examples = ""
        MultilingualOnlineTranslator.allwords.append(self)

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
