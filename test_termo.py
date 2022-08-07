from termo_solver import Solver
from termo_solver import load_txt
import datetime


def get_classes_offline(word, right_word, word_len):
    all_results = []

    for letter_position in range(word_len):
        if word == right_word:
            all_results = ['letter right done', 'letter right done', 'letter right done', 'letter right done',
                           'letter right done']
            return all_results

        elif word[letter_position] == right_word[letter_position]:
            all_results.append('letter right')

        elif word[letter_position] in right_word:
            if word.count(word[letter_position]) > 1:
                indices = []
                occurrences = right_word.count(word[letter_position])
                for i in range(word_len):
                    if word[i] == word[letter_position] and i != letter_position:
                        indices.append(i)
                for i in indices:
                    if i < letter_position:
                        if all_results[i] == 'letter right' or all_results == 'letter place':
                            occurrences -= 1
                        else:
                            if word[i] == right_word[i]:
                                occurrences -= 1
                if occurrences > 0:
                    all_results.append('letter place')
                else:
                    all_results.append('letter wrong')
            else:
                all_results.append('letter place')
        else:
            all_results.append('letter wrong')

    return all_results


def test_termo(game, target_word, print_words=False, print_possible_words=False):
    right_word = None
    attempt = 0
    print_status = False

    while not right_word:
        word = game.word_picker(len(target_word))
        if print_words:
            print(word)
        classes = get_classes_offline(word, target_word, len(target_word))

        right_word = game.classes_analyse(word, classes, len(target_word), print_status, print_possible_words)
        if right_word:
            print('In', attempt + 1, 'attempts, the correct word is:', right_word.upper())

        attempt += 1

    return attempt


def play_test(definition=None):
    if not definition:
        all_words = True
    else:
        all_words = False
        if isinstance(definition, int):
            is_integer = True
            number_of_words = definition
        else:
            is_integer = False
    words = load_txt()
    if all_words:
        n_attempts = []
        for w in words:
            game = Solver()
            target_word = w
            n_attempts.append(test_termo(game, target_word))
    elif is_integer:
        n_attempts = []
        for i in range(number_of_words):
            game = Solver()
            n_attempts.append(test_termo(game, words[i]))
    else:
        game = Solver()
        int_n_attempts = test_termo(game, definition, True, True)
        return int_n_attempts


    return n_attempts


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    n_attempts = play_test()
    if isinstance(n_attempts, int):
        print(f'Word guessed in {n_attempts} attempts')
    else:
        media = sum(n_attempts) / len(n_attempts)
        max = max(n_attempts, key=int)
        print(f'Max = {max} and Media = {media}')
        words_not_guessed = sum(1 if n > 6 else 0 for n in n_attempts)
        percent_not_guessed = words_not_guessed / len(n_attempts)
        print(f'The method not guessed {percent_not_guessed * 100}% of the words')

    end_time = datetime.datetime.now()
    print('Elapsed time:', end_time - start_time)