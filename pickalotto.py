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
try:
    import yaml
except ImportError as ex:
    print("PyYaml is missing")

NAME = "PickALotto"
__author__ = 'mardix'
__version__ = "0.3.0"

CWD = os.getcwd()
games_data_file = CWD + "/pickalotto.data"

# Default Plays for Powerball and Megamillion
DEFAULT_GAMES = {
    "megamillions": {
        "balls": range(1, 76),
        "bonus": range(1, 16),
        "balls_to_draw": 5,
        "bonus_to_draw": 1,
        "prizes": {
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
        }
    },
    "powerball": {
        "balls": range(1, 70),
        "bonus": range(1, 27),
        "balls_to_draw": 5,
        "bonus_to_draw": 1,
        "prizes": {
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
        }
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


class Lotto(object):

    def __init__(self):
        self.games = DEFAULT_GAMES

    @staticmethod
    def gen_random_numbers(numbers, total=5):
        """
        Given a list of numbers, it will randomly create a sample of x total items
        :param numbers: list - Numbers to create the sample
        :param total: int - Total number to have on the list
        :return: list
        """
        return sorted(random.sample(numbers, total))

    @staticmethod
    def gen_ticket_key(length=8):
        """
        Generate a ticket key
        :param length:
        :return:
        """
        char_set = string.ascii_uppercase + string.digits
        return ''.join(random.sample(char_set * (length - 1), length))

    def load_games_data(self, f):
        with open(f) as yfile:
            games = yaml.load(yfile)
            for k, v in games.items():
                prizes = {}
                for pk, pv in v["prizes"].items():
                    balls = int(pk.split(",", 2)[0])
                    bonus = True if pk.split(",", 2)[1].lower() == "true" else False
                    prizes.update({(balls, bonus): pv})
                games[k]["prizes"] = prizes
        self.games = games

    def select(self, game):
        """
        To select a game
        :param game:
        :return:
        """
        self.game = self.games[game]

    def pick(self, total_picks):
        """
        Return a list of list containing the numbers to plays
        :param total_picks:
        :return: list
        """
        pick_count = 0
        failed_attempt = 0
        numbers = []
        while True:
            pick = self.gen_random_numbers(self.game["balls"], self.game["balls_to_draw"])

            if self.game["bonus"]:
                pick += self.gen_random_numbers(self.game["bonus"], self.game["bonus_to_draw"])

            if pick not in numbers:
                numbers.append(pick)
                pick_count += 1
                if pick_count >= total_picks:
                    break
            else:
                failed_attempt += 1
                if failed_attempt == max_failed_attempt:
                    raise Exception("Pick Numbers max failed attempt reached")
        return numbers

    def match(self, winning_number, number):
        """
        Match the winning number with
        :param winning_number: list - list of the winning number
        :param number: List - The number to check against winning number
        :return:
        """
        winning_number = map(int, winning_number)
        number = map(int, number)
        balls = winning_number[:self.game["balls_to_draw"]]
        wb = number[:self.game["balls_to_draw"]]
        wb_hit = sum(1 for x in wb if x in balls)
        result = (wb_hit, False)

        if self.game["bonus"]:
            bonus = winning_number[self.game["balls_to_draw"]:][0]
            gb = number[self.game["balls_to_draw"]:][0]
            gb_hit = gb == bonus
            result = (wb_hit, gb_hit)

        prize = self.game["prizes"][result]
        return number, prize, result

    def match_numbers(self, winning_number, numbers):
        """
        To match a list of numbers
        :param winning_numbers:
        :param numbers:
        :return: generator
        """
        for number in numbers:
            yield self.match(winning_number=winning_number, number=number)
# ------------------------------------------------------------------------------

def main():
    import argparse

    def print_table(table):
        t = ['|' + ''.join('%5s' % i for i in row) + ' ' for row in table]
        hdr = '+' + (len(t[0])+5) * '-' + '+'
        print('\n'.join([hdr] + t + [hdr]))

    def title(title):
        print ("")
        print ("::: %s :::" % title)
        print ("")
        
    def header():
        print (__doc__)
        print ("v. %s" % __version__)

    parser = argparse.ArgumentParser()

    parser.add_argument("--game", "-g",
                        help="The game to play [-g powerball | megamillions]",
                        )

    parser.add_argument("--pick", "-p",
                        help="Select the total numbers to Pick and Play"
                             " ie [--pick 15]")

    parser.add_argument("--check", "-c",
                        help="To check a winning number against all the "
                             "numbers picked. "
                             "Separate the winning numbers with commas, with "
                             "the BONUS ball being last"
                             " ie [--check 14,5,8,3,19,26 ]")

    parser.add_argument("--file", "-f",
                        help="With --pick or --check."
                             "The file, in CSV format, to save to or load numbers from. "
                             " ie [--pick 15 --file myfile.csv]")

    parser.add_argument("--show-all",
                        help="To show all plays when checking for a winning number, import the "
                             "csv file containing the numbers"
                             " ie [--check 14,5,8,3,19,26  --file "
                             "myfile.csv --show-all]",
                        action="store_true")
    parser.add_argument("--data",
                        help="Path of pickalotto.data file to load. When empty it will attempt local directory"
                             " ie [--data pickalotto.data --check 14,5,8,3,19,26 ]")
    parser.add_argument("--list", "-l",
                        help="List all the games available",
                        action="store_true")
    try:

        args = parser.parse_args()
        game_name = args.game
        csv_file = args.file

        lotto = Lotto()
        data_file = args.data or games_data_file
        if os.path.isfile(data_file):
            lotto.load_games_data(data_file)

        header()
        if args.pick:
            lotto.select(game_name)
            num = args.pick

            while True:
                title("Generating %s numbers" % game_name.upper())
                numbers = lotto.pick(int(num))
                print_table(numbers)
                print ("")

                while True:
                    action = raw_input("* Save these numbers? (y=Yes, r=Reload, q=Quit) : ")
                    if action.lower() == "y":
                        if not csv_file:
                            d = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            csv_file = "%s/" % os.getcwd()
                            csv_file += "%s-%s-picks-%s" % (game_name, num, d)
                        if not csv_file.endswith(".csv"):
                            csv_file += ".csv"
                        export_to_csv(numbers, csv_file)
                        print("-- Numbers saved successfully at: %s" % csv_file)
                        exit()
                    elif action.lower() == "r":
                        break
                    elif action.lower() == "q":
                        print("-- Quitting without saving numbers")
                        exit()

        elif args.check:
            lotto.select(game_name)
            title("Checking %s winning numbers and prizes" % game_name.upper())
            print("Good luck! :)")
            print("")

            winning_number = args.check.split(",")
            show_all = args.show_all
            numbers = import_from_csv(csv_file)
            results = lotto.match_numbers(winning_number=winning_number,
                                          numbers=numbers)
            results_nums = []
            for r in results:
                show = True if show_all else True if r[1] != 0 else False
                if show:
                    results_nums.append(r[0] + ["$ ", "%s" % str(r[1])])
            if results_nums:
                print_table(results_nums)
            else:
                print("It seems like you are out of luck!")
                print("Next time... :)")
            print ("")
        else:
            title("Listing Games To Play ")
            for name in lotto.games:
                print("- %s" % name)
            print("")

    except Exception as e:
        print("Error: %s" % e)
        raise

    print("Done")


if __name__ == "__main__":
    main()
