#!/usr/local/bin/python3

import re
import os

#if there's no unsafe, then you're good. can probably save some time with that

#if test tile is a Cargo file, then do some dependency analysis

#naive solution, analyze file line by line

num_unsafe = 0
unsafe_fns = 0
total_fns = 0
blank = 0
comment = 0
files = 0
code = 0

#run over a directory
# skip files under test anything
# only analyze .rs files for now

def cloc_file(filename):
    global num_unsafe
    global unsafe_fns
    global total_fns
    global blank
    global comment
    global files
    global code

    files += 1
    
    regex = re.compile('^//|^\s/\*|^\s\*|^\s\*/')
    flag = False
    brackets = []   #TODO probably don't actually need a stack


    for line in open(filename).readlines():
    
        # skip comment lines
        if re.match(regex, line):
            comment += 1
        # skip blank lines
        if len(line.strip()) == 0:
            blank += 1
        code += 1
        if flag == True:
            if '{' in line:         #track brackets so you don't terminate count early
                brackets.append('{')
            if '}' in line:         #use if instead of elif in case of one line {...}
                brackets.pop()
            if len(brackets) == 0:  #we've exited the unsafe area
                flag = False
            else:
                num_unsafe += 1
        if 'fn' in line:
            total_fns += 1
            if 'unsafe' in line:
                flag = True
                brackets.append('{')
                unsafe_fns += 1
        elif 'unsafe' in line:
            flag = True
            brackets.append('{')

#runs over cwd
def cloc_repo():
    for subdir, dirs, files in os.walk(os.getcwd()):
        if 'test' in subdir:
            continue
        for f in files:
            if f.endswith('.rs'):
                cloc_file(subdir + os.sep + f)
    return summarize()

def summarize():
    unsafe_ratio = num_unsafe/code
    fn_ratio = unsafe_fns/total_fns
    return [files, blank, comment, code, num_unsafe, unsafe_ratio, total_fns, unsafe_fns, fn_ratio]

