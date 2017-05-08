#!/usr/local/bin/python3

import subprocess
import json
from pprint import pprint
import cloc
import os
import shutil
from tabulate import tabulate
import argparse

def run_cloc(name, url, working_dir):
    #clone into tmp
    os.chdir(working_dir)
    subprocess.call(['git', 'clone', url])
    os.chdir(name)
    repo_out = cloc.cloc_repo()

    os.chdir('../..')
    shutil.rmtree(working_dir + os.sep + name)  #clean up as we go along
    return repo_out

def cloc_servo(working_dir):
    url = 'https://github.com/servo/servo.git'
    os.chdir(working_dir)
    if not os.path.exists('servo'):
        subprocess.call(['git', 'clone', url])
    os.chdir('servo' + os.sep + 'components')
    components = []
    for component in os.listdir(os.getcwd()):
        os.chdir(component)
        comp_out = cloc.cloc_repo()
        comp_out.insert(0, "servo-"+component)
        os.chdir('..')
        components.append(comp_out)
    os.chdir('../../..')
    print(os.getcwd())
    return components


def main():
    parser = argparse.ArgumentParser(description='cloc for rustlang')
    parser.add_argument('--servo', action='store_true', help='include servo in analysis')
    args = parser.parse_args()
    cmd = ['curl', 'https://api.github.com/search/repositories?q=language:rust+user:servo&sort=stars', '-o', 'crawl.json']
    subprocess.call(cmd)

    output = []

    with open('crawl.json') as data_file:
        data = json.load(data_file)

    #pprint(data)
    items = data['items']

    working_dir = 'cloc_tmp'
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    for x in items:
        repo_out = run_cloc(x['name'], x['clone_url'], working_dir)
        repo_out.insert(0,x['name'])
        output.append(repo_out)
    # servo isn't listed with language:rust
    if args.servo:
        output+=cloc_servo(working_dir)


    shutil.rmtree(working_dir)   #clean up
    headers = ["files", "blank", "comment", "code", "unsafe", "%unsafe", "fns", "unsafe fns", "%unsafe fns"]
    print(tabulate(output,headers=headers))
	
if __name__ == "__main__":
    main()
