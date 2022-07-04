"""This file contains tools for easily memorizing a lookup tree."""
import argparse
import logging

logger = logging.getLogger(__name__)


def memorize_analysis():
    """Entry point for memorization of lookup tree."""
    parser = argparse.ArgumentParser("Memorization tool CLI Script")
    parser.add_argument(
        "--loglevel",
        type=int,
        help="Loglevel integer for logging system.",
        default=logging.INFO,
    )

    parser.add_argument(
        "--logfile",
        type=str,
        help="Logfile to write log.",
        default=None,
    )
    parser.add_argument(
        "--save-file",
        type=str,
        help="File to load all guess data.",
        default="guesses.txt",
    )

    args = parser.parse_args()
    if args.logfile is None:
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] %(message)s',
            level=args.loglevel,
            datefmt='%Y-%m-%d %H:%M:%S',
        )
    else:
        logging.basicConfig(
            format='%(asctime)s [%(levelname)s] %(message)s',
            level=args.loglevel,
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(args.logfile),
                logging.StreamHandler(sys.stdout),
            ],
        )

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
