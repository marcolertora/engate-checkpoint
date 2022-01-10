/**
 * @section LICENSE
 * Copyright &copy; 2012 Safran Morpho - Safran Morpho confidential - all rights reserved
 *
 * @section DESCRIPTION
 *
 *
 * @file Generic_types.thrift
 *
 * CHANGELOG
 * 23 nov 2012  - Initiate header
 * 10 dec 2012  - Change namespace to comply MPH coding rules.
 * 11 dec 2012  - Remove terminal key enum (no more keypad version).
 * 14 dec 2012  - Add comments.
 * 19 dec 2012  - Create Generic_board_type (used by Generic_Commands::terminal_get_version)
 * 03 jan 2013  - Added structure "Wiegand_or_clock_data_string_info".
 * 08 jan 2013  - Change Date_time struct to deal with integers
 *              - Add types for terminal_get_status command
 * 17 jan 2013  - Added enum "Wiegand_protocol_type"
 * 23 jan 2013  - Added structure "Ethernet_settings"
 * 24 jan 2013  - updated structure "Wiegand_or_clock_data_string_info" changed
                  type of 'wiegand_or_clock_and_data_string' to binary
 * 30 jan 2013  - Renamed variables of "Sensor_type" and "IP_protocol_type" enums.
 * 04 feb 2013  - Added Sdac_status structure
 * 07 feb 2013  - Added exceptions 'File_inexistent_error' and 'File_name_missing'
 * 16 feb 2013  - Added enum "Param_data_types".
 *              - Added structure "Parameter_range".
 * 16 feb 2013  - Renamed exception File_name_missing to File_name_missing_error
 *              - Added 'Invalid_file_extension_error', and 'File_too_large_error'
 * 16 feb 2013  - Added enum 'Date_display_format_type'
 *              - Added enum 'Time_display_format_type'
 *              - Added enum 'Time_meridian_type'
 *              - Updated structure 'Time_local_date_time_settings',
 *                made members 'date_time' and 'time_zone' as optional
 *              - Updated structure 'Time_local_date_time_settings',
 *                added members 'date_display_type', 'time_display_type' and 'time_meridian_type'
 *              - Updated structure 'Time_customed_time_zone',
 *                added members 'daylight_start_hour_of_day' and 'daylight_end_hour_of_day'
 * 18 feb 2013  - Renamed enum 'Time_meridian_type' to 'Time_hour_display_type'
 *              - Updated structure 'Time_local_date_time_settings',
 *                Renamed variable 'time_meridian_type' to 'hour_display_type'
 *              - Moved variable 'observe_daylight_saving_time' from structure 'Time_local_date_time_settings' to
                  structure 'Time_time_zone'
 *              - Modified "Parameter_range" structure
 *              - Added "Integer_range" structure
 * 20 feb 2013  - Added enum 'Terminal_reset_settings_type'
 *              - Added enum 'Terminal_peripherals'
 * 21 feb 2013  - Added structure 'Terminal_settings_options' to be used for get terminal configuration command
 *              - Added enums 'Ip_version_type' and 'Network_interface_type'
 * 23 feb 2013  - Added "WIFI_network_status" structure
 * 24 feb 2013  - Added "WIFI_module_not_connected" exception
 * 26 feb 2013  - Added PNG image support in enum Picture_format
 * 01 Mar 2013  - Added "WIFI_mode" in WIFI_configuration_info and WIFI_network_status structure.
 * 05 Mar 2013  - Added struct 'Product_info'
 *              - Added enum 'Product_info_type'
 * 13 Mar 2013  - Added enum "Event_ID" and structure "Event_config".
 * 13 Mar 2013  - Added exception "Ethernet_config_not_found" and "Ethernet_configuration_failed".
 * 14 Mar 2013  - Added strutct 'NTP_server_config'.
 * 15 mar 2013  - Add Wifi settings structure in Terminal_configuration
 *              - Change Ethernet_settings to IP_settings
 *              - Add Wifi in Terminal_settings_type
 *              - Remove WIFI ID of connection
 * 18 Mar 2013  - clock_n_data_id, trigger_TTLX of structure "Event_config" made optional
 *              - Rea-dd possibility to distinguish IPv4 from IPv6 parameters
 *              - Reuse existing structure for IP type
 *              - Provide GPRS in IP_channel
 *              - Provide GPRS in Terminal_settings_type
 *              - Added Ip_version_type in place of IP_protocol_type in IP_settings as IP_protocol_type contains "all" enumeration.
 * 25 Mar 2013  - Updated enumeration 'Generic_error_code'
 *              - Added exceptions 'No_space_left_on_device' and 'Not_compatible_with_current_license'
 * 26 Mar 2013  - Added enumeration 'Product_type'
 *              - Updated 'Terminal_info' structure
 * 28 Mar 2013  - Added structure 'Video_phone_params'
 *              -     and exceptions 'Invalid_IP_error', and 'Invalid_size_error'
 * 08 Apr 2013  - Updated enum 'Day_in_week', renamed element 'thirsday' to 'thursday'
 *              - Changed datatype of Video_phone_params.port from i32 to i16'
 * 10 apr 2013  - Updated enum 'Generic_error_code', added new error codes 'err_job_code_validation_failed', 'err_job_code_list_data_invalid',
 *                'err_invalid_job_code_array_length' and 'err_job_code_list_array_full'
 *              - Updated map 'Generic_error_msg_map' added string mapping for error codes 'err_job_code_validation_failed', 'err_job_code_list_data_invalid',
 *                'err_invalid_job_code_array_length' and 'err_job_code_list_array_full'
 * 15 Mar 2013  - removed strutct 'NTP_server_config'.
 * 18 Apr 2013  - Added enum f_key_type for internal command set_fkey for setting fkey in TNA. 
 * 30 Apr 2013  - Added following for serial parameters' get/set:
 *                    enums: Serial_protocol_type, Communication_system_type, Baud_rate
 *                    struct: Serial_params_settings
 *              - Accordingly modified enum Terminal_settings_type and struct Terminal_configuration
 * 06 May 2013  - Added exception Invalid_wiegand_string,Invalid_get_wiegand_timeout_value,Invalid_get_wiegand_port_id,Wiegand_input_disabled,Wiegand_output_disabled.
 * 09 May 2013  - Updated enum 'Date_display_format_type', renamed its elements.
 * 15 May 2013  - Changed 'enrol' word(UK english) to 'enroll' (US english change)
 * 22 May 2013  - Added exception 'Invalid_file'.
 * 23 May 2013  - Removed exception 'Wiegand_input_disabled', 'Invalid_get_wiegand_port_id and 'Invalid_get_wiegand_timeout_value'
 *              - Updated enum 'Generic_error_code', removed elements err_wiegand_input_disabled, err_wiegand_invalid_timeout_value and
 *                err_wiegand_invalid_port_id
 *              - Removed structure 'Wiegand_or_clock_data_string_info'
 * 27 May 2013  - Added enumerations named 'Protocol_host', 'Data_bits', 'Parity_bits' and 'Stop_bits'
 *              - Added structures named 'IP_host_config', 'Serial_host_config' and 'Host_configuration'
 *              - Added exception named 'Host_not_found'
 * 28 May 2013  - Renaming 'ip_restrain_list' to 'authorized_IP_list' in enum 'Terminal_reset_settings_type'
 * 30 May 2013  - Added 'host_name', 'preferred_DNS_address' and 'alternate_DNS_address' in 'IP_settings' structure
 * 19 Jun 2013  - Added enum 'Verify_result_code'
 * 22 Jun 2013  - Updated enum 'Verify_result_code'
 *                Added verify_result_ko_holiday_schedule_data_not_found,
 *                verify_result_ko_access_schedule_data_not_found
 *                verify_result_ko_user_expiry_data_not_found
 * 28 Jun 2013  - Updated enum 'Verify_result_code'
 *                Renamed 'verify_result_ko_multi_user_duplicate_id' to 'verify_result_ok_multi_user_duplicate_id'
 *              - Update enum 'Generic_error_code' 
 *                Added err_unknown
 * 19 Jul 2013  - Updated Terminal_reset_settings_type
 * 20 Jul 2013  - Structure 'Serial_params_settings' changed
 *              - Enum 'Serial_protocol_type' removed
 */
