import os
from re import template
import subprocess
from analyzer import TwitAnalysis, analysis
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


from graphics import noun_cloud, verb_bar


def render(template_vars, pdf_out_path):
    '''Render the template and export it to a pdf. Assumes any images already exist.'''
    mentions = ''
    tags = ''
    structs = ''

    if template_vars['top_mentions']:
        mentions = (
            r'''\begin{enumerate}'''
            + '\n'.join(r'\item %s (%d)' % mention
                        for mention in template_vars['top_mentions'])
            + r'\end{enumerate}'
        )
    else:
        mentions = 'This user has never mentioned anyone.'

    if template_vars['top_tags']:
        tags = (
            r'''\begin{enumerate}
            '''
            + '\n'.join(r'\item %s (%d)' % tag
                        for tag in template_vars['top_tags'])
            + r'\end{enumerate}'
        )
    else:
        tags = 'This user has never tweeted any hashtags.'

    if template_vars['top_structs']:
        structs = (
            r'''\begin{enumerate}
            '''
            + '\n'.join(r'\item %s (%d)' % struct
                        for struct in template_vars['top_structs'])
            + r'\end{enumerate}'
        )
    else:
        structs = 'This user has no text tweets.'

    tex_template = ''

    with open('latex.tex') as fin:
        tex_template = fin.read()

    tex_template = tex_template.replace(
        '@USERNAME', template_vars['name']).replace(
        '@MENTIONS', mentions).replace(
            '@HASHTAGS', tags).replace(
                '@STRUCTURES', structs)

    with open(f'{pdf_out_path[:-4]}.tex', 'w') as fout:
        fout.write(tex_template)

    # proc = subprocess.Popen(['pdflatex', f'{pdf_out_path}.tex'])
    # proc.communicate()
    os.system(f'pdflatex {pdf_out_path[:-4]}.tex')


def main():
    anal = analysis()
    today = date.today()

    noun_cloud(anal, 'noun.png')
    verb_bar(anal, 'verb.png')

    most_mentions = []
    most_tags = []
    most_structs = []

    for k in sorted(anal.mentions, key=anal.mentions.get, reverse=True)[:5]:
        most_mentions.append((k, anal.mentions[k]))

    for k in sorted(anal.tags, key=anal.tags.get, reverse=True)[:5]:
        most_tags.append((k, anal.tags[k]))

    for k in sorted(anal.mostUsedStructs, key=anal.mostUsedStructs.get, reverse=True):
        most_structs.append((k, anal.mostUsedStructs[k]))

    template_vars = {
        'name': 'profile name here',
        'top_mentions': most_mentions,
        'top_tags': most_tags,
        'top_structs': most_structs,
    }
    time = today.strftime("%b-%d-%Y")
    render(template_vars, 'report-{}.pdf'.format(time))
    return 'report-{}.pdf'.format(time)


if __name__ == '__main__':
    main()
