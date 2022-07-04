"""This file contains world anaysis tools."""
import argparse
import logging
from convergeutils.utils import add_logging_parser, setup_logging_from_args
from wordle_bot.words import WORDS, GUESSES
from wordle_bot.guess import Guesser

logger = logging.getLogger(__name__)

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def word_scores(words):
    index_counts = [[0 for _ in range(5)] for _letter in LETTERS]
    counts = [0 for _ in LETTERS]
    scores = []

    for word in words:
        temp = ""
        for i, letter in enumerate(word):
            if letter in word and letter not in temp:
                counts[LETTERS.index(letter)] += 1
                temp += letter
            index_counts[LETTERS.index(letter)][i] += 1

    for word in words:
        score = 0
        for i, letter in enumerate(word):
            score += index_counts[LETTERS.index(letter)][i]
        score += counts[LETTERS.index(letter)] / 5
        scores.append(score)

    return scores


def letter_counts():
    parser = argparse.ArgumentParser("Convergle letter count analysis CLI.")
    add_logging_parser(parser)
    args = parser.parse_args()

    setup_logging_from_args(args)
    counts = [0 for _ in LETTERS]
    index_counts = [[0 for _ in range(5)] for _letter in LETTERS]

    for word in WORDS:
        temp = ""
        for i, letter in enumerate(word):
            if letter in word and letter not in temp:
                counts[LETTERS.index(letter)] += 1
                temp += letter
            index_counts[LETTERS.index(letter)][i] += 1

    for i, letter in enumerate(LETTERS):
        logger.info(
            f"{letter}: 0: {index_counts[i][0]}\t"
            f"1: {index_counts[i][1]}\t2: {index_counts[i][2]}\t"
            f"3: {index_counts[i][3]}\t4: {index_counts[i][4]} "
        )

    best_score = 0
    best_word = "None"
    for word in WORDS:
        score = 0
        for i, letter in enumerate(word):
            score += index_counts[LETTERS.index(letter)][i]
        if score > best_score:
            best_score = score
            best_word = word
        logger.info(f"{word}: {score}")

    logger.info(f"Best Word: {best_word} -> {best_score}")


def valid_words(guesses, results, words=WORDS):
    valid_words = []
    for word in words:
        for guess, result in zip(guesses, results):
            guesser = Guesser(word)
            if guesser.guess(guess) != result:
                break
        else:
            valid_words.append(word)

    return valid_words


def valid_words_v2():
    parser = argparse.ArgumentParser("Convergle Valid Word V2 CLI tool")
    add_logging_parser(parser)
    parser.add_argument(
        "--guesses", nargs="+", type=str, help="List of guesses"
    )
    parser.add_argument(
        "--results", nargs="+", type=str, help="List of guess results"
    )
    args = parser.parse_args()
    setup_logging_from_args(args)

    assert len(args.guesses) == len(args.results), "Array Sizes not Matched."
    for guess, result in zip(args.guesses, args.results):
        assert guess in GUESSES, "INVALID GUESS"
        assert len(result) == 5, "RESULT SIZE ERROR"
        for element in result:
            assert element in "012", "INVALID RESULT CHARACTER"

    words = valid_words(args.guesses, args.results)
    for word in words:
        logger.info(word)
    logger.info(f"Total valid words {len(words)}")