/** (continuing in another comments section as above comments section is too large for Thrift compiler)
 * 25 Jul 2013  - Updated enum 'Verify_result_code'
 *                Added verify_result_ko_bio_pin_timed_out,
 *                verify_result_ko_bio_pin_not_exists
 *                verify_result_ko_bio_pin_mismatch
 *                verify_result_ko_F_key_timeout
 *                verify_result_ko_F_key_canceled
 *              - Added exception 'License_not_found'
 *              - Updated enum 'Generic_error_code' and 'Generic_error_msg_map', added enum element 'err_license_not_found'
 *              - Added exception 'SD_card_not_found'
 *              - Updated enum 'Generic_error_code' and 'Generic_error_msg_map', added enum element 'err_sd_card_not_found'
 * 27 Jul 2013  - Updated Terminal_info
 *                Added 'is_sd_card_detected' field
 * 02 Aug 2013  - Removed Internal command enums
 * 06 Aug 2013  - Removed 'Terminal_status'
 *                Updated enum 'Terminal_peripherals'
 *                Added wifi, sd_card, gprs
 * 14 Aug  2013 - Removed firmware upgrade command
 * 16 Aug 2013  - Updated enum 'Terminal_reset_settings_type', renamed enum element 'contactless_keys' to 'crypto_keys'
 * 07 Oct 2013  - Updated Struct 'Variant', added binary_value parameter
 * 25 Dec 2013  - Added exception 'Generic_error'
 * 26 Dec 2013  - Added enum 'Capability'
 */

