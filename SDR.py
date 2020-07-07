# -*- encoding: utf-8 -*-
'''
@Filename    :SDR.py
@Time        :2020/07/07 22:47:36
@Author      :Kai Li
@Version     :1.0
'''
from mir_eval.separation import bss_eval_sources
from itertools import permutations


def SDR(est, egs, mix):
    '''
        calculate SDR
        est: Network generated audio
        egs: Ground Truth
    '''
    length = est.numpy().shape[0]
    sdr, _, _, _ = bss_eval_sources(egs.numpy()[:length], est.numpy()[:length])
    mix_sdr, _, _, _ = bss_eval_sources(egs.numpy()[:length], mix.numpy()[:length])
    return float(sdr-mix_sdr)


def permutation_sdr(est_list, egs_list, mix, per):
    n = len(est_list)
    result = sum([SDR(est_list[a], egs_list[b], mix)
                      for a, b in enumerate(per)])/n
    return result