import matplotlib.pyplot as plt
import os
import random
from os import path
from analyzer import TwitAnalysis
from wordcloud import WordCloud
import numpy as np

# Boiler


def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = int(360.0 * random.randint(1, 36) * 10 / 255.0)
    s = int(100.0 * random.randint(175, 255) / 255.0)
    l = int(100.0 * random.randint(60, 120) / 255.0)

    return "hsl({}, {}%, {}%)".format(h, s, l)


# Generate noun cloud
def noun_cloud(anal: TwitAnalysis, path_out):
    wordcloud = WordCloud(background_color='white',
                          max_font_size=50,
                          width=595,
                          height=842,
                          repeat=True,
                          color_func=random_color_func
                          ).generate_from_frequencies(anal.mostUsedNouns)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(path_out, dpi=300, bbox_inches='tight', pad_inches=0)

# Generate verb bar chart


def verb_bar(anal: TwitAnalysis, path_out):
    fig1, ax1 = plt.subplots()
    ax1.pie(anal.mostUsedVerbs.values(), labels=anal.mostUsedVerbs.keys(),
            startangle=90)
    ax1.axis('equal')
    plt.savefig(path_out, dpi=300, bbox_inches='tight', pad_inches=0)