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
    for idx in tqdm.tqdm(range(length)):
        ests = [est_spk1[idx], est_spk2[idx]]
        egs = [egs_spk1[idx], egs_spk2[idx]]
        sdr.append(float(permutation_sdr(ests, egs)))
        snr.append(float(permute_SI_SNR(ests, egs)))

    plt.title('Sampels SNR and SDR Results')
    ax = plt.subplot()
    tick_spacing = 10
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    plt.scatter(x, sdr, marker='x', color='m', label=u'sdr', s=5)
    plt.scatter(x, snr, marker='o', color='c', label=u'snr', s=5)
    plt.legend()
    #plt.xticks(l, lx)
    plt.ylabel('value')
    plt.xlabel('sample index')
    plt.savefig('convtasnet_results.png')
    print('Average SNR: {:.5f}'.format(float(sum(snr))/length))
    print('Average SDR: {:.5f}'.format(float(sum(sdr)/length)))


if __name__ == "__main__":
    est_spk1 = '/home/likai/data1/create_scp/conv_spk1.scp'
    est_spk2 = '/home/likai/data1/create_scp/conv_spk2.scp'
    egs_spk1 = '/home/likai/data1/create_scp/tt_s1.scp'
    egs_spk2 = '/home/likai/data1/create_scp/tt_s2.scp'
    main(est_spk1, est_spk2, egs_spk1, egs_spk2)
