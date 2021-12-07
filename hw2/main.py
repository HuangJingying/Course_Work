#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
======================
@author: Jaron
@time: 2020/11/25:16:08
@email: fjjth98@163.com
@description: implement Profile HMM model
======================
"""

import warnings
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(formatter={'float': '{: 0.8f}'.format})
warnings.filterwarnings("ignore")

SEQUENCE1 = 'VAFTEKQDALVSSSFEAFKANIPQYSVVFYTSILEKAPAAKDLFSFLANGVDPTNPKLTGHAEKLFALVRDSAGQLKASGTVVADAALGSVHAQKAVTDPQFVVVKEALLKTIKAAVGDKWSDELSRAWEVAYDELAAAIKKA'

SEQUENCE2 = 'CGVGFIAAIDGKPRRSVVEKGIEALKAVWHRGAVDADGKTGDGAGIHVAVPQKFFKDHVKVIGHRAPDNKLAVGQVFLPRISLDAQEACRCIVETEILAFGYYIYGWRQVPINVDIIGEKANATRPEIEQIIVGNNKGVSDEQFELDLYIIRRRIEKAVKGEQINDFYICSLSARSIIYKGMFLAEQLTTFYPDLLDERFESDFAIYHQRYSTNTFPTWPLAQPFRMLAHNGEINTVKGNVNWMKAHETRMEHPAFGTHMQDLKPVIGVGLSDSGSLDTVFEVMVRAGRTAPMVKMMLVPQALTSSQTTPDNHKALIQYCNSVMEPWDGPAALAMTDGRWVVGGMDRNGLRPMRYTITTDGLIIGGSETGMVKIDETQVIEKGRLGPGEMIAVDLQSGKLYRDRELKDHLATLKPWDKWVQN'

# cannot be changed without error, because MID all are indexes
M = 0
I = 1
D = 2
T = 3   # termination


def log_sum_exp(f, a):
    """
    calculate log(a^T.exp(f))
    :param f:
    :param a:
    :return:
    """

    fc = []
    ac = []
    for i in range(len(f)):
        if f[i] != -np.inf and a[i] != 0:
            fc.append(f[i])
            ac.append(a[i])
    if len(fc) == 0:
        return -np.inf
    fc = np.array(fc)
    ac = np.array(ac)
    fm = fc.max()
    fc -= fm
    return fm + np.log(ac.dot(np.exp(fc)))


def get_malign(path):
    """
    Get the multisequence align results from file
    :param path:
    :return: values(MSA results)
    """

    with open(path, 'r') as f:
        s = f.readlines()[3:]
        prefixes = []
        for ss in s:
            i = ss.find(' ')
            if i > 0:
                prefix = ss[: i]
                if prefix not in prefixes:
                    prefixes.append(prefix)
        msa_dict = dict.fromkeys(prefixes, '')
        for pre in prefixes:
            for ss in s:
                if pre in ss:
                    msa_dict[pre] += ss[ss.rfind(' ') + 1: -1]
        return msa_dict


def build_hmm(msa_dict):
    """
    Build hmm model for msa_dict
    transition matrix_j:
    M_j->M_j+1  M_j->I_j    M_j->D_j+1
    I_j->M_j+1  I_j->I_j    I_j->D_j+1
    D_j->M_j+1  D_j->I_j    D_j->D_j+1
    :param msa_dict:
    :return:transition probability [sx3x3](MID->MID) , emission probability [sx2xn](MI->a), amino [n](index->a)
    """

    num_aligns = len(msa_dict.keys())
    values = list(msa_dict.values())
    len_seqs = len(values[0])

    # compute the states(MID) and amino
    states = np.zeros((num_aligns, len_seqs + 2), dtype=np.uint8)
    amino = ['-']
    model_len = len_seqs + 1
    for i in range(len_seqs):
        _count = 0
        for j in range(num_aligns):
            if values[j][i] == '-':
                _count += 1
            elif values[j][i] not in amino:
                amino.append(values[j][i])
        if _count / num_aligns > 0.5:
            states[:, i + 1] = I
            model_len -= 1
        else:
            for j in range(num_aligns):
                if values[j][i] == '-':
                    states[j, i + 1] = D
    amino.remove('-') # delete '-'
    amino = dict(zip(amino, range(len(amino))))

    '''# show the states
    c = plt.pcolor(states)
    plt.colorbar(c)
    plt.show()'''

    transition = np.zeros((model_len, 3, 3))
    emission = np.zeros((model_len, 2, len(amino)))

    pointer = 0
    for i in range(model_len):
        if states[0, pointer + 1] == I:
            count = 1
            while states[0, pointer + count] == I:
                count += 1
            transition[i, I, I] = (count - 2) * num_aligns
            for j in range(num_aligns):
                transition[i, I, states[j, pointer + count]] += 1
                transition[i, states[j, pointer], I] = 1.0
                if states[j, pointer] == M and pointer > 0:
                    emission[i, M, amino[values[j][pointer - 1]]] += 1
                for k in range(pointer + 1, pointer + count):
                    if values[j][k - 1] != '-':
                        emission[i, I, amino[values[j][k - 1]]] += 1

            transition[i, I, :] /= transition[i, I, :].sum()
            pointer += count
        else:
            for j in range(num_aligns):
                transition[i, states[j, pointer], states[j, pointer + 1]] += 1
                if states[j, pointer] == M and pointer > 0:
                    emission[i, M, amino[values[j][pointer - 1]]] += 1
            transition[i, M, :] /= transition[i, M, :].sum()
            if transition[i, D, :].sum() > 0:
                transition[i, D, :] /= transition[i, D, :].sum()
            pointer += 1
        emission[i, :, :] += 1
        emission[i, M, :] /= emission[i, M, :].sum()
        emission[i, I, :] /= emission[i, I, :].sum()

    np.savez('ques2.npz', transition=transition, emission=emission, amino=list(amino.keys()))

    return transition, emission, amino


def viterbi(seq, transition, emission, amino):
    """

    :param seq: sequence
    :param transition:
    :param emission:
    :param amino:
    :return:
    """

    model_len = transition.shape[0]
    num_obs = emission.shape[1]
    seq_len = len(seq)
    log_transition = np.log(transition)
    log_emission = np.log(num_obs * emission)

    # dimensions for MID, X, X, value/leftup
    V = np.zeros((3, model_len, seq_len + 1))
    dire = np.zeros((3, model_len, seq_len + 1), dtype=np.uint8)   # 3 means termination

    # initialization
    dire[D, 0, :] = dire[:, :, 0] = T
    dire[I, 0, 1] = dire[D, 1, 0] = M
    dire[I, 0, 2:] = I
    dire[D, 2:, 0] = D

    # compute value
    for j in range(1, model_len):
        for i in range(1, seq_len + 1):

            for X in [M, I]:
                V[X, j, i] = log_emission[j, X, amino[seq[i - 1]]]

            value_update = np.array([V[X, j - 1, i - 1] + log_transition[j - 1, X, M] for X in [M, I, D]])
            dire[M, j, i] = value_update.argmax()
            V[M, j, i] += value_update[dire[M, j, i]]

            value_update = np.array([V[X, j, i - 1] + log_transition[j, X, I] for X in [M, I, D]])
            dire[I, j, i] = value_update.argmax()
            V[I, j, i] += value_update[dire[I, j, i]]

            value_update = np.array([V[X, j - 1, i] + log_transition[j - 1, X, D] for X in [M, I, D]])
            dire[D, j, i] = value_update.argmax()
            V[D, j, i] = value_update[dire[D, j, i]]

    max_index = np.argmax(V[:, -1, -1] + log_transition[-1, :, M])
    max_index = [max_index, model_len - 1, seq_len]

    best_path = ''
    while True:
        if max_index[0] == M:
            best_path = 'M' + best_path
            max_index[0] = dire[M, max_index[1], max_index[2]]
            max_index[1] -= 1
            max_index[2] -= 1
        elif max_index[0] == I:
            best_path = 'I' + best_path
            max_index[0] = dire[I, max_index[1], max_index[2]]
            max_index[2] -= 1
        elif max_index[0] == D:
            best_path = 'D' + best_path
            max_index[0] = dire[D, max_index[1], max_index[2]]
            max_index[1] -= 1
        elif max_index[0] == T:
            break

    return best_path[1:]


def forward(seq, transition, emission, amino):
    """

    :param seq: sequence
    :param transition:
    :param emission:
    :param amino:
    :return:
    """

    model_len = transition.shape[0]
    num_obs = emission.shape[1]
    seq_len = len(seq)
    log_emission = np.log(num_obs * emission)

    # dimensions for MID, X, X, value/leftup
    F = np.zeros((3, model_len, seq_len + 1))

    # compute value
    for j in range(1, model_len):
        for i in range(1, seq_len + 1):

            for X in [M, I]:
                F[X, j, i] = log_emission[j, X, amino[seq[i - 1]]]

            F[M, j, i] += log_sum_exp(F[:, j - 1, i - 1], transition[j - 1, :, M])
            F[I, j, i] += log_sum_exp(F[:, j, i - 1], transition[j, :, I])
            F[D, j, i] += log_sum_exp(F[:, j - 1, i], transition[j - 1, :, D])

    log_odds = log_sum_exp(F[:, -1, -1], transition[-1, :, M])
    return log_odds


if __name__ == '__main__':

    transition, emission, amino = build_hmm(get_malign('clustalw.aln'))
    for seq in [SEQUENCE1, SEQUENCE2]:
        print(viterbi(seq, transition, emission, amino))
        print(forward(seq, transition, emission, amino))
