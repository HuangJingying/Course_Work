#!/usr/bin/python
# -*- coding: utf-8 -*-

import warnings
import numpy as np
warnings.filterwarnings('ignore')


def read_1(path='rRNA_1.txt'):
    """
    Get sequences from file
    :param path:
    :return: (seq, .), (seq, .)
    """
    with open(path, 'r') as f:
        s = f.read()
        s = [x for x in s.split('> se') if x]
        res = [['', ''], ['', '']]
        for i in range(2):
            si = [x for x in s[0].split() if x and x.find('1') == -1 and x.find('2') == -1]
            for j in range(len(si)):
                res[i][j % 2] += si[j]
    return res


def ans_1(match):
    """
    :param seq:
    :param match:
    :return:
    """
    stack = []
    match = list(match)
    res = match.copy()
    cur_struct = 0
    is_pop = False
    for i in range(len(match)):
        if match[i] == ')':
            if is_pop:
                is_pop = False
                cur_struct += 1
            stack.append(i)
        elif match[i] == '(':
            if not is_pop:
                is_pop = True
            res[i] = res[stack.pop()] = str(cur_struct)
    res = ''.join(res)
    return res


def read_2(path='rRNA_2.txt'):
    """
    Get sequences from file
    :param path:
    :return: (seq, .), (seq, .)
    """
    with open(path, 'r') as f:
        s = f.read()
        s = [x for x in s.split('> se') if x]
        res = ['', '']
        for i in range(2):
            res[i] = ''.join([x for x in s[i].split() if x and x.find('1') == -1 and x.find('2') == -1])
    return res


def ans_2(seq):
    """
    :param seq: sequence
    :return:
    """
    A, C, G, U = 0, 1, 2, 3
    L, S, F = 0, 1, 2
    dic = {'A': A, 'C': C, 'G': G, 'U': U}
    log_p1 = np.log([0.3932222718, 0.1535404400, 0.2070351532, 0.2462021350])
    log_p2 = np.log([[0.0020940761, 0.0023119568, 0.0021182850, 0.1853802019], [0.0023845837, 0.0005810153, 0.2432759581, 0.0012346576], [0.0018035684 , 0.2548115332, 0.0011257172, 0.0591062048], [0.1805989300, 0.0012467621,  0.0580773235, 0.0038492265]])
    log_La = np.log(0.9001224650)
    log_vaFa = np.log([0.0998775350, 0, 0.7631163066])
    log_vLS = np.log([0, 0.8885212264, 0.2368836934])
    log_SL = np.log(0.1114787736)

    seq = np.array([dic[x] for x in list(seq)], dtype=np.int)
    seq_len = len(seq)

    y = -np.inf * np.ones((seq_len, seq_len, 3))
    # trace back [condition, k(optional)]
    t = 3 * np.ones((seq_len, seq_len, 3, 2), dtype=np.int)
    # initialize
    for i in range(seq_len):
        y[i, i, L] = log_La + log_p1[seq[i]]
        y[i, i, S] = y[i, i, L] + log_SL
        t[i, i, S, 0] = 2
    # dynamic programing
    for d in range(1, seq_len):
        for i in range(seq_len - d):
            j = i + d
            # L
            y[i, j, L] = y[i + 1, j - 1, F] + log_vaFa[L] + log_p2[seq[i], seq[j]]
            if y[i, j, L] != -np.inf:
                t[i, j, L, 0] = 1
            # S
            s0 = np.array([y[i, k, L] + y[k + 1, j, S] + log_vLS[S] for k in range(i, j)])
            k_max = s0.argmax()
            s0_max = s0[k_max]
            s2 = y[i, j, L] + log_SL
            if s0_max == -np.inf and s2 == -np.inf:
                y[i, j, S] = -np.inf
            elif s0_max >= s2:
                y[i, j, S] = s0_max
                t[i, j, S] = [0, k_max + i]
            elif s0_max < s2:
                y[i, j, S] = s2
                t[i, j, S, 0] = 2
            # F
            f0 = np.array([y[i, k, L] + y[k + 1, j, S] + log_vLS[F] for k in range(i, j)])
            k_max = f0.argmax()
            f0_max = f0[k_max]
            f1 = y[i + 1, j - 1, F] + log_vaFa[F] + log_p2[seq[i], seq[j]]
            if f0_max == -np.inf and f1 == -np.inf:
                y[i, j, F] = -np.inf
            elif f0_max >= f1:
                y[i, j, F] = f0_max
                t[i, j, F] = [0, k_max + i]
            elif f0_max < f1:
                y[i, j, F] = f1
                t[i, j, F, 0] = 1
    # trace back
    i, j = 0, seq_len - 1
    state = np.argmax(y[i, j])
    stack = []
    res = ['.'] * seq_len
    while True:
        if t[i, j, state, 0] == 0:
            stack.append((t[i, j, state, 1] + 1, j, S))
            i, j, state = i, t[i, j, state, 1], L
        elif t[i, j, state, 0] == 1:
            res[i], res[j] = ')', '('
            i, j, state = i + 1, j - 1, F
        elif t[i, j, state, 0] == 2:
            i, j, state = i, j, L
        elif t[i, j, state, 0] == 3:
            if len(stack) > 0:
                i, j, state = stack.pop()
            else:
                break
    return ''.join(res)


def main():

    # question 1
    seq_11, seq_12 = read_1()
    print(ans_1(seq_11[1]))
    print(ans_1(seq_12[1]))

    # question 2
    seq_21, seq_22 = read_2()
    print(ans_2(seq_21))
    print(ans_2(seq_22))


if __name__ == '__main__':
    main()
