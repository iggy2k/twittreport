import sys
import os
import twint

if len(sys.argv) != 2:
    print("Invalid number of arguments")
    exit()

# Configure
c = twint.Config()

c.Username = sys.argv[1]

# Optional for accounts with tons of tweets
# c.Search = input("Filter word: ")
c.Output = "raw_tweets.txt"

# Silent run
c.Hide_output = True

# Run
twint.run.Search(c)

# Clean tweet data
count = 0
with open('raw_tweets.txt', encoding="utf8") as fin, open('clean.txt', 'a', encoding="utf8") as fout:
    for line in fin:
        count += 1
        fout.writelines(line[57:])
        os.system('cls')
        print("Processing tweet {}".format(count))
print('Total tweets: ' + str(count))
