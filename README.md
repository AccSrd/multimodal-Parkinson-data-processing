# Multimodal Dataset of Freezing of Gait in Parkinson's Disease

## Datasets

### Filtered Data

[Li, Hantao (2021), “Multimodal Dataset of Freezing of Gait in Parkinson's Disease”, Mendeley Data, V3, doi: 10.17632/r8gmbtv7w2.3](https://data.mendeley.com/datasets/r8gmbtv7w2/3)

### Raw Data

[Li, Hantao (2021), “Raw Data: Multimodal Dataset of Freezing of Gait in Parkinson's Disease”, Mendeley Data, V1, doi: 10.17632/t8j8v4hnm4.1](https://data.mendeley.com/datasets/t8j8v4hnm4/1)

### Sample Data

You can find some sample data in the floder, which can be utilized for testing the processing code.

## Paper

[Zhang, W., Huang, D., Li, H., Wang, L., Wei, Y., Pan, K., ... & Guo, Y. (2021). Sensoring and Application of Multimodal Data for the Detection of Freezing of Gait in Parkinson's Disease.](https://arxiv.org/abs/2110.04444)

## Abstract

This repository contains the code of data processing using in the dataset and paper above, and some sample data corresponding with the code.

![Fig Abstract](/Fig/Abstract.jpg "Abstract")

Freezing of gaits (FOG), a debilitating transitory inability to pursue moving, is one of the severest symptoms of Parkinson's disease (PD). An accurate and reliable detection or prediction of FOG is of great significance for PD patients' assessment and rehabilitation. It is difficult to detect FOG with sufficient low-latency and high precision based on single sensor information. In order to improve the detection accuracy and facilitate further research, we gathered and presented a new multimodal dataset by combining rich physical and physiological sensor information. The multimodal data, including electroencephalogram (EEG), electromyogram (EMG), electrocardiogram (ECG), skin conductance (SC), and acceleration (ACC) in walking tasks, were collected using a high-quality hardware system integrated commercial and self-designed sensors. A standard experimental procedure was carefully designed to induce FOG in hospital surroundings. A total number of 12 PD patients completed the experiments and produced a total length of 3 hours and 42 minutes valid data. The FOG episodes in the multimodal data were labeled by two qualified physicians. The multimodal data can be used to efficiently discriminant FOG from normal locomotion, and indicated that changes in the multimodal motional and electrophysiological signals during FOG episodes could be used to guide PD patients' treatment and recovery.

## Dataset Description

The data have been collected in Beijing Xuanwu Hospital since 2019. Until the paper was written, a total of 18 individuals have been selected based on the inclusion criteria and completed the whole data collection procedures. Among them, data of 12 participants (13 experiments, Patient ID: 08 conduct the experiment twice) are valid and can be used for the investigation of multimodal data FOG detection.

The multimodal sensoring platform acquires EEG, EMG, ACC, and SC. The locations of the sensors are shown in the Fig and the Table below.

![hardware system](/Fig/hardware%20system.png "hardware system")

|   Sensing Type   | System              | Sensor Quantity |                                                       Sensor Location                                                       |
|:----------------:|---------------------|:---------------:|:---------------------------------------------------------------------------------------------------------------------------:|
|      28D-EEG     | ‘The wireless MOVE’ |        28       | FP1, FP2, F3, F4, C4, C4, P3, P4, O1, O2, F7, F8, P7, P8, Fz, Cz, Pz, FC1, FC2, CP1, CP2, FC5, FC6, CP5, CP6, TP9, TP10, IO |
|      3D-EMG      | ‘The wireless MOVE’ |        3        |                      Gastrocnemius muscle of right leg; Tibialis anterior muscle of left and right legs                     |
| 3D-Accelerometer |       MPU6050       |        4        |                               Lateral tibia of left and right legs;  Fifth lumbar spine; Wrist                              |
|      3D-Gyro     |       MPU6050       |        4        |                               Lateral tibia of left and right legs;  Fifth lumbar spine; Wrist                              |
|       1D-SC      |        LM324        |        2        |                           The second belly of the index finger and middle finger of the left hand                           |

Participants aged between 57 and 81 years (average: 69.1 years), and have disease duration between 1 and 20 years (average: 9.3 years). 10 subjects had conspicuous FOG episodes during the experiments. The total length of data was 222 minutes and 3 seconds. There are 334 FOG events with a total duration of 88 minutes and 19 seconds.

### Data Processing

There are three steps of data processing in general:

1. Raw --> Preprocessed: Sort out the original data header, and unify the data sampling frequency to 500Hz.
2. Preprocessed --> Segmented: Divided the data into a single piece of data for each task. Put multimodal data together.
3. Segmented --> Labeled: Label the Data with 1(FOG) and 0(FOG-Free.)