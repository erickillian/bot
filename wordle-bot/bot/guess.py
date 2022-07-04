"""This file contains guess calculation functionality."""
import argparse
import logging
import random
from convergeutils.utils import add_logging_parser, setup_logging_from_args
from convergle_bot.words import WORDS, GUESSES

logger = logging.getLogger(__name__)


class Guesser:
    """This class stores a word and calculates the guess results."""
    def __init__(self, word: str):
        self.word = word

    def guess(self, guess: str):
        """Provide a word guess and get the results of the guess."""
        correct = ""
        word_copy = list(self.word)

        for i, letter in enumerate(guess):
            if letter == self.word[i]:
                word_copy.pop(word_copy.index(letter))

        for i, letter in enumerate(guess):
            if letter == self.word[i]:
                correct += "2"
                if letter in word_copy:
                    word_copy.pop(word_copy.index(letter))
            elif letter in word_copy:
                correct += "1"
                word_copy.pop(word_copy.index(letter))
            else:
                correct += "0"

        return correct


def guesser_test():
    parser = argparse.ArgumentParser("CLI Tool for Guesser Test.")
    add_logging_parser(parser)
    parser.add_argument(
        "--word", type=str, help="True word to be guessed.", default=None
    )
    parser.add_argument(
        "--guess", type=str, help="Guess of the word.", default=None
    )
    parser.add_argument(
        "--seed", type=int, help="Python random seed.", default=None
    )
    args = parser.parse_args()

    setup_logging_from_args(args)

    if args.seed is not None:
        random.seed(args.seed)
    if args.word is None:
        args.word = random.choice(WORDS)
        logger.debug(f"Randomly chose word to be '{args.word}'")
    if args.guess is None:
        args.guess = random.choice(GUESSES)
        logger.info(f"Randomly chose guess to be '{args.guess}'")

    assert len(args.word) == 5, "Word not 5 letters!"
    assert len(args.guess) == 5, "Guess not 5 letters!"

    assert args.word in WORDS, "Invalid word!"
    assert args.guess in GUESSES, "Invalid guess!"

    guesser = Guesser(args.word)
    logger.info(guesser.guess(args.guess))
