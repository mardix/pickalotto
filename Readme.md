
#PickALotto

Winning 0.2.x!

---

###Want to win the lottery? Great!

PickALotto will randomly select unique numbers for you to play in Powerball and
MegaMillion Lottery. The numbers can then be saved in .CSV file to be checked 
later on after the winning number comes out.

**DISCLAIMER**: We should not be held responsible for any loss of money. Gamble responsibly
PickALotto doesn't guarantee any win. Most likely you will lose. 
Actually, even before you start playing you are already at a loss. But this script is a fun exercise.
But if in case you win any money, don't forget about me, lol. Help a Brother Out (HBO)! 
Email me at: mardix@pylot.io

License: MIT

---

### What would be the use case for this program?

Let's see... If you are planning on playing more than 5 tickets and want to make sure each number is 
unique, this this program is for you.

It will create unique numbers for you, and also quickly check the 
winning against all the numbers you played. 

---

## Installation

    pip install pickalotto
    
---

## Usage

### Pick numbers: 

The example below will generate 5 random numbers for `powerball`. You can also chose
`megamillion`.

    pickalotto --game powerball --pick 5
    
    
Folllow the instructions on the screen that asks you to SAVE, RELOAD and QUIT.

If you SAVE, a `.csv` file will be saved in the current working directory with the picked numbers. 

If you RELOAD, it will pick new random numbers.

If you QUIT, duh!

Now, if you want to save your numbers somewhere else, you can use `--output` arg to do so:

    pickalotto -g powerball -p 5 -o powerball.csv

---

### Check numbers:

There you go, the time you've been waiting for. You want to know if you win. 

Before we continue, if you win the Jackpot, congrats. And Hook me up later. Hey!

Let's say the following numbers come out for `powerball`

    3 - 43 - 25 - 8 - 9  * 13
    
(*13 is the Powerball number.)

To check if you win (cross fingers)

    pickalotto -g powerball --check 9,10,16,20,45,23 --input powerball.csv
    
The numbers for `--check` must be separated with a comma with the powerball number as the last one.

You will see a result similar to this if you win. Only the winning numbers will
be shown

    +-----------------------------------------------+
    |    9   10   16   20   45   23   $ JACKPOT 
    |    9   10   20   28   40    6   $   100 
    +-----------------------------------------------+
        
Of course the jackpot, if you win the jackpot.

If you want to show all the numbers:

    pickalotto -g powerball -c 9,10,16,20,45,23 -i powerball.csv --show-all

---

## Advanced

You can setup your plays to create your own drawings

### plays.data

By default PickALotto will attempt to load from the current dir `plays.data` 
which contains the numbers and prizes.

`plays.data` is a Yaml file. 

This will list all the games available

    pickalotto 
    

To load the plays.data

    pickalotto --plays path/to/plays.data -g megamillion -p 5

Combine it with other actions:

    pickalotto --plays path/to/plays.data -g megamillion -p 5


`plays.data` example

FYI, the file is in Yaml


    powerball:
        balls: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        bonus: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        balls_to_draw: 5
        bonus_to_draw: 1
        prizes:
            0, False: 0
            1, False: 0
            2, False: 0
            3, False: 7
            4, False: 100
            5, False: 1000000
            0, True: 4
            1, True: 4
            2, True: 7
            3, True: 100
            4, True: 50000
            5, True: "JACKPOT"    
    
    megamillions:
        balls: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        bonus: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        balls_to_draw: 5
        bonus_to_draw: 1
        prizes:
            0, False: 0
            1, False: 0
            2, False: 0
            3, False: 5
            4, False: 500
            5, False: 1000000
            0, True: 1
            1, True: 2
            2, True: 5
            3, True: 50
            4, True: 5000
            5, True: "JACKPOT"
    
    powerball_most_drawn:
        balls: [2, 8, 9, 10, 12, 13, 14, 15, 16, 19]
        bonus: [1, 2, 6, 9, 10, 11, 12, 13, ]
        balls_to_draw: 5
        bonus_to_draw: 1
        prizes:
            0, False: 0
            1, False: 0
            2, False: 0
            3, False: 7
            4, False: 100
            5, False: 1000000
            0, True: 4
            1, True: 4
            2, True: 7
            3, True: 100
            4, True: 50000
            5, True: "JACKPOT"
            
- balls: list of numbers to pick
- bonus: list of bonus balls to pick
- balls_to_draw: the number of balls to draw
- bonus_to_draw: The number of bonus balls to draw
- prize: dict of tuple match (the total balls won, Bonus ball picked)

    0, False: 0 -> means, balls match 0 numbers + 0 bonus. It will give out $0 as prize
    
    4, True: 50000 -> means, balls match 4 numbers + the bonus ball. It will give out $5000 as prize
    
    5, True: Jackpot -> means, balls match 5 numbers + the bonus ball. It will give out Jackpot as prize
    
---

### For contributors

If anyone wants to contribute, please feel free to Pull Request. 

### Let's win together with PickALotto

---

### For the lottery players

I wish you good luck! - Mardix

---

(c) 2016 Mardix
