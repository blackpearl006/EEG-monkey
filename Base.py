# import functions

import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import math
import mne  
from scipy import signal
import pandas as pd
import os
from mne.time_frequency import psd_array_welch
from func import compute_spectral_measures
from mne.viz import plot_raw_psd


ch_names = ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'T3', 'C3', 'C4', 'T4', 'T5', 'P3', 'T6', 'O1', 'O2'] 
ch_types = ['eeg']*16

# Sampling frequency is 1000Hz
fs = 1000

directory = '/path/to/desired/folder/Monkey_Anesthesia'

stages = ['rest', 'low-anesthetic', 'deep-anesthetic', 'recovery']

req_sub = [x for x in os.listdir(directory) if x[0:4] == '2012']

mat_data = {}
eeg_data = {key: {} for key in stages}
raw_data = {key: {} for key in stages}

info = mne.create_info(ch_names=ch_names, ch_types=ch_types, sfreq=fs)

for subject in req_sub:
    if os.path.isdir(f'{directory}/{subject}'):
        mat_data[subject] = {}
        for condition in stages:
            mat_data[subject][condition] = scipy.io.loadmat(f'{directory}/{subject}/EEG_{condition}.mat')
            if subject[0:6]=='201201':
                eeg_data[condition][subject] = mat_data[subject][condition]['EEG'][:,:100000]
                eeg_data[condition][subject] = np.delete(mat_data[subject][condition]['EEG'], -5, axis=0)[:100000]
                
                # Calculate the mean and standard deviation of the EEG data
                eeg_mean = np.mean(eeg_data[condition][subject])
                eeg_std = np.std(eeg_data[condition][subject])

                # Perform z-score normalization on the EEG data in eeg_data dictionary
                eeg_data[condition][subject] = (eeg_data[condition][subject] - eeg_mean) / eeg_std

                raw_data[condition][subject] = mne.io.RawArray(np.delete(mat_data[subject][condition]['EEG'], -5, axis=0)[:100000], info)
                raw_data[condition][subject].apply_function(lambda x: (x - eeg_mean) / eeg_std)
                continue
            else :
                eeg_data[condition][subject] = mat_data[subject][condition]['EEG'][:,:100000]
                eeg_mean = np.mean(eeg_data[condition][subject])
                eeg_std = np.std(eeg_data[condition][subject])
                eeg_data[condition][subject] = (eeg_data[condition][subject] - eeg_mean) / eeg_std

                raw_data[condition][subject] = mne.io.RawArray(mat_data[subject][condition]['EEG'][:,:100000], info)
                raw_data[condition][subject].apply_function(lambda x: (x - eeg_mean) / eeg_std)

sub_1 = list(eeg_data['rest'].keys())[0]
sub_2 = list(eeg_data['rest'].keys())[1]
sub = [sub_1, sub_2]

for i,x in enumerate(sub):
    for y in stages:
        Raw = raw_data[y][x]
        Raw.compute_psd(fmax=40).plot()
        # help(Raw.compute_psd().plot())
        # fig = plot_raw_psd(Raw, average=True, picks='eeg', show=True,fmax=40)
        # fig.savefig(f'./images/psd_plot_{y}_{i}.png')

print('hai')
for i, x in enumerate(sub):
    for y in stages:
        raw = raw_data[y][x]
        raw_data[y][x] = raw.filter(l_freq = 0.1, h_freq=40, method='fir', phase = 'zero', picks='eeg')
        

for i,x in enumerate(sub):
    for y in stages:
        Raw = raw_data[y][x]
        fig = plot_raw_psd(Raw, average=True, picks='eeg', show=True,fmax=40)
        fig.savefig(f'./images/filtered_psd_plot_{y}_{i}.png')

