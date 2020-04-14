from AudioReader import AudioReader
from SDR import permutation_sdr
from SNR import permute_SI_SNR
import matplotlib.pyplot as plt
import tqdm
import matplotlib.ticker as ticker

def main(est_spk1, est_spk2, egs_spk1, egs_spk2):
    est_spk1 = AudioReader(est_spk1)
    est_spk2 = AudioReader(est_spk2)
    egs_spk1 = AudioReader(egs_spk1)
    egs_spk2 = AudioReader(egs_spk2)
    length = len(est_spk1)
    x = [i for i in range(length)]
    sdr = []
    snr = []
    index = 0
    for idx in range(length):
        ests = [est_spk1[idx], est_spk2[idx]]
        egs = [egs_spk1[idx], egs_spk2[idx]]
        mix = egs_spk1[idx]+egs_spk2[idx]

        _snr, per = permute_SI_SNR(ests, egs, mix)
        _sdr = permutation_sdr(ests, egs, mix, per)
    
        index += 1
        if True:
            sdr.append(float(_sdr))
            snr.append(float(_snr))
            print('\r{} : {}, SNR: {:5f}, SDR: {:5f}'.format(index, length, _snr, _sdr), end='')

    print('\nAverage SNRi: {:.5f}'.format(float(sum(snr))/len(sdr)))
    print('Average SDRi: {:.5f}'.format(float(sum(sdr)/len(sdr))))


if __name__ == "__main__":
    est_spk1 = '/home/likai/data1/create_scp/self_conv_spk1.scp'
    est_spk2 = '/home/likai/data1/create_scp/self_conv_spk2.scp'
    egs_spk1 = '/home/likai/data1/create_scp/tt_s1.scp'
    egs_spk2 = '/home/likai/data1/create_scp/tt_s2.scp'
    main(est_spk1, est_spk2, egs_spk1, egs_spk2)
