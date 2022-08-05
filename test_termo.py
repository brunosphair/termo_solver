from termo_solver import Solver

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


def test_termo(game, target_word):

    right_word = None
    attempt = 0

    while not right_word:
        word = game.word_picker(len(target_word))
        classes = get_classes_offline(word, target_word, len(target_word))

        right_word = game.classes_analyse(word, classes, len(target_word))
        if right_word:
            print('In', attempt + 1, 'attempts, the correct word is:', right_word.upper())

        attempt += 1

    return attempt


if __name__ == '__main__':
    words = ['CARTA', 'TESTE']
    for w in words:
        game = Solver()
        target_word = w
        attempt = test_termo(game, target_word)