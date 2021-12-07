import numpy as np
import random
from collections import defaultdict
import time, datetime
from time import time as cur_time
import itertools
import sys, os, ast
from subprocess import call, check_call
from scipy.special import expit
import math
from copy import deepcopy
from shutil import copyfile, rmtree


class EmbedPredictor(object):
    def __init__(self, pd):
        self.pd = pd
        self.nt2vecs = defaultdict(lambda : defaultdict(lambda:(np.random.rand(pd['dim'])-0.5)/pd['dim']))
        self.nt2negas = defaultdict(list)
        self.start_time = cur_time()
    
    def prepare_training_data(self, app_traces):
        relations = []
        for app_trace in app_traces:
            u = app_trace.uid
            l = 'loc_' + app_trace.loc
            t = app_trace.ts%24
            dp = int(math.floor(app_trace.ts/24))%7
            d = int(dp==4 or dp==5)
            if d==1:
                dt = 'Weekend_' + str(t)
            else:
                dt = 'Weekday_' + str(t)
            a = 'app_' + app_trace.app
            if 'c' in dir(app_trace):
                c = app_trace.c
            else:
                c = None
            relation = defaultdict(lambda : defaultdict(float))
            nts = self.pd['nt_list']                            # ['a','dt','l']
            for nt in nts:
                if eval(nt) is not None:
                    relation[nt][eval(nt)] += 1 
            relations.append(relation)
        return relations

    def fit(self, app_usage):
        relations = self.prepare_training_data(app_usage)
        pd = self.pd
        nt2vecs = self.nt2vecs        # defaultdict(lambda : defaultdict(lambda:(np.random.rand(pd['dim'])-0.5)/pd['dim']))
        
#        print('before ',nt2vecs.keys())
#        print('before ', nt2vecs['a'].keys())
        self.alpha = pd['alpha']       # 0.05 learning rate
        sample_size, sampled_size, ncount = len(relations)*pd['epoch'], 0, 0
        while True:
            random.shuffle(relations)
            for relation in relations:
                if self.alpha > pd['alpha'] * 1e-4:
                    self.alpha -= pd['alpha'] * 1e-6
                sum_vec = np.zeros(pd['dim'])         # 50 dim vectors
                sum_weight = 0
                for nt in relation:
                    for n in relation[nt]:
                        self.nt2negas[nt].append(n)
                        sum_vec += nt2vecs[nt][n] * relation[nt][n]
#                        print('nt2vecs keys ', nt2vecs.keys())
#                        print('nt2vecs[0] keys ', nt2vecs[nt].keys())
#                        print('nt2vecs ', nt2vecs[nt][n])
                        sum_weight += relation[nt][n]
                for nt in relation:
                    for n in relation[nt]:
                        for j in range(pd['negative']+1):      # 1
                            minus_n_vec = sum_vec - nt2vecs[nt][n] * relation[nt][n] 
                            minus_n_weight = sum_weight - relation[nt][n]
                            minus_n_vec_avg = minus_n_vec / minus_n_weight  #This is the vector h
                            if j==0:                #Positive Sample
                                target = n
                                label = 1
                            else:                   #Negative Sample
                                target = random.choice(self.nt2negas[nt])
                                if target==n:
                                    continue
                                label = 0
                            f = np.dot(nt2vecs[nt][target], minus_n_vec_avg)
                            g = (label - expit(f)) * self.alpha        # 1/(1+exp(-x))
                            for nt2 in relation:
                                for n2 in relation[nt2]:
                                    if not (nt==nt2 and n==n2):
                                        nt2vecs[nt2][n2] += g*nt2vecs[nt][target]*relation[nt2][n2]/minus_n_weight
                            #[Fix Me!]: How to update "nt2vecs[nt][target]"?*************************************************
                            nt2vecs[nt][target] += g*minus_n_vec_avg
                            #*********************************************************************************************
                        sampled_size += 1
                        if sampled_size==sample_size:
                            return nt2vecs

