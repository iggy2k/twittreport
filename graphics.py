import matplotlib.pyplot as plt
import os
import random
from os import path
from wordcloud import WordCloud
import numpy as np

# Boiler


def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = int(360.0 * random.randint(1, 36) * 10 / 255.0)
    s = int(100.0 * random.randint(175, 255) / 255.0)
    l = int(100.0 * random.randint(60, 120) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)


# Generate noun cloud
def noun_cloud():

    # REFACTOR
    text = open('nouns.txt').read()

    wordcloud = WordCloud(background_color='white',
                          max_font_size=50,
                          width=595,
                          height=842,
                          repeat=True,
                          color_func=random_color_func
                          ).generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('nouns.png', dpi=300, bbox_inches='tight', pad_inches=0)

# Generate verb bar chart


def verb_bar():
    verbs = []
    values = []

    # TO BE REFACTORED
    for i, line in enumerate((list(open("analyzed.csv")))):
        if 4 < i < 14:
            temp = line.split(',')
            verbs.append(temp[0])
            values.append(temp[1])

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=verbs,
            startangle=90)
    ax1.axis('equal')
    plt.savefig('verbs.png', dpi=300, bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    noun_cloud()
    verb_bar()
