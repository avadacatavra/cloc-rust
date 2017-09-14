#!/usr/local/bin/python3
#FIXME

import re
import os

#if there's no unsafe, then you're good. can probably save some time with that

#if test tile is a Cargo file, then do some dependency analysis

#naive solution, analyze file line by line

#omg this is awful FIXME
num_unsafe = 0
unsafe_fns = 0
total_fns = 0
blank = 0
comment = 0
files = 0
code = 0
panics = 0

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
    global panics

    files += 1
    
    regex = re.compile('^//|^\s/\*|^\s\*|^\s\*/')
    unsafe_regex = re.compile('.*unsafe\s*\{')
    flag = False
    literal_flag = False    #handles ```...```
    brackets = []   #TODO probably don't actually need a stack


    for line in open(filename).readlines():
    
        # skip comment lines
        if re.match(regex, line):
            comment += 1
            continue
        if "```" in line:
            if literal_flag == False:
                comment += 1
                literal_flag = True
            else:   #end comment block
                comment += 1
                literal_flag = False
            continue
        if literal_flag == True:
            comment += 1
            continue
        # skip blank lines
        if len(line.strip()) == 0:
            blank += 1
            continue

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
        if re.match('\s*unsafe impl.*for.*', line):
            num_unsafe += 1
            #TODO is this always a one liner?
        if re.match('\s*fn\s+[a-zA-Z_]*', line):
            total_fns += 1
            #FIXME pretty hacky...
            if 'unsafe ' in line:
                flag = True
                brackets.append('{')
                unsafe_fns += 1
        elif re.match("\s*unsafe\s*\{.*\}", line):   #match one liner
            num_unsafe += 1
        elif re.match(unsafe_regex, line):
            flag = True
            brackets.append('{')
        if 'panic!' in line:
            panics += 1

#runs over cwd
def cloc_repo():
    if os.getcwd() == ".git":
       return 
    for subdir, dirs, files in os.walk(os.getcwd()):
        if 'test' in subdir:
            continue
        for f in files:
            if f == "diagnostics.rs":
               continue 
            elif f.endswith('.rs'):
                cloc_file(subdir + os.sep + f)
    results = summarize()
    clear_counts()
    return results

#literally the same as cloc_repo, but you pass the directory
# can't remember why i wrote cloc_repo the way i did so keeping it for now
# also pass a flag to indicate if filewise granularity is desired
def cloc_dir(crate_dir, verbose):
    # shouldn't be necessary anymore
    #if os.getcwd() == ".git":
    #   return 
    for subdir, dirs, files in os.walk(crate_dir):
        if 'test' in subdir:
            continue
        for f in files:
            if f == "diagnostics.rs":
               continue 
            elif f.endswith('.rs'):
                cloc_file(subdir + os.sep + f)
    results = summarize()
    clear_counts()
    return results


def clear_counts():
    global num_unsafe
    global unsafe_fns
    global total_fns
    global blank
    global comment
    global files
    global code
    global panics

    num_unsafe = 0
    unsafe_fns = 0
    total_fns = 0
    blank = 0
    comment = 0
    files = 0
    code = 0
    panics = 0


def summarize():
    try:
        unsafe_ratio = (num_unsafe/code)*100
    except ZeroDivisionError:
        unsafe_ratio = 0
    try:
        fn_ratio = (unsafe_fns/total_fns)*100
    except ZeroDivisionError:
        fn_ratio = 0
    return [files, blank, comment, code, num_unsafe, unsafe_ratio, total_fns, unsafe_fns, fn_ratio, panics]

