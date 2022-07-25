from unidecode import unidecode
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from pyshadow.main import Shadow
import random


def load_txt():  # Loads the txt from lexico pt-br and put the words with 5 letters in a list
    words = []
    with open('palavras.txt', encoding='utf8') as f:
        for item in f:
            if len(item.rstrip()) == 5:
                words.append(item.rstrip().upper())

    return words


def delete_letter(letter):  # Removes from possible words the words that contain the specified letter
    for word in list(possible_words):
        if letter in unidecode(word):
            possible_words.remove(word)


def include_letter_pos(letter, letter_position):  # Removes from possible words the words that not contain the
    # specified letter in the specified position
    for word in list(possible_words):
        if unidecode(word[letter_position - 1]) != unidecode(letter):
            possible_words.remove(word)


def include_letter(letter, letter_not_position):  # Removes from possible words the words that not contains the
    # specified letter and, after removes the words that contains the specified letter but in the wrong position
    for word in list(possible_words):
        if letter not in unidecode(word):
            possible_words.remove(word)
        if unidecode(word[letter_not_position - 1]) == letter:
            possible_words.remove(word)


def number_of_letter(letter, occurrences):  # Removes from possible words the words that not contains the right
    # number of occurrences of the specified letter
    for word in list(possible_words):
        if unidecode(word).count(letter) != occurrences:
            possible_words.remove(word)


def all_results_analise(word, all_results):  # Receives the tried word and a list ('all_results') that contains,
    # in order, the class of each letter of the tried word ('letter wrong', 'letter place' or 'letter right'). Based
    # on this, the function returns a list overwriting 'letter wrong' and 'letter place' classes of letters that
    # appear more than once in the word with -1.
    for letter in set(unidecode(word)):
        if unidecode(word).count(letter) > 1:
            all_letter_results = []
            letter_positions = []
            for j in range(5):
                if unidecode(word[j]) == letter:
                    all_letter_results.append(all_results[j])
                    letter_positions.append(j)
            count_right = all_letter_results.count('letter place') + all_letter_results.count('letter right')
            count_wrong = all_letter_results.count('letter wrong')
            if count_right > 0:
                for j in range(len(all_letter_results)):
                    if all_letter_results[j] == 'letter wrong':
                        all_results[letter_positions[j]] = -1
                if count_wrong >= 1:
                    number_of_letter(letter, count_right)
            else:
                delete_letter(letter)
    return all_results


def web_termo():  # Open Google Chrome Navigator, and starting by a word imputed by the user, tries to guess the word
    # of the day of term.ooo
    global possible_words

    possible_words = load_txt()
    ser = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=ser)
    driver.get('https://term.ooo/')
    place = driver.find_element('xpath', '//*[@id="help"]/p[4]')
    shadow = Shadow(driver)
    place.click()
    k = -1

    for i in range(6):
        while shadow.find_elements('div.letter:nth-child(2)')[i].get_attribute('class') == 'letter empty' or \
                shadow.find_elements('div.letter:nth-child(2)')[i].get_attribute('class') == 'letter empty edit' or \
                shadow.find_elements('div.letter:nth-child(2)')[i].get_attribute('class') == 'letter edit empty':
            k += 1
            if i == 0:
                word = input('Qual palavra tentar?').upper()
            else:
                word = random.choice(possible_words)
            for letter in word.lower():
                css = '#kbd_' + unidecode(letter)
                shadow.find_element(css).click()
            shadow.find_element('#kbd_enter').click()
            time.sleep(2)
            if shadow.find_elements('div.letter:nth-child(2)')[i].get_attribute('class') == 'letter empty':
                print('Palavra inválida')
                for j in range(5):
                    shadow.find_element('#kbd_backspace').click()

        all_results = []
        for j in range(5):
            all_results.append(
                shadow.find_elements('div.letter:nth-child(' + str(j + 2) + ')')[i].get_attribute('class'))

        all_results = all_results_analise(word, all_results)

        for n in range(5):
            result = all_results[n]
            if result != -1:
                if result == 'letter wrong':
                    delete_letter(unidecode(word[n]))
                elif result == 'letter place':
                    include_letter(unidecode(word[n]), n + 1)
                elif result == 'letter right':
                    include_letter_pos(unidecode(word[n]), n + 1)
                elif result == 'letter right done':
                    print('A palavra correta é:', word.upper())
                    input('Pressione Enter para fechar o navegador...')
                    driver.quit()
                    exit()
        print('Palavras possíveis: ', len(possible_words))
        x = input('Imprimir palavras possíveis? (s/N) ').upper()
        if x == 'S':
            print(possible_words)
        k = -1