def spectral_entropy(ts, sfreq=1000,fmin=0.1, fmax=40, n_per_seg=1000, n_fft=1000):
  #SPECTRAL ENTROPY - ENTROPY IN FREQUENCY DOMAIN
    psd, freqs = psd_array_welch(ts, sfreq, fmin=fmin, fmax=fmax, n_per_seg=n_per_seg,n_fft=n_fft)
    psd_norm = psd / psd.sum()
    sp_e = -np.sum(psd_norm*np.log2(psd_norm))
    return sp_e/np.log2(psd_norm.shape[0])


frequency_bands = {'delta': [0.5, 4],
                   'theta': [4, 8],
                   'alpha': [8, 13],
                   'beta': [13, 30],
                   'gamma': [30, 40]}

band_data = {key: {} for key in stages}
for x in sub:
    for y in stages:
        Raw = raw_data[y][x]  # Assuming raw_data contains RawArray objects
        data = Raw.get_data().flatten()
        psds, freqs = psd_array_welch(data, sfreq=1000, fmin=0.5, fmax=40, n_per_seg=1000 ,n_fft=256)

        band_power = dict()
        for band, (fmin, fmax) in frequency_bands.items():
            band_mask = np.logical_and(freqs >= fmin, freqs <= fmax)
            band_power[band] = np.mean(psds[band_mask], axis=0)

        band_data[y][x] = band_power

perc_band = {key: {} for key in stages}
for x in sub:
    for y in stages:
        band_labels = list(band_data[y][x].keys())
        band_sum = sum([power for power in band_data[y][x].values()])
        perc_band[y][x] = {}
        for lab in band_labels:
            perc_band[y][x][lab] = band_data[y][x][lab]*100/band_sum
        

import numpy as np
import mne
import matplotlib.pyplot as plt

# Assuming you have computed the band_power dictionary as described in the previous response

# Extract the channel names from the raw data
channel_names = ch_names

# Prepare the data for visualization
band_labels = list(band_power.keys())
band_avg_power = [np.mean(power) for power in band_power.values()]

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(band_labels, band_avg_power)
plt.xlabel('Frequency Band')
plt.ylabel('Average Power')
plt.title('Power Distribution in Frequency Bands')

# Add channel-wise power values as text annotations
for i, power in enumerate(band_avg_power):
    plt.text(i, power, f'{power:.2f}', ha='center', va='bottom')

# Rotate x-axis labels for better visibility if needed
plt.xticks(rotation=45)

# Show the plot
plt.show()

spectral_entropy_plot = {key: [] for key in stages}
for x in sub:
    for y in stages:
        raw = raw_data[y][x]  # Assuming raw_data contains RawArray objects
        data = raw.get_data().flatten()
        spec_entropy = spectral_entropy(data)
        spectral_entropy_plot[y].append(spec_entropy)
        print(f'Subject {x[:6]} Stage: {y} Spectral Entropy: {spec_entropy}')

stages = list(spectral_entropy_plot.keys())
values = list(spectral_entropy_plot.values())

lower_bounds = [value[0] for value in values]
upper_bounds = [value[1] for value in values]

x = np.arange(len(stages))
bar_width = 0.35
plt.bar(x - bar_width/2, upper_bounds, width=bar_width, color='lightblue', label='Subject 1')
plt.bar(x + bar_width/2, lower_bounds, width=bar_width, color='skyblue', label='Subject 2')

plt.xlabel('Stage')
plt.ylabel('Spectral Entropy')
plt.title('Spectral Entropy for Different Stages')
plt.xticks(x, stages)
plt.legend()
plt.show()

for x in sub:
    for y in stages:
        raw = np.array(raw_data[y][x])  
        plt.specgram(raw, NFFT=1024, fs=1000/2)
        plt.show(())


import numpy as np
import matplotlib.pyplot as plt

for x in sub:
    for y in stages:
        channel_idx = 0  # Selecting the first channel
        plt.specgram(raw_data[y][x], NFFT=1000, Fs=raw[y][x].info['sfreq'])
        plt.show()

raw[0][0].shape

raw_data
