
#PickALotto

Winning!

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

    pickalotto powerball --pick 5
    
    
Folllow the instructions on the screen that asks you to SAVE, RELOAD and QUIT.

If you SAVE, a `.csv` file will be saved in the current working directory with the picked numbers. 

If you RELOAD, it will pick new random numbers.

If you QUIT, duh!

Now, if you want to save your numbers somewhere else, you can use `--output` arg to do so:

    pickalotto powerball --pick 5 --output powerball.csv

---

### Check numbers:

There you go, the time you've been waiting for. You want to know if you win. 

Before we continue, if you win the Jackpot, congrats. And Hook me up later. Hey!

Let's say the following numbers come out for `powerball`

    3 - 43 - 25 - 8 - 9  * 13
    
(*13 is the Powerball number.)

To check if you win (cross fingers)

    pickalotto powerball --check 9,10,16,20,45,23 --input powerball.csv
    

You will see a result similar to this if you win. Only the winning numbers will
be shown

    +-----------------------------------------------+
    |    9   10   16   20   45   23   $ JACKPOT 
    |    9   10   20   28   40    6   $   100 
    +-----------------------------------------------+
        
Of course the jackpot, if you win the jackpot.

If you want to show all the numbers:

    pickalotto powerball --check 9,10,16,20,45,23 --input powerball.csv --show-all


---

### For contributors

If anyone wants to contribute, please feel free to Pull Request. 

### Let's win together with PickALotto

---

### For the lottery players

I wish you good luck! - Mardix

---

(c) 2016 Mardix
