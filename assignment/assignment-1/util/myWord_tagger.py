# myWordTagger.py
# Author: Thura Aung
# 9th December, 2023
# Data preparation for word segmentation CRF model training
# Ref: Win Pa Pa, Ye Kyaw Thu, Andrew Finch, Eiichiro Sumita, "Word Boundary Identification for Myanmar Text Using Conditional Random Fields", In Proceedings of the Ninth International Conference on Genetic and Evolutionary Computing (ICGEC 2015), August 26-28, 2015, Yangon, Myanmar, pp. 447-456.

import re
import sys  # <-- FIX 1: Imported sys module
import argparse

parser = argparse.ArgumentParser(description='Data preparation for word segmentation')
parser.add_argument('-i', '--input', type=str, help='input file', required=True)
parser.add_argument('-m', '--mode', type=str, default=r's', help='s for syllable and c for character tagging', required=False)
parser.add_argument('-n', '--nTag', type=int, default=4, help='Number of Tags {2, 3, 4}', required=False)
args = parser.parse_args()

inputFile = getattr(args, 'input')
mode = getattr(args, 'mode')
n = getattr(args, 'nTag')

myConsonant = r"က-အ"
enChar = r"a-zA-Z0-9"
otherChar = r"ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s"
ssSymbol = r'္'
aThat = r'်'

# Regular expression pattern for Myanmar syllable breaking
BreakPattern = re.compile(r"((?<!" + ssSymbol + r")["+ myConsonant + r"](?![" + aThat + ssSymbol + r"])" + r"|[" + enChar + otherChar + r"])")

def segment_into_syllables(text):
    data = ""
    line = re.sub(BreakPattern, " "+r"\1", text)
    data += line
    return data.split()

def make_word_ls(line, chk='s'):
    word_ls = []
    if chk == 's':
        words = line.split()
        for word in words:
            word_ls.append(list(segment_into_syllables(word)))
    else:
        word_ls = [list(c) for c in line.split()]
    return word_ls
    
def two_tagger(word_ls):
    for word in word_ls:
        n_of_element = len(word)
        if n_of_element == 1:
            print(f"{word[0]}\t|")
        else:
            for i in range(0, n_of_element-1):
                print(f"{word[i]}\t-")
            print(f"{word[n_of_element-1]}\t|")
            
def three_tagger(word_ls):
    for word in word_ls:
        n_of_element = len(word)
        if n_of_element >= 3:
            print(f"{word[0]}\t<")
            for i in range(1, n_of_element-1):
                print(f"{word[i]}\t-")
            print(f"{word[n_of_element-1]}\t|")
        elif n_of_element == 2:
            print(f"{word[0]}\t<")
            print(f"{word[1]}\t|")
        else:
            print(f"{word[0]}\t|")
            
def four_tagger(word_ls):
    for word in word_ls:
        n_of_element = len(word)
        if n_of_element >= 4:
            print(f"{word[0]}\t<")
            for i in range(1, n_of_element-2):
                print(f"{word[i]}\t-")
            print(f"{word[n_of_element-2]}\t>")
            print(f"{word[n_of_element-1]}\t|")
        elif n_of_element == 3:
            print(f"{word[0]}\t<")
            print(f"{word[1]}\t>")
            print(f"{word[2]}\t|")
        elif n_of_element == 2:
            print(f"{word[0]}\t<")
            print(f"{word[1]}\t|")
        else:
            print(f"{word[0]}\t|")
            
try:
    with open(inputFile, 'r') as file:
        # <-- FIX 2: Used proper if/elif structure so n=3 doesn't fall through to else
        if n == 2:
            for line in file:
                two_tagger(make_word_ls(line, mode))
                print()
        elif n == 3:
            for line in file:
                three_tagger(make_word_ls(line, mode))
                print()
        elif n == 4:
            for line in file:
                four_tagger(make_word_ls(line, mode))
                print()
        else:
            print("Only 2 to 4 accepted.", file=sys.stderr)
except FileNotFoundError:
    print(f"File '{inputFile}' not found.", file=sys.stderr)  # <-- FIX 3: Changed file_path to inputFile & redirected to stderr
except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)  # <-- FIX 4: Redirected general exceptions to stderr