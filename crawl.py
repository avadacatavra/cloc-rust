#!/usr/local/bin/python3

import subprocess
import json
from pprint import pprint
import cloc
import os
import shutil
from tabulate import tabulate

def run_cloc(name, url, working_dir):
    #clone into tmp
    os.chdir(working_dir)
    subprocess.call(['git', 'clone', url])
    os.chdir(name)
    repo_out = cloc.cloc_repo()

    os.chdir('../..')
    shutil.rmtree(working_dir + os.sep + name)
    return repo_out

def main():
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

    os.rmdir(working_dir)   #clean up
    headers = ["files", "blank", "comment", "code", "unsafe", "%unsafe", "fns", "unsafe fns", "%unsafe fns"]
    print(tabulate(output,headers=headers))
	
if __name__ == "__main__":
    main()
