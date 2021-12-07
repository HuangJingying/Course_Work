#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import numpy as np


SOURCE_FILE = 'Wuhan-Hu-1.fasta'
TARGET_FILE = 'MD-MDH-0232.fasta'
MATCH_FILE = 'match.out'
TRANSCRIPT_FILE = 'transcript.out'
NUM_FILE = 'num.out'
PUNISH_GRADE = 2
LEFT = 0
UP = 1
LEFTUP = 2
LINE_LENGTH = 60


def get_seq(file):
    """
    Get sequence from fasta file
    :param file: (String) file path
    :return: (String) sequence
    """

    seq = ''
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            line = f.readline()[:-1]
            seq += line

    return seq


def get_dires(s_seq, t_seq):
    """
    Compute the D table and direction table
    :return: (ndarray) Dtable, (ndarray) direction_table
    """


    s_len = len(s_seq)
    t_len = len(t_seq)

    # each line of the Dtable
    Dtable = np.zeros((s_len, t_len), dtype=np.uint32)
    Dtable[0, :] = PUNISH_GRADE * np.arange(t_len, dtype=np.uint32)
    Dtable[:, 0] = PUNISH_GRADE * np.arange(s_len, dtype=np.uint32)
    dires = np.zeros((s_len, t_len), dtype=np.uint8)
    dires[0, :] = LEFT
    dires[:, 0] = UP

    # calculate direction table
    for i in range(1, s_len):
        for j in range(1, t_len):
            Dvalues = np.array([Dtable[i, j - 1] + PUNISH_GRADE,
                                Dtable[i - 1, j] + PUNISH_GRADE,
                                Dtable[i - 1, j - 1] + int(s_seq[i] != t_seq[j])])
            dires[i, j] = np.argmin(Dvalues)
            Dtable[i, j] = Dvalues[dires[i, j]]

    return Dtable, dires


def get_res(s_seq, t_seq, dires):
    """
    Get edit transcript between two seq
    :param s_seq: source sequence
    :param t_seq: target sequence
    :param dires: direction table
    :return: (String) edit transcript
    """

    res = ''
    res_s = ''
    res_t = ''
    ci = len(s_seq) - 1
    cj = len(t_seq) - 1

    while ci != 0 or cj != 0:
        if dires[ci, cj] == LEFT:
            res = 'D' + res
            res_s = '-' + res_s
            res_t = t_seq[cj] + res_t
            cj -= 1
        elif dires[ci, cj] == UP:
            res = 'I' + res
            res_s = s_seq[ci] + res_s
            res_t = '-' + res_t
            ci -= 1
        else:
            if s_seq[ci] == t_seq[cj]:
                res = 'M' + res
            else:
                res = 'R' + res
            res_s = s_seq[ci] + res_s
            res_t = t_seq[cj] + res_t
            ci -= 1
            cj -= 1

    count = np.array([0, LINE_LENGTH])
    with open(MATCH_FILE, 'w') as f:
        for i in range(int(len(res) / LINE_LENGTH) + 1):
            s = res_s[count[0]: count[1]] + '\n' + res[count[0]: count[1]] + '\n' + res_t[count[0]: count[1]] + '\n'
            f.write(s)
            count += LINE_LENGTH
            if count[1] > len(res):
                count[1] = -1

    count = np.array([0, LINE_LENGTH])
    with open(TRANSCRIPT_FILE, 'w') as f:
        for i in range(int(len(res) / LINE_LENGTH) + 1):
            s = res[count[0]: count[1]] + '\n'
            f.write(s)
            count += LINE_LENGTH
            if count[1] > len(res):
                count[1] = -1

    with open(NUM_FILE, 'w') as f:
        f.write('D[100, 100]={}\n'.format(Dtable[100, 100]))
        f.write('D[1000, 1000]={}\n'.format(Dtable[1000, 1000]))
        f.write('D[10000, 10000]={}\n'.format(Dtable[10000, 10000]))
        f.write('D[L_1, L_2]={}\n'.format(Dtable[-1, -1]))

    return res


if __name__ == '__main__':

    # input
    ti = time.time()
    s_seq = get_seq(SOURCE_FILE)
    t_seq = get_seq(TARGET_FILE)
    print('I time: {}'.format(time.time() - ti))

    # calculate table
    ti = time.time()
    Dtable, dires = get_dires(s_seq, t_seq)
    print('Table time: {}'.format(time.time() - ti))

    # get result
    ti = time.time()
    res = get_res(s_seq, t_seq, dires)
    print('Result time: {}'.format(time.time() - ti))
