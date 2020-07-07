# -*- encoding: utf-8 -*-
'''
@Filename    :NpzReader.py
@Time        :2020/07/07 22:49:09
@Author      :Kai Li
@Version     :1.0
'''

import torchaudio
import torch
import numpy as np

def handle_scp(scp_path):
    '''
    Read scp file script
    input: 
          scp_path: .scp file's file path
    output: 
          scp_dict: {'key':'wave file path'}
    '''
    scp_dict = dict()
    line = 0
    lines = open(scp_path, 'r').readlines()
    for l in lines:
        scp_parts = l.strip().split()
        line += 1
        if len(scp_parts) != 2:
            raise RuntimeError("For {}, format error in line[{:d}]: {}".format(
                scp_path, line, scp_parts))
        if len(scp_parts) == 2:
            key, value = scp_parts
        if key in scp_dict:
            raise ValueError("Duplicated key \'{0}\' exists in {1}".format(
                key, scp_path))

        scp_dict[key] = value

    return scp_dict


def read_wav(fname, return_rate=False):
    '''
         Read wavfile using Pytorch audio
         input:
               fname: wav file path
               return_rate: Whether to return the sampling rate
         output:
                src: output tensor of size C x L 
                     L is the number of audio frames 
                     C is the number of channels. 
                sr: sample rate
    '''
    src, sr = torchaudio.load(fname, channels_first=True)
    if return_rate:
        return src.squeeze(), sr
    else:
        return src.squeeze()


def write_wav(fname, src, sample_rate):
    '''
         Write wav file
         input:
               fname: wav file path
               src: frames of audio
               sample_rate: An integer which is the sample rate of the audio
         output:
               None
    '''
    torchaudio.save(fname, src, sample_rate)


class AudioReader(object):
    '''
        Class that reads Wav format files
        Input as a different scp file address
        Output a matrix of wav files in all scp files.
    '''

    def __init__(self, scp_path, sample_rate=8000):
        super(AudioReader, self).__init__()
        self.sample_rate = sample_rate
        self.index_dict = handle_scp(scp_path)
        self.keys = list(self.index_dict.keys())

    def _load(self, key):
        src = np.load(self.index_dict[key])['data']
        return torch.from_numpy(src)

    def __len__(self):
        return len(self.keys)

    def __iter__(self):
        for key in self.keys:
            yield key, self._load(key)

    def __getitem__(self, index):
        if type(index) not in [int, str]:
            raise IndexError('Unsupported index type: {}'.format(type(index)))
        if type(index) == int:
            num_uttrs = len(self.keys)
            if num_uttrs < index and index < 0:
                raise KeyError('Interger index out of range, {:d} vs {:d}'.format(
                    index, num_uttrs))
            index = self.keys[index]
        if index not in self.index_dict:
            raise KeyError("Missing utterance {}!".format(index))

        return self._load(index)


if __name__ == "__main__":
    r = AudioReader('/home/likai/data1/create_scp/cv_s2.scp')
    index = 0
    print(r[1])
