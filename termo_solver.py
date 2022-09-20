from unidecode import unidecode


class Solver:
    def __init__(self):
        self.possible_words = load_txt()
        self.all_possible_words = self.possible_words.copy()
        self.right_letters = set()

    def delete_letter(self, letter: str):
        '''
        Removes from possible words the words that contain the specified letter
        '''
        for word in list(self.possible_words):
            if letter in word:
                self.possible_words.remove(word)

    def include_letter_pos(self, letter: str, letter_position: int):
        '''
        Removes from possible words the words that not contain the specified
        letter in the specified position.
        '''
        for word in list(self.possible_words):
            if word[letter_position - 1] != letter:
                self.possible_words.remove(word)

    def include_letter(self, letter: str, letter_not_position: int):
        '''
        Removes from possible words the words that not contains the specified
        letter and, after, removes the words that contains the specified letter
        but in the wrong position.
        '''
        for word in list(self.possible_words):
            if letter not in word:
                self.possible_words.remove(word)
            if word[letter_not_position - 1] == letter:
                self.possible_words.remove(word)

    def number_of_letter(self, letter, occurrences):
        '''
        Removes from possible words the words that not contains the right
        number of occurrences of the specified letter.
        '''
        for word in list(self.possible_words):
            if word.count(letter) != occurrences:
                self.possible_words.remove(word)

    def word_picker(self, word_len):
        '''
        Returns the word to be tested. The criteria is: the word that has most
        of the more common letters of the possible words, except the right
        letters. It is not necessary a possible word.
        '''

        # TODO: implement a solution to words with repeated letters

        letter_list = dict()
        the_word = self.possible_words[0]
        if len(self.possible_words) == 1:
            return the_word
        else:
            for word in self.possible_words:
                for letter in word:
                    if letter not in letter_list:
                        letter_list[letter] = 0
                    letter_list[letter] += 1

            for letter in self.right_letters:
                if letter in letter_list:
                    del letter_list[letter]

            sorted_letters = sorted(letter_list, key=letter_list.get)

            biggest_count = 0
            if len(sorted_letters) < word_len + 1:
                final = len(sorted_letters)
            else:
                final = word_len + 1
            for word in self.all_possible_words:
                count = 0
                for y in range(1, final):
                    if sorted_letters[(-1) * y] in word:
                        count += 1
                    if word[y - 1] in self.right_letters:
                        count -= 1
                if count > biggest_count:
                    the_word = word
                    biggest_count = count

            return the_word

    def classes_analysis(
                        self,
                        word: str,
                        classes: list,
                        word_len: int,
                        print_status=True,
                        print_possible_words=False
                        ):
        '''
        Receives the tried word and a list ('classes') that contains, in order,
        the class of each letter of the tried word ('letter wrong', 'letter
        place', 'letter right' or 'letter empty'). Based on this, the function
        returns a list overwriting 'letter wrong' classes of letters that
        appear more than once in the word with -1. Than, based on classes,
        removes the words that are no longer possible to be the word of the
        day. At the end, returns None if the word was not guesses or the
        guessed word.
        '''

        right_word = None

        if classes[0] == 'letter empty':
            print('Word', word.upper(), 'invalid')
            if word in self.possible_words:
                self.possible_words.remove(word)
            self.all_possible_words.remove(word)

            return right_word

        for letter in set(word):
            if word.count(letter) > 1:
                all_letter_results = []
                letter_positions = []
                for j in range(word_len):
                    if word[j] == letter:
                        all_letter_results.append(classes[j])
                        letter_positions.append(j)
                count_right = all_letter_results.count('letter place')
                + all_letter_results.count('letter right')
                count_wrong = all_letter_results.count('letter wrong')
                if count_right > 0:
                    for j in range(len(all_letter_results)):
                        if all_letter_results[j] == 'letter wrong':
                            classes[letter_positions[j]] = -1
                    if count_wrong >= 1:
                        self.number_of_letter(letter, count_right)
                else:
                    self.delete_letter(letter)

        for n in range(word_len):
            result = classes[n]
            if result != -1:
                if result == 'letter wrong':
                    self.delete_letter(word[n])
                elif result == 'letter place':
                    self.include_letter(word[n], n + 1)
                    self.right_letters.add(word[n])
                elif result == 'letter right':
                    self.include_letter_pos(word[n], n + 1)
                    self.right_letters.add(word[n])
                elif result == 'letter right done':
                    right_word = word

        if print_status:
            print('Possible Words: ', len(self.possible_words))
        if print_possible_words:
            print(self.possible_words)

        return right_word


def load_txt():
    '''
    Loads the words.txt, based on lexico pt-br and put the words in a list.
    The file contains only words with 5 letter, and each one is a valid word in
    term.ooo, tested one by one.
    '''
    words = []
    with open('words.txt', encoding='utf8') as f:
        for item in f:
            words.append(unidecode(item.rstrip().upper()))

    return words
