#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 2020

@author: jingyinghuang
"""


def get_seq(file):
    """
    Get structure (dot-parantheses format) from fasta file,eg:
    > seqence1:
    GAGGAAAGUCCCGCCUCCAGAUCAAGGGAAGUCCCGCGA
    .....))).))))).....))))).))))))))))....
    :param file: (String) file path
    :return: (String) structure sequence
    """
    sequence = ""
    strings = [".", "(", ")"]
    with open(file, 'r') as f:
        line = f.readline()
        i = 0
        while line != '':  # The EOF char is an empty string
            if any(STRING in strings for STRING in line):
                # print(line, end='')
                seq = line.strip()
                sequence += seq  # write seq line>>until next anno line
            line = f.readline()
    return sequence


def anti_seq(seq):
    """
    Get reverse sequence
    :param file: (String) sequence
    :return: (String) reverse sequence
    """
    return seq[::-1]


def toPairs(struc):
    """
     find pairs of structure
     :param file: (String) sequence
     :return: (String) dict, -1:no pairs
     """
    stack = []
    pairs = {}
    for i, s in enumerate(struc):
        pairs[i] = -1  # init , -1:no pairs
        if s == "(":
            stack.append(i)
        elif s == ")":
            pair = stack.pop()
            pairs[pair] = i
            pairs[i] = pair
    return pairs


'''
Alphabet
L : paired, 5' end  (
R : paired, 3' end  )
H : hairpin loop
T : internal loop
B : bulge loop
M : multiloop
E : external region(unpaired) RNA
'''


def parse(structure):
    """
     parse secondary structure
     :param file: (String) structure sequence
     :return: (String) structure pasre

     reference: https://github.com/morrislab/rnascan/tree/master/scripts
     """
    L = len(structure)
    pairs = toPairs(structure)
    # print(pairs)
    # for i in range(L):
    #     print(pairs[i])
    # parae
    i = 0
    alph = ""
    annot = ""

    # external bases on the 5 ' end
    for i in range(L):
        if structure[i] == '.':
            alph += "E";  # external unpaired region
        else:
            break
    # print("i", i)
    # for j in range(i, L):
    j = i
    while(j<L):
        if structure[j] == '.':
            k = j - 1

            while structure[k] == '.':  # search for the nearest parantheses on the left side of this dot
                k -= 1

            m = j + 1
            while m < L and structure[m] == '.':  # search for the nearest parantheses on the right side of this dot
                m += 1

            if m == L:
                annot = "E"
            elif structure[k] == '(' and structure[m] == ')':
                annot = "H"  # hairpin loop

            elif structure[k] == ')' and structure[m] == ')':  # bulge or interior or multiloop!
                if pairs[m] + 1 == pairs[k]:  # m and k's paired bases are consecutive so this "." belongs to a bulge
                    annot = "B"  # hairpin loop
                else:
                    annot = "N"  # interior loop
            elif structure[k] == ')' and structure[m] == '(':
                foundEnclosingPair = False
                # check if there's any i-j pair where i<k and j>m
                for pos in range(k):
                    if pairs[pos] > m:
                        foundEnclosingPair = True
                if foundEnclosingPair:
                    annot = "M"  # multiloop
                else:
                    annot = "E"

            elif structure[k] == '(' and structure[m] == '(':  # can be multiloop, interior loop or bulge
                if pairs[m] + 1 == pairs[k]:  # m and k's paired bases are consecutive so this "." belongs to a bulge
                    annot = "B"
                else:
                    annot = "N"  # not known for now, we'll analyze these again below

            while (j < m):  # the neighbor dots belong to the same annotation
                alph += annot
                j += 1

            if m < L:
                if (structure[m] == '('):
                    alph += "L"  # now j points to a paired base
                elif (structure[m] == ')'):
                    alph += "R"
        else:
            if (structure[j] == '('):
                alph += "L"
            elif structure[j] == ')':
                alph += "R"
        j+=1
    # analyze multiloop
    Mindices = {}
    for index, num in enumerate(structure):
        Mindices[index] = 0
    for j in range(L):
        if (alph[j] == 'R'):
            k = j
            if alph[k + 1] == 'L' or alph[k + 1] == 'M':  # find "switches" from R to L, RM * L
                m = k + 1

                while structure[m] == '.':  # find end of "switch"
                    m += 1

                s = pairs[k] - 1  # index at which multi loop starts
                e = pairs[m] + 1  # index at which multi loop ends
                while s >= 0 and structure[s] == '.':  # replace any loop left of the multiloop region with M
                    if (alph[s] == 'N'):
                        Mindices[s] = 1
                    s -= 1
                while e < L and structure[e] == '.':  # creplace any loop right of the multiloop region with M
                    if (alph[e] == 'N'):
                        Mindices[e] = 1
                    e += 1
    # print(Mindices)
    alph_list=list(alph) # in python str can not replace a character in a specific pos
    for j in range(L):  # get rid of "N"s
        if alph[j] == 'N':
            # print(j, Mindices[j],alph[j])
            if Mindices[j] == 1:
                alph_list[j] = 'M'
            else:
                alph_list[j] = 'T'


    return "".join(alph_list)


def print_seq(anti_s, l):
    """
    l:length of each line
     """
    length = len(anti_s)
    for i in range(int(length // l) + 1):
        # print(i,l*i+l)
        if (l * i + l) < length:
            print(anti_s[l * i:l * i + l])
        else:
            print(anti_s[l * i:])


if __name__ == '__main__':
    # read
    structure = get_seq("./rRNA_1_1.txt")
    anti_s = anti_seq(structure)
    # print
    # print_seq(anti_s, 40)
    # parse
    print(">seq1")
    print_seq(parse(anti_s),40)

    structure = get_seq("./rRNA_1_2.txt")
    anti_s = anti_seq(structure)
    print(">seq2")
    print_seq(parse(anti_s),40)
