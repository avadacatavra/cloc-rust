#!/usr/local/bin/python3
#FIXME

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

# a bit hacky, should probs be generalized
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
    return components

def cloc_rust(working_dir):
    url = 'https://github.com/rust-lang/rust'
    os.chdir(working_dir)
    if not os.path.exists('rust'):
        subprocess.call(['git', 'clone', url])
    os.chdir('rust/src')
    components = []
    for component in os.listdir(os.getcwd()):
        if os.path.isdir(component):
            os.chdir(component)
            comp_out = cloc.cloc_repo()
            comp_out.insert(0, "rust-"+component)
            os.chdir('..')
            components.append(comp_out)
    os.chdir('../../..')
    return components



def main():
    parser = argparse.ArgumentParser(description='cloc for rustlang')
    parser.add_argument('--servo', action='store_true', help='include servo in analysis')
    parser.add_argument('--rust', action='store_true', help='include rust in analysis')
    parser.add_argument('--dir', action='store', help='analyze a particular existing directory. skips github')
    parser.add_argument('--keep', action='store_true', help='keep temporary directory (will keep servo/rust too)')
    args = parser.parse_args()

    cmd = ['curl', 'https://api.github.com/search/repositories?q=language:rust+user:servo&sort=stars', '-o', 'crawl.json']
    subprocess.call(cmd)

    output = []

    #with open('crawl.json') as data_file:
    #    data = json.load(data_file)

    #items = data['items']

    working_dir = 'cloc_tmp'
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    #for x in items:
    #    repo_out = run_cloc(x['name'], x['clone_url'], working_dir)
    #    repo_out.insert(0,x['name'])
    #    output.append(repo_out)
    # servo isn't listed with language:rust
    if args.servo:
        output += cloc_servo(working_dir)
    if args.rust:
        output += cloc_rust(working_dir)

    if not args.keep:
        shutil.rmtree(working_dir)   #clean up
    headers = ["files", "blank", "comment", "code", "unsafe", "%unsafe", "fns", "unsafe fns", "%unsafe fns", "panics"]
    print(tabulate(output,headers=headers))
	
if __name__ == "__main__":
    main()