namespace cpp Distant_cmd

/** Enumeration for capabilities */
enum Capability
{
    // File sizes
    max_file_size_video = 0,
    max_file_size_audio,
    max_file_size_picture,
    max_file_size_stolen_card_list,
    max_file_size_language,
    max_file_size_SSL_component,
    
    // File extensions
    file_ext_video,
    file_ext_audio,
    file_ext_picture,
    file_ext_language,
    file_ext_SSL_component
    
    // File upload chunk size
    max_file_upload_chunk_size
    
    // Users
    max_user_DB_records,
}

/**
 * \brief Enum representing verify result codes
*/
enum Verify_result_code
{
   verify_result_ok = 0,
   verify_result_ok_multi_user_intermediate_id,
   verify_result_ok_multi_user_duplicate_id,
   verify_result_ko_user_trigger_mismatch,
   verify_result_ko_user_reference_mismatch,
   verify_result_ko_user_pin_timed_out,
   verify_result_ko_user_pin_not_exists,
   verify_result_ko_user_pin_mismath,
   verify_result_ko_holiday_scheduled,
   verify_result_ko_holiday_schedule_data_not_found,
   verify_result_ko_user_not_scheduled,
   verify_result_ko_access_schedule_data_not_found,
   verify_result_ko_user_bio_expired,
   verify_result_ko_user_expiry_data_not_found,
   verify_result_ko_user_bio_not_detected,
   verify_result_ko_user_bio_canceled,
   verify_result_ko_user_bio_mismatch,
   verify_result_ko_user_bio_not_found,
   verify_result_ko_user_bio_fake_finger_detected,
   verify_result_ko_user_bio_moist_finger,
   verify_result_ko_user_bio_misplaced_finger,
   verify_result_ko_user_bio_unsupported_format,
   verify_result_ko_user_bio_incompatible_ref_error,
   verify_result_ko_user_not_in_white_list,
   verify_result_ko_face_not_detected,
   verify_result_ko_job_code_list_not_exists,
   verify_result_ko_job_code_check_failure,
   verify_result_ko_job_code_timed_out,
   verify_result_ko_bio_pin_timed_out,
   verify_result_ko_bio_pin_not_exists,
   verify_result_ko_bio_pin_mismatch,
   verify_result_ko_F_key_timeout,
   verify_result_ko_F_key_canceled
}

/**
 * Structure for holding video phone related parameters
 */
struct Video_phone_params
{
    /**
     * Name of the profile
     */
    1: required string name,

    /**
     * The IP address to call to
     */
    2: required string address_IP,

    /**
     * The port to connect to at the given IP address
     */
    3: required i16 port
}

/**
 * \brief Enum representing data-types of parameters
 */
enum Param_data_types
{
    db_integer = 0,
    db_unsigned_int = 1,
    db_binary = 5,
    db_string = 6
}

/**
 * Structure containing minimum and maximum values for integer
 * and unsigned integer parameters.
 */
struct Integer_range
{
    /**
     * Minimum value in case if range is continuous for eg: "0:10" (min_value = 0)
     */
    1: i32 min_value,

    /**
     * Maximum value in case if range is continuous for eg: "0:10" (max_value = 10)
     */
    2: i32 max_value
}

