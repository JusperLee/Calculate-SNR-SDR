# -*- encoding: utf-8 -*-
'''
@Filename    :SNR.py
@Time        :2020/07/07 22:47:44
@Author      :Kai Li
@Version     :1.0
'''
import torch
from itertools import permutations


def SI_SNR(_s, s, mix, zero_mean=True):
    '''
         Calculate the SNR indicator between the two audios. 
         The larger the value, the better the separation.
         input:
               _s: Generated audio
               s:  Ground Truth audio
         output:
               SNR value 
    '''
    length = _s.shape[0]
    _s = _s[:length]
    s =s[:length]
    mix = mix[:length]
    if zero_mean:
        _s = _s - torch.mean(_s)
        s = s - torch.mean(s)
        mix = mix - torch.mean(mix)
    s_target = sum(torch.mul(_s, s))*s/(torch.pow(torch.norm(s, p=2), 2)+1e-8)
    e_noise = _s - s_target
    # mix ---------------------------
    mix_target = sum(torch.mul(mix, s))*s/(torch.pow(torch.norm(s, p=2), 2)+1e-8)
    mix_noise = mix - mix_target 
    return 20*torch.log10(torch.norm(s_target, p=2)/(torch.norm(e_noise, p=2)+1e-8)) - 20*torch.log10(torch.norm(mix_target, p=2)/(torch.norm(mix_noise, p=2)+1e-8))


def permute_SI_SNR(_s_lists, s_lists, mix):
    '''
        Calculate all possible SNRs according to 
        the permutation combination and 
        then find the maximum value.
        input:
               _s_lists: Generated audio list
               s_lists: Ground truth audio list
        output:
               max of SI-SNR
    '''
    length = len(_s_lists)
    results = []
    per = []
    for p in permutations(range(length)):
        s_list = [s_lists[n] for n in p]
        result = sum([SI_SNR(_s, s, mix, zero_mean=True) for _s, s in zip(_s_lists, s_list)])/length
        results.append(result)
        per.append(p)
    return max(results), per[results.index(max(results))]