from analyzer import TwitAnalysis, analysis
import pandas as pd
import matplotlib.pyplot as plt

from graphics import noun_cloud, verb_bar


def render(template_vars, pdf_out_path):
    '''Render the template and export it to a pdf. Assumes any images already exist.'''
    from weasyprint import HTML
    import os
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    html_out = template.render(template_vars)

    with open('html_out.html', 'w') as fout:
        fout.write(html_out)

    HTML(string=html_out, base_url=os.path.join(
        os.path.abspath(os.getcwd()), '')).write_pdf(pdf_out_path)


if __name__ == '__main__':
    anal = analysis()
    print(anal)

    noun_cloud(anal, 'noun.png')
    verb_bar(anal, 'verb.png')

    most_mentions = []
    most_tags = []

    for k in sorted(anal.mentions, key=anal.mentions.get, reverse=True)[:5]:
        most_mentions.append((k, anal.mentions[k]))

    for k in sorted(anal.tags, key=anal.tags.get, reverse=True)[:5]:
        most_tags.append((k, anal.tags[k]))

    template_vars = {
        'title': 'Test title',
        'name': 'profile name here',
        'img_logo': 'logo 512.png',
        'img_pfp': 'avatar.jpg',
        'img_nouns': 'noun.png',
        'img_verb': 'verb.png',
        'top_mentions': most_mentions,
        'top_tags': most_tags,
    }

    render(template_vars, 'report.pdf')