/**
 * Range shall be defined by the data type of the parameter.
 */
struct Parameter_range
{
    /** Data type of the parameter */
    1: required Param_data_types data_type,

    /**
     * Available only if value of Param_data_types is "db_integer" and "db_unsigned_int"
     */
    2: optional Integer_range continuous_range,

    /**
     * Length of the buffer
     * Available only if value of Param_data_types is "db_binary" and "db_string"
     */
    3: optional i32 max_length,

    /**
     * List of discontinuous values. For eg: If range is "1,3,5,7,9"
     * Available only if value of Param_data_types is "db_integer" and "db_unsigned_int"
     */
    4: optional list<i32> discontinuous_range
}

/**
 * A generic datatype
 *
 *
 * It is the generic datatype that might be used, for instance, as MA5G configuration parameter.<br>
 * Note that only one of the values of interest shall be filled in.
 */
struct Variant
{
    1: optional byte byte_value,
    2: optional i16 int16_value,
    3: optional i32 int32_value,
    4: optional i64 int64_value,
    5: optional double double_value,
    6: optional bool bool_value,
    7: optional string UTF8string_value,
    8: optional binary binary_value
}

/**
 * A structure to deal with date and time
 */
struct Date_time
{
    /** Year */
    1: i16  year;
    /** Month */
    2: i16  month;
    /** Day */
    3: i16  day;
    /** Hour */
    4: i16  hour;
    /** Minute */
    5: i16  minute;
    /** Second */
    6: i16  second;
}

/**
 * Generic error codes
 */
enum Generic_error_code
{
    err_unknown,
    err_size_invalid,
    err_size_negative,
    err_size_zero,
    err_buffer_overflow,
    err_buffer_underflow,
    err_config_inexistent_parameter,
    err_config_invalid_value,
    err_core_inexistent_user_id,
    err_core_timeout,
    err_core_out_of_memory,
    err_security_default_password,
    err_WIFI_module_not_connected,
    err_no_space_left_on_device,
    err_not_compatible_with_current_license,
    err_ethernet_config_not_found,
    err_ethernet_configuration_failed,
    err_job_code_validation_failed,
    err_job_code_list_data_invalid,
    err_invalid_job_code_array_length,
    err_job_code_list_array_full,
    err_wiegand_invalid_wiegand_string,
    err_wiegand_output_disabled,
	err_host_not_found,
	err_license_not_found,
	err_sd_card_not_found
}

/** Enumeration representing the month in a year */
enum Month_in_year
{
    january = 1,
    february,
    march,
    april,
    may,
    june,
    july,
    august,
    september,
    october
    november,
    december
}

/** Enumeration representing the day in week */
enum Day_in_week
{
    monday = 1,
    tuesday,
    wednesday,
    thursday,
    friday,
    saturday,
    sunday
}

struct Time_customed_time_zone
{
    /** Offset from UTC in quarter of hour*/
    1: required i32 UTC_offset_in_quarter,
    /**
     * Number representing the month that starts the daylight saving time.<br>
     * Not set if terminal uses predefined timezone.
     */
    2: optional Month_in_year daylight_start_month,
    /**
     * Number representing the weekday that starts the daylight saving time.<br>
     * Not set if terminal uses predefined timezone.
     */
    3: optional Day_in_week daylight_start_day_in_week,
    /**
     * Number representing the week number in month (1 to 4) where daylight saving time starts.<br>
     * Not set if terminal uses predefined timezone.
     */
    4: optional byte daylight_start_week_in_month,
    /**
     * Number representing the hour of day (0 to 23) where daylight saving time starts.<br>
     * Not set if terminal uses predefined timezone.
     */
    5: optional i16 daylight_start_hour_of_day,
    /**
     * Number representing the month that ends the daylight saving time.<br>
     * Not set if terminal uses predefined timezone.
     */
    6: optional Month_in_year daylight_end_month,
    /**
     * Number representing the weekday that ends the daylight saving time.<br>
     * Not set if terminal uses predefined timezone.
     */
    7: optional Day_in_week daylight_end_day_in_week,
    /**
     * Number representing the week number in month (1 to 4) where daylight saving time ends.<br>
     * Not set if terminal uses predefined timezone.
     */
    8: optional byte daylight_end_week_in_month,
    /**
     * Number representing the hour of day (0 to 23) where daylight saving time ends.<br>
     * Not set if terminal uses predefined timezone.
     */
    9: optional i16 daylight_end_hour_of_day
}

