import re
import os
import sys
import readline
from nltk.corpus import stopwords

class bcolors:
    CRED    = '\33[31m'
    OKCYAN = '\033[96m'
    CBLINK    = '\33[5m'
    OKGREEN = '\033[92m'
    CYELLOW = '\33[93m'
    ENDC = '\033[0m'
    DIM = '\033[90m'
    OKBLUE = '\033[94m'
    MAGENTA = '\033[35m'

def moveup(n):
    for i in range(n):
        print("\033[F\033[F")
        sys.stdout.write("\033[K")
    return

def startdim(end='\n', flush=False):
    print(f"{bcolors.DIM}", end=end, flush=flush)

def stopdim(end='\n', flush=False):
    print(f"{bcolors.ENDC}", end=end, flush=flush)

startdim_dim_flush = lambda: startdim(end='', flush=True)
stopdim_dim_flush = lambda: stopdim(end='', flush=True)

def prntc(print_statement, flag=True, end='\n', dim=False, flush=False):    
    if flag:
        if dim:
            print_statement = f"{bcolors.DIM}" + print_statement + f"{bcolors.ENDC}"
        print(print_statement, end=end, flush=flush)
    return

def remove_stopwords(list_of_string):
    stop_words = set(stopwords.words('english'))
    valid_c = []
    for w in list_of_string:
        if w not in stop_words:
            valid_c.append(w)
    return valid_c

def cleanup_str(single_string_of_words):
    list_words = re.findall(r'\S+', single_string_of_words)
    valid_c = remove_stopwords(list_words)
    return ' '.join(valid_c)

def runcdcmd(s, prevpath):
    path_changed = False
    str_cleaned = re.sub('\s+',' ',s.strip())
    str_cleaned_split = str_cleaned.split()
    l = len(str_cleaned_split)    
    if l>=2:
        cmd, path = str_cleaned_split[:2]
    elif l==1:
        cmd,path = str_cleaned_split[0], '~'
    else:
        return path_changed, str_cleaned
    
    if cmd == 'cd':
        if path == '-':
            path = prevpath
        os.chdir(os.path.expanduser(path))
        path_changed = True

    return path_changed, str_cleaned

def choose_param_value(list_of_options, currentval, DIMCOLOR=False, VANISH=False):
    print_lines_count = 0
    
    if VANISH:
        DIMCOLOR = False

    if DIMCOLOR:
        print(f"{bcolors.DIM}", flush=True)
        print_lines_count += 1
        
    if currentval not in list_of_options:
        print('currentval : '+repr(currentval))        
        print('list_of_options : ')
        print(list_of_options)
        raise Exception('Current item is not available in list of options.')
    
    match_current_idx = [ii for ii,option in enumerate(list_of_options) if currentval==option][0]
    
    print('Available options :')
    print_lines_count += 1
    for ID, item in enumerate(list_of_options):
        if ID == match_current_idx:    
            print('*['+str(ID)+'] : '+repr(item))
        else:
            print(' ['+str(ID)+'] : '+repr(item))
        print_lines_count += 1
    
    param_changed = False
    newval = currentval

    option_str = input('Enter choice ID : ')
    print_lines_count += 1
    valid_options_ID = list(range(len(list_of_options)))
    valid_options = list(map(str, valid_options_ID))
    if option_str not in valid_options:
        print('Error : ID needs to be one of - ' + str(valid_options_ID))
        print_lines_count += 1
    else:
        optionID = int(option_str)
        if match_current_idx == optionID:
            print('Warning : Same ID as current option. Not changing.')
            print_lines_count += 1
        else: # Changing param
            newval = list_of_options[optionID]
            param_changed = True

    if DIMCOLOR:
        print(f"{bcolors.ENDC}", flush=True)
        print_lines_count += 1

    if VANISH:       
        moveup(print_lines_count)

    return newval, param_changed

def getcmd(cmd, joined_lines):
    lines_split = joined_lines.split('\n')
    out_switch = None
    sug_cmd = ""
    for line in lines_split:
        line_cleaned = line.strip()
        if len(line_cleaned)>0:
            if line_cleaned[0] == '-':
                line_cleaned_split = line_cleaned.split()
                out_switch = line_cleaned_split[0]
                out_switch = out_switch.split(',')[0] # stop at first comma
                sug_cmd = cmd + ' ' + out_switch
                break    
    return sug_cmd

def rlinput(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)  # or raw_input in Python 2
    finally:
        readline.set_startup_hook()
    return
