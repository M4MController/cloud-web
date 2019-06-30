# -*- coding: utf-8 -*-
import obd
from m4m_utils import cur_date
from termcolor import colored

command_table = [
    obd.commands.PIDS_A,
    obd.commands.STATUS,
    obd.commands.FREEZE_DTC,
    obd.commands.FUEL_STATUS,
    obd.commands.ENGINE_LOAD,
    obd.commands.COOLANT_TEMP,
    obd.commands.SHORT_FUEL_TRIM_1,
    obd.commands.LONG_FUEL_TRIM_1,
    obd.commands.SHORT_FUEL_TRIM_2,
    obd.commands.LONG_FUEL_TRIM_2,
    obd.commands.FUEL_PRESSURE,
    obd.commands.INTAKE_PRESSURE,
    obd.commands.RPM,
    obd.commands.SPEED,
    obd.commands.TIMING_ADVANCE,
    obd.commands.INTAKE_TEMP,
    obd.commands.MAF,
    obd.commands.THROTTLE_POS,
    obd.commands.AIR_STATUS,
    obd.commands.O2_SENSORS,
    obd.commands.O2_B1S1,
    obd.commands.O2_B1S2,
    obd.commands.O2_B1S3,
    obd.commands.O2_B1S4,
    obd.commands.O2_B2S1,
    obd.commands.O2_B2S2,
    obd.commands.O2_B2S3,
    obd.commands.O2_B2S4,
    obd.commands.OBD_COMPLIANCE,
    obd.commands.O2_SENSORS_ALT,
    obd.commands.AUX_INPUT_STATUS,
    obd.commands.RUN_TIME,
    obd.commands.PIDS_B,
    obd.commands.DISTANCE_W_MIL,
    obd.commands.FUEL_RAIL_PRESSURE_VAC,
    obd.commands.FUEL_RAIL_PRESSURE_DIRECT,
    obd.commands.O2_S1_WR_VOLTAGE,
    obd.commands.O2_S2_WR_VOLTAGE,
    obd.commands.O2_S3_WR_VOLTAGE,
    obd.commands.O2_S4_WR_VOLTAGE,
    obd.commands.O2_S5_WR_VOLTAGE,
    obd.commands.O2_S6_WR_VOLTAGE,
    obd.commands.O2_S7_WR_VOLTAGE,
    obd.commands.O2_S8_WR_VOLTAGE,
    obd.commands.COMMANDED_EGR,
    obd.commands.EGR_ERROR,
    obd.commands.EVAPORATIVE_PURGE,
    obd.commands.FUEL_LEVEL,
    obd.commands.WARMUPS_SINCE_DTC_CLEAR,
    obd.commands.DISTANCE_SINCE_DTC_CLEAR,
    obd.commands.EVAP_VAPOR_PRESSURE,
    obd.commands.BAROMETRIC_PRESSURE,
    obd.commands.O2_S1_WR_CURRENT,
    obd.commands.O2_S2_WR_CURRENT,
    obd.commands.O2_S3_WR_CURRENT,
    obd.commands.O2_S4_WR_CURRENT,
    obd.commands.O2_S5_WR_CURRENT,
    obd.commands.O2_S6_WR_CURRENT,
    obd.commands.O2_S7_WR_CURRENT,
    obd.commands.O2_S8_WR_CURRENT,
    obd.commands.CATALYST_TEMP_B1S1,
    obd.commands.CATALYST_TEMP_B2S1,
    obd.commands.CATALYST_TEMP_B1S2,
    obd.commands.CATALYST_TEMP_B2S2,
    obd.commands.PIDS_C,
    obd.commands.STATUS_DRIVE_CYCLE,
    obd.commands.CONTROL_MODULE_VOLTAGE,
    obd.commands.ABSOLUTE_LOAD,
    obd.commands.COMMANDED_EQUIV_RATIO,
    obd.commands.RELATIVE_THROTTLE_POS,
    obd.commands.AMBIANT_AIR_TEMP,
    obd.commands.THROTTLE_POS_B,
    obd.commands.THROTTLE_POS_C,
    obd.commands.ACCELERATOR_POS_D,
    obd.commands.ACCELERATOR_POS_E,
    obd.commands.ACCELERATOR_POS_F,
    obd.commands.THROTTLE_ACTUATOR,
    obd.commands.RUN_TIME_MIL,
    obd.commands.TIME_SINCE_DTC_CLEARED,
    obd.commands.MAX_MAF,
    obd.commands.FUEL_TYPE,
    obd.commands.ETHANOL_PERCENT,
    obd.commands.EVAP_VAPOR_PRESSURE_ABS,
    obd.commands.EVAP_VAPOR_PRESSURE_ALT,
    obd.commands.SHORT_O2_TRIM_B1,
    obd.commands.LONG_O2_TRIM_B1,
    obd.commands.SHORT_O2_TRIM_B2,
    obd.commands.LONG_O2_TRIM_B2,
    obd.commands.FUEL_RAIL_PRESSURE_ABS,
    obd.commands.RELATIVE_ACCEL_POS,
    obd.commands.HYBRID_BATTERY_REMAINING,
    obd.commands.OIL_TEMP,
    obd.commands.FUEL_INJECT_TIMING,
    obd.commands.FUEL_RATE,
]

def obd_start():
    print(cur_date(), "Connecting OBD...")
    obd_con = obd.OBD()
    if obd_con.is_connected():
        print(cur_date(), "OBD connected\n")
    else:
        print(cur_date(), colored("OBD not connected\n", 'red'))

    return obd_con 


def obd_read(con):
    data = {}
    for cmd in command_table:
        response = con.query(cmd)
        data[cmd.name.lower()] = response.value

    return data