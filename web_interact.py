from unidecode import unidecode
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pyshadow.main import Shadow
import time


def get_classes(word, i, shadow):  # Types the word in the term.ooo site and finds if its a valid word, if not, deletes
    # it from the pertinents lists

    for letter in word.lower():
        css = '#kbd_' + unidecode(letter)
        shadow.find_element(css).click()
    shadow.find_element('#kbd_enter').click()
    time.sleep(2)
    if shadow.find_elements('div.letter:nth-child(2)')[i].get_attribute('class') == 'letter empty':
        for j in range(5):
            shadow.find_element('#kbd_backspace').click()
    classes = []
    for j in range(5):
        classes.append(
            shadow.find_elements('div.letter:nth-child(' + str(j + 2) + ')')[i].get_attribute('class'))

    return classes


def web_termo(game):  # Open Google Chrome Navigator, and starting by a word imputed by the user, tries to guess the
    # word of the day of term.ooo

    ser = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=ser)
    driver.get('https://term.ooo/')
    place = driver.find_element('xpath', '//*[@id="help"]/p[4]')
    shadow = Shadow(driver)
    place.click()
    i = 0
    right_word = None

    while i <= 5 and not right_word:
        while shadow.find_elements('div.letter:nth-child(2)')[i].get_attribute('class') == 'letter empty' or \
                shadow.find_elements('div.letter:nth-child(2)')[i].get_attribute('class') == 'letter empty edit' or \
                shadow.find_elements('div.letter:nth-child(2)')[i].get_attribute('class') == 'letter edit empty':
            word = game.word_picker()
            classes = get_classes(word, i, shadow)


        right_word = game.classes_analyse(word, classes)
        if right_word:
            print('A palavra correta é:', right_word.upper())
            input('Pressione Enter para fechar o navegador...')
            driver.quit()
            exit()

        i += 1

    print('The word was not guessed :(')


#game = Solver()
#web_termo(game)
