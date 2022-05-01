import sys
import os
import twint
import urllib.request


def main(name_from_gui=None):
    if len(sys.argv) != 2 and name_from_gui is None:
        print("Invalid number of arguments")
        exit()

    # Configure
    c = twint.Config()

    if len(sys.argv) != 2:
        c.Username = name_from_gui
    else:
        c.Username = sys.argv[1]

    # Optional for accounts with tons of tweets
    # c.Search = input("Filter word: ")
    c.Output = "raw_tweets.txt"

    # Silent
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

    # Get avatar

    c.Format = "{avatar}"
    c.Output = "avatar.txt"
    twint.run.Lookup(c)

    f = open("avatar.txt", "r")
    url = f.readline()
    urllib.request.urlretrieve(url.replace("normal", "400x400"), "avatar.jpg")
    return


if __name__ == '__main__':
    main()
