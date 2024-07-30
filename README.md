# [Network Traffic Analysis of Medical Devices](https://ieeexplore.ieee.org/abstract/document/10577713/)

## Table of Contents

- [Overview](#overview)
- [Citation](#citation)


## Overview
This repository is intended to provide documentation on the dataset.

This dataset contains .pcap files which makeup the device activity for 8 medical devices: Sense-U BabyMonitor, EarWax Device, FitBitFitness, GuardianAlert . Each .pcapng file contains a single packet and has been cleaned of ip/mac addresses and the checksums have been recomputed. This was done to anonymize the data and remove information which may simplify the task of classification.


| Device           | WiFi | Bluetooth | # of  functions | Description                                                                                   |
|------------------|--------------|-------------------|--------|-----------------------------------------------------------------------------------------------|
| BabyMonitor      | Yes          | Yes               | 7      | Real-time baby monitoring device through a video stream, manufactured by Sense-U.             |
| EarWax           | Yes          | No                | 5      | Device for ear wax removal with high-definition camera and LED lighting.                      |
| FitBitFitness    | Yes          | Yes               | 5      | Fitness tracker that tracks daily activity, heart rate, and sleep patterns.                   |
| GuardianAlert    | Yes          | No                | 7      | Provides 24-hour emergency support for seniors, including a wearable alert button and two-way communication for immediate assistance in a crisis. |
| KardiaMobile     | Yes          | No                | 6      | Device that can record a medical electrocardiogram (EKG) on the smartphone.                   |
| KetoScanMeter    | Yes          | Yes               | 5      | Breath-acetone analyzer that measures the amount of ketones in a person’s breath.             |
| WithingsBPM      | Yes          | Yes               | 8      | Blood pressure monitor that can be synced with a smartphone app for tracking.                 |
| WyzeScale        | Yes          | Yes               | 8      | Scale that measures weight and body mass indexes.                                             |




## Citation

If you use this dataset in your work, please cite it as:

Mashnoor, Nowfel, and Batyr Charyyev. "Network Traffic Analysis of Medical Devices." _2024 International Conference on Smart Applications, Communications and Networking (SmartNets)_. IEEE, 2024.

BibTeX: 
```bibtex
@inproceedings{mashnoor2024network,
  title={Network Traffic Analysis of Medical Devices},
  author={Mashnoor, Nowfel and Charyyev, Batyr},
  booktitle={2024 International Conference on Smart Applications, Communications and Networking (SmartNets)},
  pages={1--6},
  year={2024},
  organization={IEEE}
}
```


We hope you find this Dataset is valuable for your research or application. If you have any questions or need further assistance, please don't hesitate to contact us at nmashnoor@unr.edu