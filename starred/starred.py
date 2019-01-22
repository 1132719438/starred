#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
from io import BytesIO
from collections import OrderedDict
import click
from github3 import GitHub
from github3.exceptions import NotFoundError
from github3.exceptions import ForbiddenError
from terminaltables import GithubFlavoredMarkdownTable
import pickle
import operator


try:
    from starred import VERSION
except ImportError:
    VERSION = 'dev'


badge_url = 'https://cdn.rawgit.com/sindresorhus/awesome/d730'\
            '5f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg'

awesome_url = 'https://github.com/sindresorhus/awesome'

github_url = 'https://github.com/1132719438/starred'

count_badge = 'https://img.shields.io/badge/Total-{count}-{color}.svg'
date_badge = 'https://img.shields.io/badge/Date-{today}-{color}.svg'

desc = '''# Awesome Stars [![Awesome]({badge_url})]({awesome_url})

> A curated list of my GitHub stars!  Generated by [starred]({github_url}).

![Total]({count_badge_url})
![Date]({date_badge_url})

## Contents
'''

license_ = '''
## License

[![CC0](http://mirrors.creativecommons.org/presskit/buttons/88x31/svg/cc-zero.svg)]\
(https://creativecommons.org/publicdomain/zero/1.0/)

To the extent possible under law, [{username}](https://github.com/{username})\
 has waived all copyright and related or neighboring rights to this work.
'''

html_escape_table = {
    ">": "&gt;",
    "<": "&lt;",
}


def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c, c) for c in text)


@click.command()
@click.option('--username', envvar='USER', help='GitHub username', required=True)
@click.option('--token', envvar='GITHUB_TOKEN', help='GitHub token')
@click.option('--sort', type=click.Choice(['stars', 'date', 'name']), default='date',
              help='sort by language with stars, date or name')
@click.option('--repository', default='', help='repository name')
@click.option('--message', default=None, help='commit message')
@click.option('--output', default='',
              help='output file name with path(print to stdout if not set)')
@click.option('--launch',  is_flag=True, help='launch to Github after update repository')
@click.option('--type', type=click.Choice(['table', 'list']), default='table',
              help='output repository information in table or list')
