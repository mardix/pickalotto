"""
-------------------------------------------------------------------------------------------
 /$$$$$$$  /$$           /$$        /$$$$$$  /$$                   /$$     /$$
| $$__  $$|__/          | $$       /$$__  $$| $$                  | $$    | $$
| $$  \ $$ /$$  /$$$$$$$| $$   /$$| $$  \ $$| $$        /$$$$$$  /$$$$$$ /$$$$$$    /$$$$$$
| $$$$$$$/| $$ /$$_____/| $$  /$$/| $$$$$$$$| $$       /$$__  $$|_  $$_/|_  $$_/   /$$__  $$
| $$____/ | $$| $$      | $$$$$$/ | $$__  $$| $$      | $$  \ $$  | $$    | $$    | $$  \ $$
| $$      | $$| $$      | $$_  $$ | $$  | $$| $$      | $$  | $$  | $$ /$$| $$ /$$| $$  | $$
| $$      | $$|  $$$$$$$| $$ \  $$| $$  | $$| $$$$$$$$|  $$$$$$/  |  $$$$/|  $$$$/|  $$$$$$/
|__/      |__/ \_______/|__/  \__/|__/  |__/|________/ \______/    \___/   \___/   \______/
--------------------------------------------------------------------------------------------
"""


from __future__ import print_function
import os
import csv
import string
import random
import datetime


__author__ = 'mardix'
NAME = "PickALotto"
__version__ = "0.1.1"

MEGAMILLIONS = "megamillions"
POWERBALL = "powerball"
POWERBALL_MOST_DRAWN = "powerball_md"

PRIZES = {
    "powerball": {
            (0, False): 0,
            (1, False): 0,
            (2, False): 0,
            (3, False): 7,
            (4, False): 100,
            (5, False): 1000000,
            (0, True): 4,
            (1, True): 4,
            (2, True): 7,
            (3, True): 100,
            (4, True): 50000,
            (5, True): "JACKPOT"
        },
    "megamillions": {
            (0, False): 0,
            (1, False): 0,
            (2, False): 0,
            (3, False): 5,
            (4, False): 500,
            (5, False): 1000000,
            (0, True): 1,
            (1, True): 2,
            (2, True): 5,
            (3, True): 50,
            (4, True): 5000,
            (5, True): "JACKPOT"
        },
}

GAMES = {
    MEGAMILLIONS: {
        "balls": range(1, 75 + 1),
        "powerballs": range(1, 15 + 1),
        "prizes": PRIZES["megamillions"]
    },
    POWERBALL: {
        "balls": range(1, 69 + 1),
        "powerballs": range(1, 26 + 1),
        "prizes": PRIZES["powerball"]
    },
    POWERBALL_MOST_DRAWN: {
        "balls": [2, 8, 9, 10, 12, 13, 14, 15, 16, 19, 20, 22, 26, 27, 28, 29, 30, 32, 35, 39, 40, 41, 42, 45, 47, 55, 56, 57, 62, 63, 64, 68, 69],
        "powerballs": [1, 2, 6, 9, 10, 11, 12, 13, 15, 17, 18, 20, 21, 22, 23, 24, 26],
        "prizes": PRIZES["powerball"]
    }
}

# ------------------------------------------------------------------------------

def import_from_csv(filename):
    numbers = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        numbers = list(reader)
    return numbers

def export_to_csv(list, filename):
    """
    To save numbers to a file name as CSV
    :param list:
    :param filename:
    :return:
    """
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for l in list:
            writer.writerow(l)


def gen_ticket_key(length=8):
    """
    Generate a ticket key
    :param length:
    :return:
    """
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set * (length - 1), length))


def gen_random_numbers(numbers, total=5):
    """
    Given a list of numbers, it will randomly create a sample of x total items
    :param numbers: list - Numbers to create the sample
    :param total: int - Total number to have on the list
    :return: list
    """
    return sorted(random.sample(numbers, total))


def pick_numbers(balls,
                 powerballs,
                 total_picks=5,
                 max_balls=5,
                 max_powerball=1,
                 max_failed_attempt=100):
    """
    To create a random pick from a list of numbers
    :param balls: list - All White balls
    :param powerball: list - All power balls numbers
    :param total_picks: int - Total numbers to pick
    :param max_balls: int - Total of balls to select
    :param max_powerball: int - Total of powerball number to pick
    :param max_failed_attempt: int - The number of failed numbers until it gives up
    :return: list
    """
    pick_count = 0
    failed_attempt = 0
    numbers = []
    while True:
        pick = gen_random_numbers(balls, max_balls)
        pick += gen_random_numbers(powerballs, max_powerball)

        if pick not in numbers:
            numbers.append(pick)
            pick_count += 1
            if pick_count >= total_picks:
                break
        else:
            failed_attempt += 1
            if failed_attempt == max_failed_attempt:
                raise Exception("quick_pick max failed attempt reached")
    return numbers