def get_valid_words():
    parser = argparse.ArgumentParser("Convergle letter count analysis CLI.")
    add_logging_parser(parser)
    parser.add_argument(
        "--zero", type=str, help="Letter at index 0.", default=None
    )
    parser.add_argument(
        "--not-zero", type=str, nargs="+", help="Letter at index 0."
    )
    parser.add_argument(
        "--one", type=str, help="Letter at index 1.", default=None
    )
    parser.add_argument(
        "--not-one", type=str, nargs="+", help="Letters not at index 1."
    )
    parser.add_argument(
        "--two", type=str, help="Letter at index 2.", default=None
    )
    parser.add_argument(
        "--not-two", type=str, nargs="+", help="Letters not at index 2."
    )
    parser.add_argument(
        "--three", type=str, help="Letter at index 3.", default=None
    )
    parser.add_argument(
        "--not-three", type=str, nargs="+", help="Letters not at index 3."
    )
    parser.add_argument(
        "--four", type=str, help="Letter at index 4.", default=None
    )
    parser.add_argument(
        "--not-four", type=str, nargs="+", help="Letters not at index 4."
    )
    parser.add_argument(
        "--contains", type=str, nargs="+", help="List of contained characters."
    )
    parser.add_argument(
        "--invalids", type=str, nargs="+", help="List of invalid characters."
    )
    args = parser.parse_args()

    setup_logging_from_args(args)
    valids = []

    for word in WORDS:
        valid = True
        word_copy = word
        i = 0
        if args.zero is not None:
            valid &= (args.zero == word_copy[0 - i])
            word_copy = word_copy.replace(word_copy[0 - i], '', 1)
            i += 1
        if args.one is not None:
            valid &= (args.one == word_copy[1 - i])
            word_copy = word_copy.replace(word_copy[1 - i], '', 1)
            i += 1
        if args.two is not None:
            valid &= (args.two == word_copy[2 - i])
            word_copy = word_copy.replace(word_copy[2 - i], '', 1)
            i += 1
        if args.three is not None:
            valid &= (args.three == word_copy[3 - i])
            word_copy = word_copy.replace(word_copy[3 - i], '', 1)
            i += 1
        if args.four is not None:
            valid &= (args.four == word_copy[4 - i])

        if args.not_zero is not None:
            for letter in args.not_zero:
                valid &= (word[0] != letter)
        if args.not_one is not None:
            for letter in args.not_one:
                valid &= (word[1] != letter)
        if args.not_two is not None:
            for letter in args.not_two:
                valid &= (word[2] != letter)
        if args.not_three is not None:
            for letter in args.not_three:
                valid &= (word[3] != letter)
        if args.not_four is not None:
            for letter in args.not_four:
                valid &= (word[4] != letter)

        if args.contains is not None:
            for contain in args.contains:
                valid &= (contain in word_copy)

        if args.invalids is not None:
            for invalid in args.invalids:
                valid &= (invalid not in word_copy)

        if valid:
            valids.append(word)
            logger.info(f"{word}")

    scores = word_scores(valids)
    i = scores.index(max(scores))

    logger.info(f"{valids[i]} {scores[i]} {100 / len(scores):0.2f}%")
    logger.info(f"Total Remaining: {len(scores)}")


def general_brute_force(guessables, words):
    guess_avgs = []
    guessers = [Guesser(word) for word in words]

    for guess in guessables:
        possible_valids_sum = 0
        for guesser in guessers:
            result = guesser.guess(guess)
            valids = valid_words([guess], [result], words)
            if result == "22222":
                valids.remove(guess)
            possible_valids_sum += len(valids)

        guess_avgs.append(possible_valids_sum / len(words))
        logger.debug(f"Guess: {guess} Score: {guess_avgs[-1]:0.2f}")

    best_guess_avg = min(guess_avgs)
    best_guess_index = guess_avgs.index(best_guess_avg)

    return guessables[best_guess_index], best_guess_avg


def brute_force():
    """CLI Entrypoint for brute force guess calculations."""
    parser = argparse.ArgumentParser("Convergle Brute Force CLI.")
    add_logging_parser(parser)
    parser.add_argument(
        "--guesses", nargs="+", type=str, help="List of guesses", default=[]
    )
    parser.add_argument(
        "--results",
        nargs="+",
        type=str,
        help="List of guess results",
        default=[],
    )
    args = parser.parse_args()

    setup_logging_from_args(args)
    starting_words = valid_words(args.guesses, args.results)

    best_guess, average = general_brute_force(WORDS, starting_words)
    logger.info(f"Best Guess: {best_guess}")
    logger.info(f"Average resulting valids: {average}")