struct Time_time_zone
{
    /** Set to true if daylight saving time shall be handled*/
    1: required bool observe_daylight_saving_time,
    /**
     * Name of a predefined timezone (Europe/Paris for example).<br>
     * Not set if terminal uses customized time zone.
     */
    2: optional string predefined_time_zone_UTF8,
    /**
     * Customized time zone.<br>
     * Not set if terminals uses predefined time zone.
     */
    3: optional Time_customed_time_zone customed_time_zone
}

/** Enumeration representing the date display type */
enum Date_display_format_type
{
    mm_slash_dd_slash_yyyy,// MM/DD/YYYY 
    dd_slash_mm_slash_yyyy,// DD/MM/YYYY
    mmm_dash_dd_dash_yy,// MMM-DD-YY
    dd_dash_mmm_dash_yy,// DD-MMM-YY
    yyyy_slash_mm_slash_dd // YYYY/MM/DD
}

/** Enumeration representing the time display type */
enum Time_display_format_type
{
    hh_colon_mm_colon_ss,//HH:MM:SS
    hh_colon_mm_dot_ss //HH:MM.SS
}

/** Enumeration representing the time meridian type */
enum Time_hour_display_type
{
    time_12_hour,
    time_24_hour
}

struct Time_local_date_time_settings
{
    /** Date and time in DDMMYY format*/
    1: optional Date_time date_time,
    /**
     * Structure defining the terminal time zone<br>
     * Can use predefined or customized time zone
     */
    2: optional Time_time_zone time_zone,
    /** Number representing date display format type */
    3: optional Date_display_format_type date_display_type,
    /** Number representing time display format type */
    4: optional Time_display_format_type time_display_type,
    /** Number representing time meridian type */
    5: optional Time_hour_display_type hour_display_type
}

// /** The types of the serial protocolcommunication system */
//enum Serial_protocol_type
//{
//    /** RS-422 serial protocol */
//    RS422,
//    /** RS-485 serial protocol */
//    RS485
//}   

/** The types of the communication system */
enum Communication_system_type
{
    /** Half-duplex communication */
    half_duplex, 
    /** Full-duplex communication */
    full_duplex,
}

/** The baud rates supported */
enum Baud_rate
{
    baud_9600 = 9600,
    baud_19200 = 19200,
    baud_38400 = 38400,
    baud_57600 = 57600,
    baud_115200 = 115200
}

/** The data bits supported */
enum Data_bits
{
    /** 7 characters */
    data_bits_7 = 7,
    /** 8 characters */
    data_bits_8 = 8
}

/** Parity supported */
enum Parity_bits
{
    /** no parity bit */
    no_parity = 0,
    /** odd parity bit */
    odd_parity = 1,
    /** even parity bit */
    even_parity = 2
}

/** Stop bits supported */
enum Stop_bits
{
    /** 1 stop bit */
    stop_bits_1 = 1,
    /** 2 stop bits */
    stop_bits_2 = 2
}

/** Settings for serial channel */
struct Serial_params_settings
{
//    /** The serial protocol */
//    1: optional Serial_protocol_type serial_protocol,
    
    /** The baud rate for the serial protocol */
    1: optional Baud_rate baud,

    /** Data bits or character size */
    2: optional Data_bits char_size,

    /** Parity supported */
    3: optional Parity_bits parity,

    /** Stop bits supported */
    4: optional Stop_bits stop_bit,

    /** The kind of communication system used by the serial channel this instance represents */
    5: optional Communication_system_type communication_system,
    
    /** The net ID for the terminal */
    6: optional i16 net_id,
}

enum IP_channel
{
    ethernet,
    wifi,
    gprs
}

enum Ip_version_type
{
    ip_v4,
    ip_v6
}

struct IP_settings
{
    /** Specify for which IP channel the configuration apply for*/
    1: required IP_channel channel,
    /** IPV4 address or IPV6 address configuration*/
    2: required Ip_version_type ip_version,
    /** Set to true if dynamic IP configuration else set to false for static IP configuration*/
    3: required bool is_dhcp_mode,
    /** If static IP configuration then value of IP address to be set*/
    4: optional string ip_address,
    /** If static IP configuration then value of netmask(IPV4)/prefix_length(IPV6) to be set*/
    5: optional string net_mask_or_prefix_len,
    /** If static IP configuration then value of default gateway to be set*/
    6: optional string gateway_address
	/** Device host name*/
    7: optional string host_name
	/** preferred DNS server address*/
    8: optional string preferred_DNS_address
	/** alternate DNS server address*/
    9: optional string alternate_DNS_address
}

