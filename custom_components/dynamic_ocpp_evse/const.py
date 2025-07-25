DOMAIN = "dynamic_ocpp_evse"

# configuration keys
CONF_NAME = "name"
CONF_ENTITY_ID = "entity_id"
CONF_PHASE_A_CURRENT_ENTITY_ID = "phase_a_current_entity_id"
CONF_PHASE_B_CURRENT_ENTITY_ID = "phase_b_current_entity_id"
CONF_PHASE_C_CURRENT_ENTITY_ID = "phase_c_current_entity_id"
CONF_MAIN_BREAKER_RATING = "main_breaker_rating"
CONF_INVERT_PHASES = "invert_phases"
CONF_CHARGIN_MODE_ENTITY_ID = "charging_mode_entity_id"
CONF_EVSE_CURRENT_IMPORT_ENTITY_ID = "evse_current_import_entity_id"
CONF_EVSE_CURRENT_OFFERED_ENTITY_ID = "evse_current_offered_entity_id"
CONF_MAX_IMPORT_POWER_ENTITY_ID = "max_import_power_entity_id"
CONF_PHASE_VOLTAGE = "phase_voltage"
CONF_UPDATE_FREQUENCY = "update_frequency"
CONF_OCPP_PROFILE_TIMEOUT = "ocpp_profile_timeout"
CONF_CHARGE_PAUSE_DURATION = "charge_pause_duration"
CONF_MIN_CURRENT_ENTITY_ID = "min_current_entity_id"
CONF_MAX_CURRENT_ENTITY_ID = "max_current_entity_id"	

# sensor attributes
CONF_PHASES = "phases"
CONF_CHARING_MODE = "charging_mode"
CONF_AVAILABLE_CURRENT = "available_current"
CONF_PHASE_A_CURRENT = "phase_a_current"
CONF_PHASE_B_CURRENT = "phase_b_current"
CONF_PHASE_C_CURRENT = "phase_c_current"
CONF_EVSE_MINIMUM_CHARGE_CURRENT = "evse_minimum_charge_current"  # defaults to 6
CONF_EVSE_MAXIMUM_CHARGE_CURRENT = "evse_maximum_charge_current"  # defaults to 16
CONF_EVSE_CURRENT_IMPORT = "evse_current_import"
CONF_EVSE_CURRENT_OFFERED = "evse_current_offered"
CONF_MAX_IMPORT_POWER = "max_import_power"
CONF_MIN_CURRENT = "min_current"
CONF_MAX_CURRENT = "max_current"
CONF_EXCESS_EXPORT_THRESHOLD = "excess_export_threshold"  # Maximum allowed export before charging starts in Excess mode

# Battery support configuration constants
CONF_BATTERY_POWER_ENTITY_ID = "battery_power_entity_id"
CONF_BATTERY_SOC_ENTITY_ID = "battery_soc_entity_id"
CONF_BATTERY_SOC_TARGET_ENTITY_ID = "battery_soc_target_entity_id"
CONF_BATTERY_MAX_CHARGE_POWER = "battery_max_charge_power"  # W
CONF_BATTERY_MAX_DISCHARGE_POWER = "battery_max_discharge_power"  # W
CONF_ALLOW_GRID_CHARGING_ENTITY_ID = "allow_grid_charging_entity_id"
