from unidecode import unidecode
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pyshadow.main import Shadow
import time


class Web:
    def __init__(self):
        ser = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=ser)
        self.shadow = Shadow(self.driver)

    def termo(self):
        self.driver.get('https://term.ooo/')
        # Random place to click and close the site instructions
        place = self.driver.find_element('xpath', '//*[@id="help"]/p[4]')
        place.click()

    def class_by_attribute(self, selector, i):
        return self.shadow.find_elements(selector)[i].get_attribute('class')

    def get_classes(self, word, i, word_len):  # Types the word in the term.ooo site and finds if its a valid word, if
        # not, erases the typed letters. At the end, returns the classes of the letters elements in the site

        for letter in word.lower():
            css = '#kbd_' + unidecode(letter)
            self.shadow.find_element(css).click()
        self.shadow.find_element('#kbd_enter').click()
        time.sleep(2)
        if self.class_by_attribute('div.letter:nth-child(2)', i) == 'letter empty':
            for j in range(word_len):
                self.shadow.find_element('#kbd_backspace').click()
        classes = []
        for j in range(word_len):
            classes.append(
                self.class_by_attribute(f'div.letter:nth-child({str(j + 2)})', i))

        return classes


def play_termo(game, max_attempts, word_len):  # Open Google Chrome Navigator, and starting by a word imputed by the
    # user, tries to guess the word of the day of term.ooo

    web = Web()
    web.termo()

    right_word = None
    attempt = 0
    first_letter_selector = 'div.letter:nth-child(2)'

    while attempt <= max_attempts - 1 and not right_word:
        while web.class_by_attribute(first_letter_selector, attempt) == 'letter empty' or \
                web.class_by_attribute(first_letter_selector, attempt) == 'letter empty edit' or \
                web.class_by_attribute(first_letter_selector, attempt) == 'letter edit empty':
            word = game.word_picker(word_len)
            classes = web.get_classes(word, attempt, word_len)

        right_word = game.classes_analyse(word, classes, word_len)
        if right_word:
            print('In', attempt + 1, 'attempts, the correct word is:', right_word.upper())
            input('Press Enter to close the web browser...')
            web.driver.quit()
            exit()

        attempt += 1

    print('The word was not guessed :(')