@click.version_option(version=VERSION, prog_name='starred')
def starred(username, token, sort, repository, message, output, launch, type):
    """GitHub starred

    creating your own Awesome List used GitHub stars!

    example:
        starred --username 1132719438 --output README.md
    """
    if output.strip():
        output = output.strip()
        output_path = os.path.split(output)[0]
        if output_path and not os.path.isdir(output_path):
            os.makedirs(output_path)
        output_file = open(output, "w", encoding='utf-8')
    else:
        output_file = None

    if repository:
        if not token:
            click.secho('Error: create repository need set --token', fg='red', file=sys.stderr)
            return
        repo_file = BytesIO()
        sys.stdout = repo_file
        # do not output to file when update repository
        output_file = None
    else:
        repo_file = None

    try:
        gh = GitHub(token=token)
        stars = gh.starred_by(username)
    except ForbiddenError as e:
        click.secho('Error: talk to Github failed: {}'.format(e), fg='red', file=sys.stderr)
        return
    today = str(datetime.date.today())

    repo_dict = {}
    new_dict = {}

    # starred order
    star_order = 0
    for s in stars:
        language = s.language or 'Others'
        description = html_escape(s.description).replace('\n', '') if s.description else ''
        if language not in repo_dict:
            repo_dict[language] = []
        repo_dict[language].append([s.name, s.html_url, description.strip(), s.owner.login,
                                    s.stargazers_count, star_order])
        if language not in new_dict:
            new_dict[language] = []
        new_dict[language].append([s.name, s.html_url])
        star_order += 1

    repo_dict = OrderedDict(sorted(repo_dict.items(), key=lambda l: l[0]))
    new_dict = OrderedDict(sorted(new_dict.items(), key=lambda l: l[0]))

    # load prev repo dict and compare with new repo dict
    save_pkl = True
    cur_path = os.path.split(os.path.realpath(__file__))[0]
    repo_pkl_path = os.path.join(cur_path, 'starred-repo.pkl')
    if os.path.isfile(repo_pkl_path):
        with open(repo_pkl_path, 'rb') as file:
            old_dict = pickle.load(file, encoding='utf-8')
        if operator.eq(old_dict, new_dict):
            save_pkl = False
            if repo_file:
                click.secho('Error: starred repositories not change in {}'.format(today),
                            fg='red', file=sys.stderr)
                return

    if save_pkl:
        with open(repo_pkl_path, 'wb') as file:
            pickle.dump(new_dict, file)

    total = 0
    # sort by language and date
    if sort == 'date':
        for language in repo_dict:
            repo_dict[language] = sorted(repo_dict[language], key=lambda l: l[5])
            total += len(repo_dict[language])
    # sort by language and name
    elif sort == 'name':
        for language in repo_dict:
            repo_dict[language] = sorted(repo_dict[language], key=lambda l: l[0])
            total += len(repo_dict[language])
    # sort by language and stars
    else:
        for language in repo_dict:
            repo_dict[language] = sorted(repo_dict[language], key=lambda l: l[4], reverse=True)
            total += len(repo_dict[language])

    # desc
    count_badge_url = count_badge.format(count=total, color='green')
    date_badge_url = date_badge.format(today=today.replace('-', '--'), color='blue')
    click.echo(desc.format(badge_url=badge_url, awesome_url=awesome_url,
                           github_url=github_url, count_badge_url=count_badge_url,
                           date_badge_url=date_badge_url),
               file=output_file)

    # contents
    for language in repo_dict.keys():
        data = u'  - [{0}({2})](#{1}-{2})'.format(language, '-'.join(language.lower().split()),
                                                  len(repo_dict[language]))
        click.echo(data, file=output_file)
    click.echo('', file=output_file)

    info_dict = {}
    for language in repo_dict:
        info_dict[language] = [[index + 1,  # index
                                '[{}]({})'.format(repo[0], repo[1]),  # name with url
                                repo[2],  # description
                                repo[3],  # owner
                                repo[4]]  # stars
                               for index, repo in enumerate(repo_dict[language])]

    info_dict = OrderedDict(sorted(info_dict.items(), key=lambda l: l[0]))

    # repo
    for language in info_dict:
        count = len(info_dict[language])
        info_dict[language].insert(0, ['', 'Name', 'Description', 'Owner', 'Stars'])
        click.echo('## {} ({}) \n'.format(language.replace('#', '# #'), count), file=output_file)
        if type == 'table':
            table = GithubFlavoredMarkdownTable(info_dict[language])
            click.echo(table.table, file=output_file)
        else:
            for repo in repo_dict[language]:
                data = u'- [{}]({}) - {}'.format(*repo)
                click.echo(data, file=output_file)
        click.echo('', file=output_file)

    # license
    click.echo(license_.format(username=username), file=output_file)

    if repo_file:
        if not message:
            message = 'Add starred {}'.format(today)

        try:
            rep = gh.repository(username, repository)
            try:
                rep.file_contents('/Archives/README-{}.md'.format(today))
                click.secho('Error: already commit [/Archives/README-{}.md]'.format(today),
                            fg='red', file=sys.stderr)
            except NotFoundError:
                readme = rep.readme()
                readme.update(message, repo_file.getvalue())
                rep.create_file('Archives/README-{}.md'.format(today),
                                'Archive starred {}'.format(today), repo_file.getvalue())
        except NotFoundError:
            rep = gh.create_repository(repository, 'A curated list of my GitHub stars!')
            rep.create_file('README.md', 'Add starred {}'.format(today), repo_file.getvalue())
            rep.create_file('Archives/README-{}.md'.format(today),
                            'Archive starred {}'.format(today), repo_file.getvalue())
        if launch:
            click.launch(rep.html_url)


if __name__ == '__main__':
    starred()
