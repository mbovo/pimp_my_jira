# pimp_my_jira
# Copyright(C) 2024 Manuel Bovo

# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY
# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import click
import yaml
import os
from rich import print

class CMD:
    CREATE = 'echo jira issue create'
    NO_INPUT = '--no-input'
    EXTRA = ''

class FLAGS:
    PROJECT = '-p'
    PARENT = '-P'
    TYPE = '-t'
    SUMMARY = '-s'
    BODY = '-b'
    COMPONENT = '-C'
    LABEL = '-l'
    VALID_TYPES = ['task', 'story', 'bug','sub-task']

@click.command()
@click.option('-f', "--ifile", prompt='Input yaml file', help='The input file to be processed', type=click.Path(exists=True, readable=True))
@click.option('-n', "--dry-run", is_flag=True, help='Dry run the command')
def main(ifile:str, dry_run:bool):

    if not check_jira():
        print('Jira binary not found, please install it (https://github.com/ankitpokhrel/jira-cli) and make sure it is in the PATH')
        exit(1)

    content = {}
    with open(ifile) as f:
        content = yaml.safe_load(f.read())

    commands=parse(content)

    if dry_run:
        print('Dry run, no commands executed')
        print(commands)
    else:
        for cmd in commands:
            os.system(cmd)

def check_jira()->bool:
    ret = os.system('which jira')
    ver = os.system('jira version')
    return ret & ver == 0

def parse(content: dict)-> list[str]:

    if 'project' not in content:
      print('No project found, missing key: project')
      return []

    if 'type' not in content:
        print('No default type found, missing key: type')
        return []

    if 'component' not in content:
        print('No default component found, missing key: component')
        return []

    if 'issues' not in content:
        print('No issues found, missing key: issues')
        return []

    count = len(content['issues'])
    print (f'Loaded {count} issues to process')

    ret = []

    prj = content['project']
    gtype = content['type']
    gcomponent = content['component']

    cmd = CMD.CREATE
    for issue in content['issues']:
        cmd = CMD.CREATE
        cmd += f' {FLAGS.PROJECT}{prj}'
        if 'parent' in issue:
            cmd += f' {FLAGS.PARENT}"{issue["parent"]}"'
        if 'type' in issue:
            if issue["type"].lower() not in FLAGS.VALID_TYPES:
                print(f'Invalid type: {issue["type"]}')
                continue
            cmd += f' {FLAGS.TYPE}"{issue["type"]}"'
        else:
            cmd += f' {FLAGS.TYPE}"{gtype}"'
        if 'summary' in issue:
            cmd += f' {FLAGS.SUMMARY}"{issue["summary"]}"'
        else:
            print('No summary found, missing key: summary')
            continue
        if 'body' in issue:
            cmd += f' {FLAGS.BODY}"{issue["body"]}"'
        else:
            print('No body found, missing key: body')
            continue
        if 'component' in issue:
            cmd += f' {FLAGS.COMPONENT}"{issue["component"]}"'
        elif 'components' not in issue:
            cmd += f' {FLAGS.COMPONENT}"{gcomponent}"'
        if 'label' in issue:
            cmd += f' {FLAGS.LABEL}"{issue["label"]}"'
        if 'components' in issue:
            cmpStr = ",".join(issue['components'])
            cmd += f' {FLAGS.COMPONENT}"{cmpStr}"'
        if 'labels' in issue:
            lblStr = ",".join(issue['labels'])
            cmd += f' {FLAGS.LABEL}"{lblStr}"'
        cmd += CMD.NO_INPUT
        cmd += CMD.EXTRA
        ret += [cmd]

    return ret