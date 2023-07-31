# Monkey EEG Analysis

We aim to conduct EEG signal analysis on monkeys under anaesthesia to draw meaningful conclusions. Our objective is to utilize the insights gained from this study to contribute to an upcoming EEG workshop held at CMI Chennai from 3rd July to 8th July

## Team

---

1. Ninad Aithal: BS in Data Science
2. Jainendra Tiwari: BS in Data Science
3. Tarun Kumar Reddy: BTech, Sai University. 
4. Vaishali Agarwal: MSc, Data Science, CMI

## About the Data

- **Two subjects (Two Monkeys)**
- **4 Different Conditions: Rest, Low Anaesthesia, Deep Anaesthesia, and Recovery**
- 5 min in each state
- Truncated it to 100 sec

Sampling rate:  1000Hz
Location of electrodes: **Fp1, Fp2, F7, F3, Fz, F4, F8, T3, C3, C4, T4, T5, P3, T6, O1, O2** 

File: EEG_{experiments}.mat (Data matrix: Channel x Time)

### Visualization of the average of one condition

![Untitled](Monkey%20EEG%20Analysis/Untitled.png)

### Visualization of the average of one condition after truncation

![Untitled](Monkey%20EEG%20Analysis/Untitled%201.png)

### Visualization of the average of all channels in different conditions

![Untitled](Monkey%20EEG%20Analysis/Untitled%202.png)

![Untitled](Monkey%20EEG%20Analysis/Untitled%203.png)

### Plotting Power Spectral Density using `mne.viz.plot_raw_psd`

### Subject 1 - 20120123S11

![Subject 1 at resting stage](Monkey%20EEG%20Analysis/psd_plot_rest_0.png)

Subject 1 at resting stage

![Subject 1 at low-anesthetic stage](Monkey%20EEG%20Analysis/psd_plot_low-anesthetic_0.png)

Subject 1 at low-anesthetic stage

![Subject 1 at deep-anesthetic stage](Monkey%20EEG%20Analysis/psd_plot_deep-anesthetic_0.png)

Subject 1 at deep-anesthetic stage

![Subject 1 at recovery stage](Monkey%20EEG%20Analysis/psd_plot_recovery_0.png)

Subject 1 at recovery stage

### Subject 2 - 20120904S11

![Subject 2 at rest stage](Monkey%20EEG%20Analysis/psd_plot_rest_1.png)

Subject 2 at rest stage

![Subject 2 at low-anesthetic stage](Monkey%20EEG%20Analysis/filtered_psd_plot_low-anesthetic_1.png)

Subject 2 at low-anesthetic stage

![Subject 2 at deep-anesthetic stage](Monkey%20EEG%20Analysis/psd_plot_deep-anesthetic_1.png)

Subject 2 at deep-anesthetic stage

![Subject 2 at the recovery stage](Monkey%20EEG%20Analysis/psd_plot_recovery_1.png)

Subject 2 at the recovery stage

### Comparing PSD of all the states for a subject

![Untitled](Monkey%20EEG%20Analysis/Untitled%204.png)

![Untitled](Monkey%20EEG%20Analysis/Untitled%205.png)

### Observations

1. We see that the data of subject 2 has very less standard deviation when compared to subject 1. 
2. We see a sharp peak at 50Hz and odd multiples of 50Hz are assumed to be noise, which is to be eliminated during preprocessing
3. The effect of anesthesia is observed as the amplitude of higher-frequency waves becomes increasingly flat.

## PSD after using Band Pass Filter

### Subject-1

![Rest](Monkey%20EEG%20Analysis/filtered_psd_plot_rest_0.png)

Rest

![Low](Monkey%20EEG%20Analysis/filtered_psd_plot_low-anesthetic_0.png)

Low

![Deep](Monkey%20EEG%20Analysis/filtered_psd_plot_deep-anesthetic_0.png)

Deep

![Recovery](Monkey%20EEG%20Analysis/filtered_psd_plot_recovery_0.png)

Recovery

### Subject-2

![Rest](Monkey%20EEG%20Analysis/filtered_psd_plot_rest_1.png)

Rest

![Low](Monkey%20EEG%20Analysis/filtered_psd_plot_low-anesthetic_1%201.png)

Low

![Deep](Monkey%20EEG%20Analysis/filtered_psd_plot_deep-anesthetic_1.png)

Deep

![Recovery ](Monkey%20EEG%20Analysis/filtered_psd_plot_recovery_1.png)

Recovery 

## Comparing the Spectral Entropy of all events

![Spectral_entropy.png](Monkey%20EEG%20Analysis/Spectral_entropy.png)

## Waveform Complexity

Waveform complexity is a measure that quantifies the complexity or irregularity of a waveform. It provides information about the temporal structure and variability of the signal. A waveform with higher complexity indicates a more intricate pattern, while a waveform with lower complexity suggests a simpler or more regular pattern.

![waveform_complexity_rest.png](Monkey%20EEG%20Analysis/waveform_complexity_rest.png)

![waveform_complexity_low_anes.png](Monkey%20EEG%20Analysis/waveform_complexity_low_anes.png)

![waveform_complexity_deep_anes.png](Monkey%20EEG%20Analysis/waveform_complexity_deep_anes.png)

![waveform_complexity_recovery.png](Monkey%20EEG%20Analysis/waveform_complexity_recovery.png)

## Power Distribution across bands

```python
frequency_bands = {'delta': [0.5, 4],
                   'theta': [4, 8],
                   'alpha': [8, 13],
                   'beta': [13, 30],
                   'gamma': [30, 40]}
```

Subject 1

![Screenshot 2023-07-19 at 11.29.01 AM.png](Monkey%20EEG%20Analysis/Screenshot_2023-07-19_at_11.29.01_AM.png)

Subject 2

![Screenshot 2023-07-19 at 11.30.05 AM.png](Monkey%20EEG%20Analysis/Screenshot_2023-07-19_at_11.30.05_AM.png)