def match_winning_number(winning_number, number, prizes, max_balls=5, max_powerball=1):
    """
    :param winning_number: list - list of the winning number
    :param number: List - The number to check against winning number
    :param prizes:
    :param max_balls: int - Total of balls to select
    :param max_powerball: int - Total of powerball number to pick
    :return: tuple, (number played, prize won, the matching set)
    """
    wn = winning_number[:max_balls]
    pwn = winning_number[max_powerball:][0]
    wb = number[:max_balls]
    gb = number[max_powerball:][0]
    wb_hit = sum(1 for x in wb if x in wn)
    gb_hit = gb == pwn
    result = (wb_hit, gb_hit)
    prize = prizes[result]
    return number, prize, result


# ------------------------------------------------------------------------------

def main():
    import argparse

    def format_number(l):
        """
         Pretty print the numbers
        """
        p = " ".join(["(%s)" % i for i in l[:5]])
        p += " [* %s]" % l[5]
        return p

    def print_table(table):
        t = ['|' + ''.join('%5s' % i for i in row) + ' ' for row in table]
        hdr = '+' + (len(t[0])+5) * '-' + '+'
        print('\n'.join( [hdr] + t + [hdr]))

    def title(title):
        print ("")
        print ("::: %s :::" % title)
        print ("")

    def show_line():
        print ("_" * 80)
        
    def header():
        print (__doc__)
        print ("v. %s" % __version__)

    parser = argparse.ArgumentParser()

    parser.add_argument("game",
                        help="The game to play [powerball | megamillions]",
                        )

    parser.add_argument("--pick", "-p",
                        help="Select the total amount to Pick and Play"
                             " ie [--pick 15]")
    parser.add_argument("--output", "-o",
                        help="With --pick. After generating the numbers. "
                             "The file, in CSV format, to save the numbers to. "
                             " ie [--pick 15 --output myfile.csv]")

    parser.add_argument("--check", "-c",
                        help="To check a winning number against all the "
                             "numbers picked."
                             "Separate the winning numbers with commas, with "
                             "the POWERBALL being last"
                             " ie [--check 14,5,8,3,19,26 ]")
    parser.add_argument("--input", "-i",
                        help="With --check. When checking for a winning number,"
                             "import the csv file containing the numbers"
                             " ie [--check 14,5,8,3,19,26  --input myfile.csv]")
    parser.add_argument("--show-all",
                        help="When checking for a winning number, import the "
                             "csv file containing the numbers"
                             " ie [--check 14,5,8,3,19,26  --input "
                             "myfile.csv --show-all]",
                        action="store_true")
    #parser.add_argument("--config",
    #                    help="On PLAY, a method to select a quick pick numbers"
    #                         " ie [--config ]")

    try:
        args = parser.parse_args()
        game_name = args.game
        games = GAMES[game_name]

        header()
        if args.pick:
            num = args.pick
            output = args.output

            while True:
                title("Generating %s numbers" % game_name.upper())

                numbers = pick_numbers(balls=games["balls"],
                                       powerballs=games["powerballs"],
                                       total_picks=int(num))
                print_table(numbers)
                print ("")

                while True:
                    action = raw_input("* Save these numbers? (y=Yes, r=Reload, q=Quit) : ")
                    if action.lower() == "y":
                        if not output:
                            d = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            output = "%s/" % os.getcwd()
                            output += "%s-%s-picks-%s" % (game_name, num, d)
                        if not output.endswith(".csv"):
                            output += ".csv"
                        export_to_csv(numbers, output)
                        print("-- Numbers saved successfully at: %s" % output)
                        exit()
                    elif action.lower() == "r":
                        break
                    elif action.lower() == "q":
                        print("-- Quitting without saving numbers")
                        exit()

        elif args.check:
            title("Checking %s winning numbers and prizes" % game_name.upper())
            print("Good luck! :)")
            print("")
            prizes = games["prizes"]
            input = args.input
            show_all = args.show_all

            winning_number = args.check.split(",")
            numbers = import_from_csv(input)

            results_nums = []
            for number in numbers:
                r = match_winning_number(winning_number, number, prizes)
                show = True if show_all else True if r[1] != 0 else False
                if show:
                    results_nums.append(number + ["$ ", "%s" % str(r[1])])
            print_table(results_nums)
            print ("")

    except Exception as e:
        print("Error")
        print(e)

    print("Done")


if __name__ == "__main__":
    main()
