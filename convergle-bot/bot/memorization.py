"""This file contains tools for easily memorizing a lookup tree."""
import argparse
import logging
from convergeutils.utils import add_logging_parser, setup_logging_from_args

logger = logging.getLogger(__name__)


def memorize_analysis():
    """Entry point for memorization of lookup tree."""
    parser = argparse.ArgumentParser("Memorization tool CLI Script")
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

    count = 0
    for result, guess in zip(results, guesses):
        if len(result) == 5:
            count2 = 0

            for result2 in results:
                if len(result2) == 10:
                    if result2[:5] == result:
                        count2 += 1

            logger.info(f"{result} -> {guess} -> {count2}")
            count += 1

    logger.info(f"Initial tree size {count}")
