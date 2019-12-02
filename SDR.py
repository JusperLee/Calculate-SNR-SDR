from mir_eval.separation import bss_eval_sources
from itertools import permutations


def SDR(est, egs):
    '''
        calculate SDR
        est: Network generated audio
        egs: Ground Truth
    '''
    length = est.numpy().shape[0]
    sdr, _, _, _ = bss_eval_sources(egs.numpy()[:length], est.numpy()[:length])
    return float(sdr)


def permutation_sdr(est_list, egs_list):
    n = len(est_list)
    sdrs = []
    for p in permutations(range(n)):
        result = sum([SDR(est_list[a], egs_list[b])
                      for a, b in enumerate(p)])/n
        sdrs.append(result)
    return max(sdrs)
