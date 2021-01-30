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
    print(f"{myword.targetlanguage} Translations:")
    print_translations(myword.translations)
    print(f"\n{myword.targetlanguage} Examples:")
    print_examples(myword.examples)

# I have saved one of the translations to the htm page and use it instead of calling the server every time I troubleshoot


def test():
    f = open('test.htm', 'r', encoding='utf-8')
    soup = bS(f.read(), 'html.parser')
    f.close()
    b = []
    a = soup.find_all('a', class_='translation')
    for i in a:
        if i.text:
            word = i.text.replace("\n", "")
            word = word.lstrip()
            # for some weird reason word "translation" also has translate class, had to create an exception for it
            if word != 'Translation':
                b.append(word)


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
        self.source_language = input('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:\n')
        self.translatedword = input('Type the word you want to translate:\n')
        self.translatelink = ""
        self.response = ""
        self.bscontent = ""
        self.translatepair = ""
        self.targetlanguage = ""
        self.translations = ""
        self.examples = ""
        MultilingualOnlineTranslator.allwords.append(self)

    def translatemessage(self):
        print(f'You chose "{self.source_language}" as the language to translate "{self.translatedword}" to.')
        if self.source_language == 'en':
            self.translatepair = 'french-english'
            self.targetlanguage = 'English'
        elif self.source_language == 'fr':
            self.translatepair = 'english-french'
            self.targetlanguage = 'French'

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
