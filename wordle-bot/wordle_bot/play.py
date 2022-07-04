"""Play Convergle."""
import argparse
import logging
import json
import random
import numpy as np
from convergeutils.utils import add_logging_parser, setup_logging_from_args
from wordle_bot.guess import Guesser
from wordle_bot.words import GUESSES, WORDS
from wordle_bot.analysis import general_brute_force, valid_words

logger = logging.getLogger(__name__)


def play():
    """Entry point for convergle play script."""
    parser = argparse.ArgumentParser("Play Convergle CLI Script")
    add_logging_parser(parser)

    args = parser.parse_args()
    setup_logging_from_args(args)
    word = random.choice(WORDS)
    guesser = Guesser(word)
    result = "00000"

    while result != "22222":
        guess = input("Please enter guess: ").strip()
        if guess not in GUESSES:
            logger.info("Guess invalid please try again.")
            continue
        result = guesser.guess(guess)
        logger.info(result)


def sim_all_wordles():
    """Entry point for sim of all wordles."""
    parser = argparse.ArgumentParser("Bot plays all wordles CLI Script")
    add_logging_parser(parser)
    parser.add_argument(
        "--save-file",
        type=str,
        help="File to save all guess data.",
        default="guesses.txt",
    )
    parser.add_argument(
        "--start-word",
        type=str,
        help="Word for initial guess",
        default="raise",
    )

    args = parser.parse_args()
    setup_logging_from_args(args)

    counts = []
    count_one_results = []
    count_two_guesses = []
    saved_results = []
    saved_guesses = []

    for word in WORDS:
        logger.info(f"WORD: {word}")
        words = WORDS.copy()
        guesser = Guesser(word)
        result = "00000"
        result_str = ""
        count = 0
        guesses = []
        results = []
        while result != "22222":
            count += 1
            if count == 1:
                guess = args.start_word
            elif count == 2 and result in count_one_results:
                index = count_one_results.index(result)
                guess = count_two_guesses[index]
            else:
                guess, _ = general_brute_force(GUESSES, words)
                if count == 2:
                    count_one_results.append(result)
                    count_two_guesses.append(guess)
            guesses.append(guess)
            if result_str not in saved_results:
                saved_results.append(result_str)
                saved_guesses.append(guess)
            result = guesser.guess(guess)
            results.append(result)
            result_str += result
            logger.info(f"GUESS: {guess} RESULT: {result}")
            words = valid_words(guesses, results)

        logger.info(f"Bot took {count} guesses for {word}!")
        counts.append(count)

    logger.info(f"Average guesses: {np.mean(counts):0.2f}!")

    with open(args.save_file, "w") as savefile:
        for result, guess in zip(saved_results, saved_guesses):
            savefile.write(f"{result},{guess}\n")


def best_guess_lookup():
    parser = argparse.ArgumentParser("Bot plays all wordles CLI Script")
    add_logging_parser(parser)
    parser.add_argument(
        "--save-file",
        type=str,
        help="File to load all guess data.",
        default="guesses.txt",
    )
    parser.add_argument("--result", type=str, help="Result String to look up.")

    args = parser.parse_args()
    setup_logging_from_args(args)

    with open(args.save_file, "r") as raw_data:
        lines = raw_data.readlines()

    results = []
    guesses = []

    for line in lines:
        line = line.strip()
        data = line.split(",")
        results.append(data[0])
        guesses.append(data[1])

    index = results.index(args.result)
    logger.info(f"Guess: {guesses[index]}")


def autoplay():
    import requests

    parser = argparse.ArgumentParser("Bot plays all wordles CLI Script")
    add_logging_parser(parser)
    parser.add_argument(
        "--save-file",
        type=str,
        help="File to load all guess data.",
        default="guesses.txt",
    )

    args = parser.parse_args()
    setup_logging_from_args(args)

    with open(args.save_file, "r") as raw_data:
        lines = raw_data.readlines()

    results = []
    guesses = []

    for line in lines:
        line = line.strip()
        data = line.split(",")
        results.append(data[0])
        guesses.append(data[1])

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Token 473805f5ac005529b15f37c35248f54e78e99f53',
        'Connection': 'keep-alive',
        'Referer': 'https://converge-general-sports.herokuapp.com/wordle',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',  # noqa
        'X-CSRFToken': 'FZKSyo3hi3vtEoJ4VztOxKHloNqpg8e4tIz1XzxMzBJ5CZGi9eYhMH9FSTUJYIS7',  # noqa
    }

    cookies = {
        'csrftoken': 'FZKSyo3hi3vtEoJ4VztOxKHloNqpg8e4tIz1XzxMzBJ5CZGi9eYhMH9FSTUJYIS7',  # noqa
        'sessionid': '2thjprskw2pcolztfkixk3ojayb1f8up',
    }
    count = 0

    while True:
        try:
            status = json.loads(
                requests.get(
                    'https://converge-general-sports.herokuapp.com/api/v1/wordle/status',  # noqa
                    cookies=cookies,
                    headers=headers,
                ).content
            )

            logger.info(status["correct"])
            index = results.index(status["correct"])
            guess = guesses[index]
            logger.info(guess)

            json_data = {
                "guess": guess
            }

            requests.post(
                'https://converge-general-sports.herokuapp.com/api/v1/wordle/guess',  # noqa
                cookies=cookies,
                headers=headers,
                json=json_data,
            )
            count += 1
        except Exception:
            logger.info(f"Worldle Complete in {count} guesses!")
            break
