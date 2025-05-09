import datetime
import logging
from .const import *  # Make sure DOMAIN is defined in const.py

_LOGGER = logging.getLogger(__name__)

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_sensor_data(self, sensor):
    state = self.hass.states.get(sensor)
    _LOGGER.debug(f"Getting state for sensor: {sensor}  -  {state} ({type(state.state)})")
    if state is None:
        _LOGGER.warning(f"Failed to get state for sensor: {sensor}")
        return None
    value = state.state
    if type(value) == str:
        if is_number(value):
            value = float(value)
            _LOGGER.debug(f"Sensor: {sensor}  -  {state} is ({type(value)})")
    return value

def get_sensor_attribute(self, sensor, attribute):
    state = self.hass.states.get(sensor)
    _LOGGER.debug(f"Getting attribute '{attribute}' for sensor: {sensor}  -  {state}")
    if state is None:
        _LOGGER.warning(f"Failed to get state for sensor: {sensor} when getting attribute '{attribute}'")
        return None
    value = state.attributes.get(attribute)
    if value is None:
        _LOGGER.warning(f"Failed to get attribute '{attribute}' for sensor: {sensor}")
        return None
    if type(value) == str:
        if is_number(value):
            value = float(value)
    return value


def calculate_available_current(self):
    state = {}
    try:
        state[CONF_PHASES] = get_sensor_attribute(self, "sensor." + self.config_entry.data.get(CONF_ENTITY_ID), CONF_PHASES)
    except:
        state[CONF_PHASES] = None

    state[CONF_MAIN_BREAKER_RATING] = self.config_entry.data.get(CONF_MAIN_BREAKER_RATING)
    state[CONF_INVERT_PHASES] = self.config_entry.data.get(CONF_INVERT_PHASES)
    state[CONF_CHARING_MODE] = get_sensor_data(self, self.config_entry.data.get(CONF_CHARGIN_MODE_ENTITY_ID))
    state[CONF_PHASE_A_CURRENT] = get_sensor_data(self, self.config_entry.data.get(CONF_PHASE_A_CURRENT_ENTITY_ID))
    state[CONF_PHASE_B_CURRENT] = get_sensor_data(self, self.config_entry.data.get(CONF_PHASE_B_CURRENT_ENTITY_ID))
    state[CONF_PHASE_C_CURRENT] = get_sensor_data(self, self.config_entry.data.get(CONF_PHASE_C_CURRENT_ENTITY_ID))
    state[CONF_EVSE_CURRENT_IMPORT] = get_sensor_data(self, self.config_entry.data.get(CONF_EVSE_CURRENT_IMPORT_ENTITY_ID))
    state[CONF_EVSE_CURRENT_OFFERED] = get_sensor_data(self, self.config_entry.data.get(CONF_EVSE_CURRENT_OFFERED_ENTITY_ID))
    state[CONF_MAX_IMPORT_POWER] = get_sensor_data(self, self.config_entry.data.get(CONF_MAX_IMPORT_POWER_ENTITY_ID))
    state[CONF_PHASE_VOLTAGE] = self.config_entry.data.get(CONF_PHASE_VOLTAGE)
    
    # Determine the number of phases based on individual phase currents
    phases = 0
    if state[CONF_EVSE_CURRENT_OFFERED] is not None:
        evse_attributes = self.hass.states.get(self.config_entry.data.get(CONF_EVSE_CURRENT_OFFERED_ENTITY_ID)).attributes
        for attr, value in evse_attributes.items():
            if attr.startswith('L') and is_number(value) and float(value) > 1:
                phases += 1

    # Fallback to the existing method if individual phase currents are not provided
    if phases == 0 and state[CONF_PHASES] is not None and is_number(state[CONF_PHASES]):
        phases = state[CONF_PHASES]
    if phases == 0 and (is_number(state[CONF_EVSE_CURRENT_IMPORT]) and state[CONF_EVSE_CURRENT_IMPORT] > 0) and (is_number(state[CONF_EVSE_CURRENT_OFFERED]) and state[CONF_EVSE_CURRENT_OFFERED] > 0):
        phases = min(max(round(state[CONF_EVSE_CURRENT_IMPORT] / state[CONF_EVSE_CURRENT_OFFERED], 0), 1), 3)

    voltage = 230
    if state[CONF_PHASE_VOLTAGE] is not None and is_number(state[CONF_PHASE_VOLTAGE]):
        voltage = state[CONF_PHASE_VOLTAGE]

    for key, value in state.items():
        _LOGGER.debug(f"doe_values: {key} : {value} : {type(value)}")

    if state[CONF_INVERT_PHASES]:
        state[CONF_PHASE_A_CURRENT], state[CONF_PHASE_B_CURRENT], state[CONF_PHASE_C_CURRENT] = -state[CONF_PHASE_A_CURRENT], -state[CONF_PHASE_B_CURRENT], -state[CONF_PHASE_C_CURRENT]
        
    if state[CONF_CHARING_MODE] == 'Standard':
        target_import_power = state[CONF_MAX_IMPORT_POWER]
        target_import_current = target_import_power / voltage
    else:
        target_import_power = 0
        target_import_current = 0

    phase_a_current = state[CONF_PHASE_A_CURRENT]
    phase_b_current = state[CONF_PHASE_B_CURRENT]
    phase_c_current = state[CONF_PHASE_C_CURRENT]

    phase_a_import_current = max(phase_a_current, 0)
    phase_b_import_current = max(phase_b_current, 0)
    phase_c_import_current = max(phase_c_current, 0)

    phase_a_export_current = max(-phase_a_current, 0)
    phase_b_export_current = max(-phase_b_current, 0)
    phase_c_export_current = max(-phase_c_current, 0)
    
    total_import_current = phase_a_import_current + phase_b_import_current + phase_c_import_current

    evse_current = state[CONF_EVSE_CURRENT_IMPORT]
    evse_current_per_phase = evse_current / phases


    # calculate limits
    max_import_power = state[CONF_MAX_IMPORT_POWER]
    max_import_current = max_import_power / voltage

    remaining_available_import_current = max_import_current - total_import_current
    
    remaining_available_current_phase_a = state[CONF_MAIN_BREAKER_RATING] - phase_a_current
    remaining_available_current_phase_b = state[CONF_MAIN_BREAKER_RATING] - phase_b_current
    remaining_available_current_phase_c = state[CONF_MAIN_BREAKER_RATING] - phase_c_current

    if phases == 1:
        max_evse_available = evse_current_per_phase + min(remaining_available_current_phase_a, remaining_available_import_current + phase_a_export_current)
        calc_used = "01"
    
    elif phases == 2:
        max_evse_available = evse_current_per_phase + min(remaining_available_current_phase_a, remaining_available_current_phase_b, (remaining_available_import_current + phase_a_export_current + phase_b_export_current) / 2)
        calc_used = "02"
   
    elif phases == 3:
        max_evse_available = evse_current_per_phase + min(remaining_available_current_phase_a, remaining_available_current_phase_b, remaining_available_current_phase_c, (remaining_available_import_current + phase_a_export_current + phase_b_export_current + phase_c_export_current) / 3)
        calc_used = "03"
    
    else:
        max_evse_available = self.config_entry.data.get(CONF_DEFAULT_CHARGE_CURRENT)
        calc_used = "04"
    
    # calculate target current
    if state[CONF_CHARING_MODE] == 'Standard':
        target_import_current = max_import_current
    else:
        target_import_current = 0

    remaining_available_import_current = target_import_current - total_import_current
    
    remaining_available_current_phase_a = state[CONF_MAIN_BREAKER_RATING] - phase_a_current
    remaining_available_current_phase_b = state[CONF_MAIN_BREAKER_RATING] - phase_b_current
    remaining_available_current_phase_c = state[CONF_MAIN_BREAKER_RATING] - phase_c_current

    if phases == 1:
        target_evse = evse_current_per_phase + min(remaining_available_current_phase_a, remaining_available_import_current + phase_a_export_current)
        calc_used = "01"
    
    elif phases == 2:
        target_evse = evse_current_per_phase + min(remaining_available_current_phase_a, remaining_available_current_phase_b, (remaining_available_import_current + phase_a_export_current + phase_b_export_current) / 2)
        calc_used = "02"
   
    elif phases == 3:
        target_evse = evse_current_per_phase + min(remaining_available_current_phase_a, remaining_available_current_phase_b, remaining_available_current_phase_c, (remaining_available_import_current + phase_a_export_current + phase_b_export_current + phase_c_export_current) / 3)
        calc_used = "03"
    
    else:
        target_evse = self.config_entry.data.get(CONF_DEFAULT_CHARGE_CURRENT)
        calc_used = "04"

    if state[CONF_CHARING_MODE] == 'Eco':
        target_evse = max(6, target_evse)




    state[CONF_AVAILABLE_CURRENT] = min(max_evse_available, target_evse)

    if state[CONF_AVAILABLE_CURRENT] < 6:
        state[CONF_AVAILABLE_CURRENT] = 0
    if state[CONF_AVAILABLE_CURRENT] > 16:
        state[CONF_AVAILABLE_CURRENT] = 16
    
    if state[CONF_AVAILABLE_CURRENT] > 6 and is_number(state[CONF_EVSE_CURRENT_IMPORT]) and  not state[CONF_EVSE_CURRENT_IMPORT] > 0:
        state[CONF_AVAILABLE_CURRENT] = 6
    

    return {
        CONF_AVAILABLE_CURRENT: round(state[CONF_AVAILABLE_CURRENT], 1),     # Current available based on input parameters
        CONF_PHASES: phases,                 # either a known or estimated number of phases used
        CONF_CHARING_MODE: state[CONF_CHARING_MODE],    # Charging mode selected by the user
        'calc_used': calc_used,
        'max_evse_available': max_evse_available,
    }