struct Sdac_status
{
    /** SDAC mode : 0=Off, 1=On*/
    1: required i32 mode;
    /** Relay state : 0=Door unlocked, 1=Door locked */
    2: optional i32 relay_state;
    /** Door status : 0=Open, 1=Closed, -1=Error */
    3: optional i32 door_status;
    /** Request to exit state : 0=Off, 1=On, -1=Error */
    4: optional i32 req_to_exit_state;
}

enum Terminal_settings_type
{
    date_time,
    ip,
    wifi_cfg,
    gprs_cfg,
    serial_params_cfg
}

/** enum for WIFI encryption type */
enum WIFI_encryption_type
{
    enc_none,
    enc_wep,
    enc_wpa_psk,
    enc_wpa2_psk
}

struct WIFI_network_info
{
    /** SSID address */
    1: optional string SSID,

    /** BSSID address*/
    2: optional string BSSID,

    /** Frequency of ssid */
    3: optional i16 frequency,

    /** Signal level of ssid */
    4: optional i16 signal_level,

    /** Encryption type enum */
    5: optional WIFI_encryption_type enc_type
}

struct WIFI_settings
{
    1: WIFI_network_info wifi_info

    /**
     * Security key (password) of WIFI SSID.
     * Write Only value (i.e. can not be read)
     */
    2: optional string password,

    /**
     * WEP key index of SSID.
     * Write Only value (i.e. can not be read)
     */
    3: optional byte wep_key_index,
}

/** Enumeration of available distant session state*/
enum IP_protocol_type
{
    ipv4,
    ipv6,
    all
}

struct Terminal_configuration_type
{
    1: required Terminal_settings_type settings_type,
    2: optional Ip_version_type ip_version,
    3: optional IP_channel ip_channel,
}

struct Terminal_configuration
{
    1: optional Time_local_date_time_settings date_time_settings,
    2: optional IP_settings ip_settings
    3: optional WIFI_settings wifi_settings
    4: optional Serial_params_settings serial_params
}

/** List of the settings that can be reset.*/
enum Terminal_reset_settings_type
{
    /** Configuration parameters modified by config_set_params command */
    configuration_parameters,
    /** Date and Time settings: date, time, timezone, display format */
    date_time,
    /** Ethernet settings */
    ethernet,
    /** Serial settings */
    serial,
    /** Wifi settings */
    wifi,
    /** video_phone_params settings */
    video_phone,
    /** crypto keys (includes contactless and RSA keys) */
    crypto_keys,
    /** Passwords */
    passwords,
    /** SSL components */
    ssl_components,
    /** Stolen card list */
    stolen_card_list,
    /** Job code lists */
    job_code_lists,
    /** Access schedules */
    access_schedules,
    /** Holiday schedules */
    holiday_schedules,
    /** Door schedule */
    door_schedule,
    /** authorized IP list */
    authorized_IP_list,
    /** Logs */
    logs,
    /** Passphrases */
    passphrases,
    /** Language files */
    languages,
    /** Multimedia files (video, audio, pictures...) */
    multimedia_files,
    /** User database */
    user_db,
    /** White list */
    white_list,
    /** Dynamic message */
    dynamic_msg,
    /** VIP list */
    vip_list,
    /** Event setting */
    events
}

/** List of the terminal peripherals.*/
enum Terminal_peripherals
{
    screen,
    keyboard,
    camera,
    microphone,
    speaker,
    contactless_reader_mifare_desfire,
    contactless_reader_iclass,
    contactless_reader_prox,
    sensor_cbi,
    wifi,
    sd_card,
    gprs
}

/** Enumeration of available picture interface for capture feature.*/
enum Picture_interface
{
    front_camera,
    screen
}

/** Enumeration of available picture format for capture and display features.*/
enum Picture_format
{
    JPEG,
    BMP,
    PNG
}

struct XY_coordinates
{
    /** Horizontal coordinate of a point*/
    1: required i16 x,
    /** Vertical coordinate of a point*/
    2: required i16 y
}


