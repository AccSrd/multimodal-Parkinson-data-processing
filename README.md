# Multimodal Dataset of Freezing of Gait in Parkinson's Disease

## Datasets

### Filtered Data

[Li, Hantao (2021), “Multimodal Dataset of Freezing of Gait in Parkinson's Disease”, Mendeley Data, V3, doi: 10.17632/r8gmbtv7w2.3](https://data.mendeley.com/datasets/r8gmbtv7w2/3)

### Raw Data

[Li, Hantao (2021), “Raw Data: Multimodal Dataset of Freezing of Gait in Parkinson's Disease”, Mendeley Data, V1, doi: 10.17632/t8j8v4hnm4.1](https://data.mendeley.com/datasets/t8j8v4hnm4/1)

We provide the source files for the publicity and comprehensiveness of the data. The data length in the Raw Data file is longer than in the previous database because it contains signals recorded during patient preparation. However, due to privacy and medical data protection reasons, we cannot provide you with videos and personal information of patients, so you cannot use the files in this database to get the annotated files directly (if you can get the label marks, you can use the provided scripts to self-label the raw data into filtered data). If you do not have a specific need for raw files, you can ignore this database and use the filtered dataset.

## Paper

[Zhang, W., Huang, D., Li, H., Wang, L., Wei, Y., Pan, K., ... & Guo, Y. (2021). Sensoring and Application of Multimodal Data for the Detection of Freezing of Gait in Parkinson's Disease.](https://arxiv.org/abs/2110.04444)

## Abstract

This repository contains the code of data processing using in the dataset and paper above, and some sample data corresponding with the code.

![Fig Abstract](/Fig/Abstract.JPG "Abstract")

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

## Sample Data

The corresponding sample data were given in the `./Sample Data` folder. It is worth mentioning that the sample data is just a sample, un-alignment segment of the actual data.

The EEG/EMG raw data provided in the dataset must be preprocessed (detailed information is provided in the paper) in EEGLAB to get the `.txt` file shown in `./Sample Data`. We do not show the EEGLAB scripts here. The contrast curve of the EEG signal is shown here. The above one is raw data in `.eeg` file, while the image below is the preprocessed data.

![Raw EEG signal](/Fig/ori_eeg.jpeg "Raw EEG signal")
![Prep EEG signal](/Fig/prep_eeg.png "Prep EEG signal")

The whole dataset is provided in the dataset shown above. Please use that link to download the dataset.

## Python Scripts

We provide the python script to process the raw data into filtered data in the `./Scripts` folder.

It is effortless to use:
`python Scripts/data_process.py`

You can modify the parameters in the `./Scripts/data_process.py` and the config settings in the `./settings.toml` to your own need. However, we recommend that you directly utilize the data we provide in the dataset. We performed rigorous data alignment work using multiple timestamp information sources and invited experienced Parkinson's experts to perform data labeling work.
