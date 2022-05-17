import sys
sys.path.append("..")

from config import settings

def get_column_name_raw(sensor_location: str) -> list[str]:
    assert sensor_location in settings.SENSOR_NAME_ACC, 'Invalid Sensor Location'

    column_name = [sensor_location + data for data in settings.SENSOR_SUFFIX_ACC]
    if sensor_location == 'Arm':
        column_name = column_name + settings.SENSOR_LAST_SUFFIX_Arm
    else:
        column_name = column_name + settings.SENSOR_LAST_SUFFIX_Other

    return column_name


def get_column_name_prep(sensor_location: str) -> list[str]:
    assert sensor_location in settings.SENSOR_NAME_ACC or sensor_location in settings.SENSOR_NAME_EEG , 'Invalid Sensor Location'

    if sensor_location == 'Arm': return settings.PREP_COLNAME_ARM
    elif sensor_location == 'Waist': return settings.PREP_COLNAME_WAIST
    elif sensor_location == 'LShank': return settings.PREP_COLNAME_LS
    elif sensor_location == 'RShank': return settings.PREP_COLNAME_RS
    elif sensor_location == 'EEG': return settings.PREP_COLNAME_EEG
    elif sensor_location == 'EMG': return settings.PREP_COLNAME_EMG


def get_time_suffix(idx: int, time_stamp: str):
    if idx%5 == 0:
        return time_stamp
    else:
        return settings.TIME_SUFFIX_TABLE[idx%5]


def reformat_col_gait(Dataframe_Gait):
    # Delete the time stamp of the right leg, wrist and waist, leaving only the time stamp of the left leg's file.
    # If the left leg data was not collected, pay attention to change the DropName and CriName!

    Trans = Dataframe_Gait['RShankOriTIME']
    Dataframe_Gait.drop(labels=['RShankOriTIME'], axis=1, inplace = True)
    Dataframe_Gait.insert(1, 'RShankOriTIME', Trans)

    Trans = Dataframe_Gait['WaistOriTIME']
    Dataframe_Gait.drop(labels=['WaistOriTIME'], axis=1, inplace = True)
    Dataframe_Gait.insert(2, 'WaistOriTIME', Trans)

    Trans = Dataframe_Gait['ArmOriTIME']
    Dataframe_Gait.drop(labels=['ArmOriTIME'], axis=1, inplace = True)
    Dataframe_Gait.insert(3, 'ArmOriTIME', Trans)

    Dataframe_Gait = Dataframe_Gait.rename(columns={settings.COL_CRITERION+'TIME': 'GaitTIME'})
    Dataframe_Gait = Dataframe_Gait.drop([settings.COL_DROP+'TIME', 'WaistTIME', 'ArmTIME'], axis=1)
    
    return Dataframe_Gait