/** enum for protocol type */
enum Wiegand_protocol_type
{
    wiegand,
    clock_and_data
}

        /** Enumeration of available distant session state*/
        enum Distant_session_state
        {
    opened,
    closed
        }

/** Enumaration of board type*/
enum Generic_firmware_type
{
    terminal_firmware,
    sensor_firmware
}

/** struct of Product info*/
struct Product_info
{
    /** UTF8 string that represents 10 digit terminal part number of packaged product */
    1: optional string terminal_packaged_part_number_UTF8,
    /** UTF8 string that represents 14 digit terminal serial number of packaged product */
    2: optional string terminal_packaged_serial_number_UTF8,
    /** UTF8 string that represents terminal commercial name */
    3: optional string terminal_packaged_comm_name_UTF8,
    /** UTF8 string that represents 10 digit sensor part number of packaged product */
    4: optional string sensor_packaged_part_number_UTF8,
    /** UTF8 string that represents 14 digit sensor serial number of packaged product */
    5: optional string sensor_packaged_serial_number_UTF8,
    /** UTF8 string that represents 10 digit product specific part number */
    6: optional string specific_part_number_UTF8,
    /** UTF8 string that represents license identifier */
    7: optional string license_identifier_UTF8,
    /** UTF8 string that represents license name */
    8: optional string license_name_UTF8,
    /** UTF8 string that represents MAC address of Ethernet */
    9: optional string mac_address_ethernet_UTF8,
    /** UTF8 string that represents MAC address of WiFi */
    10: optional string mac_address_wifi_UTF8,
    /** UTF8 string that represents MAC address of 3G modem */
    11: optional string mac_address_3g_modem_UTF8
}

/** Enumeration of info type*/
enum Product_info_type
{
    /** 10 digit number that represents terminal part number of packaged product */
    terminal_packaged_part_number,
    /** 14 digit number that represents terminal serial number of packaged product */
    terminal_packaged_serial_number,
    /** String that represents terminal descriptive name of packaged product */
    terminal_packaged_comm_name,
    /** 10 digit number that represents sensor part number of packaged product */
    sensor_packaged_part_number,
    /** 14 digit number that represents sensor serial number of packaged product */
    sensor_packaged_serial_number,
    /** 10 digit number that represents product specific part number */
    specific_part_number,
    /** String that represents license identifier */
    license_identifier,
    /** String that represents license name */
    license_name,
    /** String that represents MAC address of Ethernet */
    mac_address_ethernet,
    /** String that represents MAC address of WiFi */
    mac_address_wifi,
    /** String that represents MAC address of 3G modem */
    mac_address_3g_modem
}

/**
 * \brief Structure representing per event configuration
 */
struct Event_config
{
    /** Event enable/disable flag */
    1: required bool enable,
    /** Event sending to controller flag */
    2: required bool send_to_controller,
    /** Event ID for clock n data */
    3: optional string clock_n_data_id,
    /** Event sending over TTL0 enable/disable flag */
    4: optional bool trigger_TTL0,
    /** Event sending over TTL1 enable/disable flag */
    5: optional bool trigger_TTL1,
    /** Event sending over TTL2 enable/disable flag */
    6: optional bool trigger_TTL2,
}

/** Enum host protocol */
enum Protocol_host
{
    /** normal TCP channel */
    prot_TCP,
    /** UDP protocol */
    prot_UDP,
    /** secure TCP channel */
    prot_SSL 
}

/**
 * \brief Structure contains IP host configuration data
 */
struct IP_host_config
{
    /** controller IP address */
    1: required string ip_address,

    /** controller port number, range (1:65000) */
    2: required i32 port,
    
    /** timeout for connection, read and write */
    3: required i32 timeout,

    /** protocol to use for IP channel, range (1:65000) */
    4: required Protocol_host protocol
}

/**
 * \brief Structure contains serial host configuration data
 */
struct Serial_host_config
{
    /** The baud rate for the serial protocol */
    1: required Baud_rate baud,
    
    /** The kind of communication system used by the serial channel */
    2: required Communication_system_type communication_system,
    
    /** Databits to use */
    3: required Data_bits char_size,
    
    /** Parity bits to use */
    4: required Parity_bits parity,
    
    /** Stop bits to use */
    5: required Stop_bits stopbits
}

/**
 * Configurations of the host on which the data needs to be send 
 */
struct Host_configuration
{
    /** IP host configuration if data needs to be sent on IP channel*/
    1: optional IP_host_config ip_host_conf,
    
    /** serial host configuration if data needs to be sent on serial channel*/
    2: optional Serial_host_config serial_host_conf
}

/** A map that translates error code into string.*/
const map< Generic_error_code, string > Generic_error_msg_map =
{
        Generic_error_code.err_unknown                               : "Unknown error",
        Generic_error_code.err_size_invalid                          : "Invalid size",
        Generic_error_code.err_size_negative                         : "Size is negative"
        Generic_error_code.err_size_zero                             : "Size is zero",
        Generic_error_code.err_buffer_overflow                       : "Buffer Underflow",
        Generic_error_code.err_buffer_underflow                      : "Buffer Overflow",
        Generic_error_code.err_config_inexistent_parameter           : "Inexistent configuration parameter",
        Generic_error_code.err_config_invalid_value                  : "Invalid configuration parameter value",
        Generic_error_code.err_core_inexistent_user_id               : "Inexistent User ID",
        Generic_error_code.err_core_timeout                          : "Operation timed out",
        Generic_error_code.err_core_out_of_memory                    : "Out of memory",
        Generic_error_code.err_security_default_password             : "Default password detected",
        Generic_error_code.err_WIFI_module_not_connected             : "WIFI module not connected",
        Generic_error_code.err_no_space_left_on_device               : "No space left on device",
        Generic_error_code.err_not_compatible_with_current_license   : "Not compatible with current license",
        Generic_error_code.err_ethernet_config_not_found             : "Ethernet configuration not found",
        Generic_error_code.err_ethernet_configuration_failed         : "Failed to configure ethernet settings",
        Generic_error_code.err_job_code_validation_failed            : "job code validation failed",
        Generic_error_code.err_job_code_list_data_invalid            : "job code list data invalid",
        Generic_error_code.err_invalid_job_code_array_length         : "invalid job code array length",
        Generic_error_code.err_job_code_list_array_full              : "job code list array full",
		Generic_error_code.err_host_not_found                        : "Send to host failed",
        Generic_error_code.err_license_not_found                     : "License not found",
        Generic_error_code.err_sd_card_not_found                     : "SD card not found"
}
/** The specified user ID does not exist.*/
exception Inexistent_user_id_error
{
    1: required Generic_error_code err_code,
    2: required string user_id_UTF8
}

exception Out_of_memory_error
{
    1: required Generic_error_code err_code
}

/** Command reaches the timeout.*/
exception Timeout_error
{
    1: required Generic_error_code err_code
}

/** One command argument can not be interpreted.*/
exception Invalid_argument_error
{
    1: required Generic_error_code err_code;
    2: optional string what_UTF8;
}

/** The command was cancelled by distant command.*/
exception Cancelled_error
{
    1: required Generic_error_code err_code
}

exception Security_default_password
{
    1: required Generic_error_code err_code
}

exception File_inexistent_error
{
    1: required Generic_error_code err_code;
    2: optional string what_UTF8;
}

exception File_name_missing_error
{
    1: required Generic_error_code err_code;
    2: optional string what_UTF8;
}

exception Invalid_file_extension_error
{
    1: required Generic_error_code err_code;
    2: optional string what_UTF8;
}

exception File_too_large_error
{
    1: required Generic_error_code err_code;
    2: optional string what_UTF8;
}

exception WIFI_module_not_connected
{
    1: required Generic_error_code err_code;
    2: optional string what_UTF8;
}

exception Ethernet_config_not_found
{
    1: required Generic_error_code err_code;
    2: optional string what_UTF8;
}

exception Ethernet_configuration_failed
{
    1: required Generic_error_code err_code;
    2: optional string what_UTF8;
}

exception Invalid_IP_error
{
    1: required string what_UTF8
}

exception Invalid_size_error
{
    1: required string what_UTF8
}

exception Invalid_wiegand_string
{
    1: required Generic_error_code err_code
}

exception Wiegand_output_disabled
{
    1: required Generic_error_code err_code
}

exception Host_not_found
{
	1: required Generic_error_code err_code
}
exception License_not_found
{
    1: required Generic_error_code err_code
}
exception SD_card_not_found
{
    1: required Generic_error_code err_code
}

/** The exception encompassing other general exceptions */
exception Generic_error
{
    1: required Generic_error_code err_code;
    2: optional string what_UTF8;
}
