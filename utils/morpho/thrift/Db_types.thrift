/**
 * @section LICENSE
 * Copyright &copy; 2012 Safran Morpho - Safran Morpho confidential - all rights reserved
 *
 * @section DESCRIPTION
 *
 *
 * @file Db_types.thrift
 *
 * CHANGELOG
 * 23 nov 2012  - Initiate header
 * 10 dec 2012  - Change namespace to comply MPH coding rules.
 * 14 dec 2012  - Change some types names to comply MPH coding rules.
 *              - Templates type is defined in Biofinger_types
 *              - Add comments.
 *              - Complete the user fields in User_DB_record.
 * 28 dec 2012  - Modified enum User_DB_fields
 *              - Added field for first name
 *              - Added field for user role
 *              - Renamed field to duress finger index
 *              - Added "Date_time_db" structure for expiry date
 * 08 jan 2013  - Update User_DB_fields enum
 * 19 jan 2013  - Added "Transaction_log_DB_fields", "Transaction_log_filter_type" enums
 *              - Added "Transaction_log_DB_record", "Transaction_log_filter" structures.
 * 25 jan 2013  - Added "Transaction_log_status" structure.
 *              - Modified "Transaction_log_DB_record" structure - Made all fields optional,
 *              - Renamed "name_fascn" to "name" and "jobcode_cve" to "jobcode" field.
 * 30 jan 2013  - Renamed "Transaction_log_DB_fields" enum variables
 * 04 feb 2013  - Modified data type of "channel" parameter to byte in "Transaction_log_DB_record" structure.
 *              - Added an optional parameter "is_final_response" in "Transaction_log_DB_record" structure.
 *              - Used DB_status structure in "Transaction_log_status" structure.
 *              - Added field error_code in "Transaction_log_DB_record" structure.
 *              - Modified data type of user_control_status to enum "Transaction_log_user_control_status".
 *              - Renamed userid to user_ID and filter to filter_type in "Transaction_log_filter" structure.
 * 12 feb 2013  - Added "Door_open_schedule" structure and modified exceptions related to schedules.
 * 14 feb 2013  - Added "Holiday_schedule" structure.
 * 05 mar 2013  - Added enum 'Data_export_type'
 *              - Added struture 'Data_export_options'
 *  			- Added exception 'Invalid_directory_path_error'
 *              - Updated structure 'Transaction_log_DB_record', 
 *                Modified type of 'user_control_status' from 'i32'to 'Transaction_log_user_control_status'
 * 07 mar 2013  - Added element in enum 'Data_export_type', added 'error_log' and 'user_database'
 *              - Updated structure 'Transaction_log_filter', 
 *                modified type of variable 'user_control_status' from 'i32' to enum 'Transaction_log_user_control_status'
 * 25 mar 2013  - 'Transaction_log_user_control_status' renamed with 'Transaction_log_action_status'
 *              - Added enumeration 'Transaction_log_action_code'
 *              - Updated structure 'Transaction_log_DB_record', modified variable type of action field to enum 'Transaction_log_action_code'
 * 05 apr 2013  - Updated enum 'Transaction_log_DB_fields', added element 'matching_score'
 *              - Updated structure 'Transaction_log_DB_record', added member 'matching_score'
 *              - Update enum 'User_type', renamed element 'biometric' to 'enrolled'
 * 08 apr 2013  - Updated enum 'Transaction_log_action_status', updated elements to 'action_fail' and 'action_pass'
 *              - Updated enum 'Transaction_log_DB_fields', added element 'user_role'
 *                Renamed element 'user_control_status' to 'action_status'
 *              - Updated enum 'Transaction_log_filter_type', renamed element 'user_control_status' to 'action_status'
 *              - Updated structure 'Transaction_log_DB_record', added member 'user_role'
 * 09 apr 2013  - Updated enum 'Transaction_log_action_status', changed value of enum elements 'action_pass' and 'action_fail'
 * 10 apr 2013  - Added structure 'Jobcode_list'
 *              - Added exceptions 'Job_code_list_array_full', 'Invalid_job_code_array_length', 'Job_code_list_data_invalid',
 *                and 'Job_code_validation_failed'
 * 15 apr 2013  - Updated structure 'Jobcode_list', made member 'jobcode_values' as optional
 * 16 apr 2013  - Updated structure 'User_DB_record', changed type of member 'job_code_list' to 'i16'
 * 15 May 2013  - Changed 'enrol' word(UK english) to 'enroll' (US english change)
 * 21 May 2013  - Added dynamic message structure.
 * 23 May 2013  - Updated enum 'Transaction_log_filter_type', added element 'log_action'
 *              - Updated structure 'Transaction_log_filter', Added member 'log_action'
 * 04 June 2013 - Changed jobcode type to i32 from string in 'Transaction_log_DB_record' structure
 *              - Added Usr_ctrl_ref and Usr_ctrl_check field in 'Transaction_log_DB_record' structure
 *              - new enum added in 'Transaction_log_DB_fields'
 * 11 June 2013 - Updated structure 'Usr_ctrl_check', added members 'face_detection_photo_check' and 'VIP_list_check'
 *              - Updated enum 'User_type', added member 'VIP_list'
 *              - Updated enum 'User_DB_fields', added member 'VIP_list_flag'
 *              - Updated structure 'User_DB_record', added member 'VIP_list_flag'
 * 14 June 2013 - 'User_access_rule' structure defined
 * 15 June 2013 - 'tlac_user_rule_check_failure' added Transaction_log_action_code
 * 22 June 2013 - Added new fields in 'Usr_ctrl_ref'
 *                user_record_ref_in_DB
 *                access_schedule_ref_in_DB
 *                holiday_schedule_ref_in_DB
 * 28 June 2013 - Updated enum 'Transaction_log_action_code'
 *                Added tlac_add_user,tlac_reboot_initiated,tlac_multi_user_intermediate_id
 * 01 July 2013 - Removed field 'external_db' from 'User_rule_reference_check'
 * 24 July 2013 - Spell correction in User_rule_trigger_check.keyboard
 *                Description added for Jobcode_list
 * 25 July 2013 - Updated structure 'Usr_ctrl_check'
 *                Added new field tna_ext_mode_check
 * 31 July 2013 - Updated enum 'User_type' added 'all' for getting all users
 * 02 Aug 2013  - Removed Internal command enums
 * 05 Aug 2013  - Changed data type of field 'action_data' in Transaction_log_DB_record structure to binary
 * 06 Aug 2013  - Updated enum 'Transaction_log_filter_type', added enum element 'photo_status'
 *              - Updated struct 'Transaction_log_filter', added member 'photo_status'
 *              - Updated struct 'Transaction_log_status', removed member 'filter_log_count'
 * 21 Aug 2013 - Updated structure 'Usr_ctrl_check'
 *                Added new field job_code_list_check
 * 11 Sept 2013 - Updated comment for field 'specific_relay_duration_in_sec'
 */

include "Biofinger_types.thrift"
include "Generic_types.thrift"

namespace cpp Distant_cmd


/**
 * Jobcode list datatype
 *
 * This will be used for the job code list load/retrieve operation
 */
struct Jobcode_list
{
    /** List number (1 to 128) */
    1: i16 list_number;
    /** List name, max name length is 128 */
    2: string list_name;
    /** Array of Job code values (0 to (2^32-1)), value is unsigned but it is declared as singed in command due to thrift data type limitation */
    3: optional list<i32> jobcode_values;
}

/** Enumeration for transaction log action code */
enum Transaction_log_action_code
{
    tlac_duress_finger_detected,
    tlac_fake_finger_detected,
    tlac_user_control_successful,
    tlac_biometric_mismatch,
    tlac_pin_mismatch,
    tlac_user_id_not_in_db,
    tlac_control_timed_out,
    tlac_rejected_by_schedule,
    tlac_temp_validity_expired,
    tlac_user_not_in_white_list,
    tlac_black_listed_card,
    tlac_face_not_detected,
    tlac_transaction_log_full,
    tlac_controller_feedback_action,
    tlac_job_code_check_failure,
    tlac_user_rule_check_failure,
    tlac_door_opened_for_too_long,
    tlac_door_forced_open,
    tlac_door_closed_after_alarm,
    tlac_door_unlocked,
    tlac_door_locked_back,
    tlac_management_menu_login,
    tlac_management_menu_logout,
    tlac_database_deleted,
    tlac_enrollment_completed,
    tlac_user_deleted,
    tlac_user_modification_completed,
    tlac_cls_card_encoded,
    tlac_cls_card_reset,
    tlac_settings_changed,
    tlac_cls_card_security_key_reset,
    tlac_security_policy_changed,
    tlac_tamper_detected,
    tlac_tamper_cleared,
    tlac_terminal_boot_completed,
    tlac_firmware_upgrade,
    tlac_add_user,
    tlac_reboot_initiated,
    tlac_multi_user_intermediate_id,
    tlac_max_code
}

struct DB_status
{
    /** Maximum number of records.*/
    1: i32      capacity;
    /** Current number of records.*/
    2: i32      size;
}

struct Transaction_log_status
{
    /** Log status */
    1: DB_status log_status;
}

/** Enumeration representing all the action status */
enum Transaction_log_action_status
{
    action_fail,
    action_pass
    // More to be defined here
}

/** Enumeration representing all the fields contained in a transaction log record.*/
enum Transaction_log_DB_fields
{
    action_status,
    date_time,
    name,
    first_name,
    channel,
    action_data,
    action,
    userid_csn,
    jobcode,
    duration,
    matched_finger,
    tna_key,
    photo,
    error_code,
    matching_score,
    user_role,
    usr_ctrl_ref,
    usr_ctrl_checks_to_do,
    usr_ctrl_checks_done
}

struct Usr_ctrl_ref 
{
    /** Control mode reference */
    1: required bool ctrl_mode_ref_in_DB;
    /** user record reference */
    2: required bool user_record_ref_in_DB;
    /** Terminal ID check reference */
    3: required bool id_check_ref_in_DB;
    /** Smartcard ID check reference */
    4: required bool id_check_ref_on_SC;
    /** Finger data reference */
    5: required bool finger_ref_in_DB;
    /** PIN data reference */
    6: required bool pin_ref_in_DB;
    /** Expiry date reference */
    7: required bool expiry_date_ref_in_DB;
    /** Access schedule data reference */
    8: required bool access_schedule_ref_in_DB;
    /** Holiday schedule data reference */
    9: required bool holiday_schedule_ref_in_DB;
}

struct Usr_ctrl_check 
{
     1: required bool id_check_DB;
     2: required bool id_check_SC;
     3: required bool bio_check;
     4: required bool pin_check;
     5: required bool usr_rule_check;
     6: required bool biopin_check;
     7: required bool face_detection_check;
     8: required bool face_detection_mandatory;
     9: required bool face_detection_photo_check;
    10: required bool white_list_check;
    11: required bool VIP_list_check;
    12: required bool stolen_SC_list_check;
    13: required bool multi_usr_check;
    14: required bool duress_check;
    15: required bool access_schedule_check;
    16: required bool holiday_schedule_check;
    17: required bool expiry_date_check;
    18: required bool tna_ext_mode_check;
    19: required bool job_code_list_check;
}

struct Transaction_log_DB_record
{
    /** User control status */
    1: optional Transaction_log_action_status action_status;
    /** Transaction time stamp */
    2: optional Generic_types.Date_time date_time;
    /** Name */
    3: optional string name;
    /** First name */
    4: optional string first_name;
    /** Channel */
    5: optional byte channel;
    /** Action data (Action specific data) values */
    6: optional binary action_data;
    /** Action */
    7: optional Transaction_log_action_code action;
    /** User ID or CSN */
    8: optional string userid_csn;
    /** Jobcode */
    9: optional i32 jobcode;
    /** Duration */
    10: optional i16 duration;
    /** Matched finger index of user */
    11: optional byte matched_finger;
    /** Time and Attendance key pressed by user (valid value 0(No Key) to 16(pressed key) ) */
    12: optional byte tna_key;
    /** Photo data of user */
    13: optional binary photo;
    /** Error code */
    14: optional i32 error_code;
    /** Matching score */
    15: optional i64 matching_score;
    /** User role */
    16: optional byte user_role;
    /** Referenced used during user control */
    17: optional Usr_ctrl_ref usr_ctrl_ref_used;
    /** Controls to do during user control */
    18: optional Usr_ctrl_check usr_ctrl_checks_to_do;
    /** Controls performed during user control */
    19: optional Usr_ctrl_check usr_ctrl_checks_done;
    /**  Flag indicating whether the response is final or intermediate */
    20: optional bool is_final_response = false;
}

/** Enumeration representing all the filters available for retrieving transaction logs.*/
enum Transaction_log_filter_type
{
    all,
    action_status,
    date_time,
    user_id,
    log_action,
    photo_status
}

struct Transaction_log_filter
{
    /** Filter type required */
    1: required Transaction_log_filter_type filter_type;
    /** User control status */
    2: optional Transaction_log_action_status action_status;
    /** Start time stamp */
    3: optional Generic_types.Date_time start_time_stamp;
    /** End time stamp */
    4: optional Generic_types.Date_time end_time_stamp;
    /** User ID */
    5: optional string user_id;
    /** Action */
    6: optional Transaction_log_action_code log_action;
    /** Photo status */
    7: optional bool photo_status;
}

/**
 * Enumeration representing the type of users in database.
 *
 * See user_DB_get_user_IDs command.
 */
enum User_type
{
    enrolled,
    white_list,
    VIP_list,
    all,
 }

/** Enumeration representing all the fields contained in a user record.*/
enum User_DB_fields
{
    name,
    first_name
    templates,
    first_finger_qual,
    second_finger_qual,
    third_finger_qual,
    first_finger_nb,
    second_finger_nb,
    third_finger_nb,
    duress_finger_index,
    schedule_nb,
    PIN_code,
    user_card_sn,
    job_code_list,
    apply_holiday_schedule,
    specific_relay_duration_in_sec,
    expiry_date,
    user_rule,
    white_list_flag,
    legacy_timemask,
    legacy_extended_id,
    user_role,
    VIP_list_flag,
    additional_data
}

/** The requested field does not exist in user database.*/
exception User_DB_unavailable_field
{
    1: required Generic_types.Generic_error_code    err_code,
    2: required User_DB_fields                      missing_fields
}

enum Dynamic_msg_type
{
    dynamic_msg_none,
    dynamic_msg_text,
    dynamic_msg_image
}

struct Dynamic_msg_DB_record
{
    1: Generic_types.Date_time start_date; ///< to hold dynamic message start date
    2: Generic_types.Date_time end_date; ///< to hold dynamic message end date
    3: string message_or_filename; ///< to hold dynamic message string
    4: Dynamic_msg_type type; ///< to hold dynamic message type
    5: bool attach_flag; ///< to hold dynamic message attach flag
}

struct User_rule_control_check
{
    /** PIN control <br> if enabled PIN control is required for user */
    1: required bool PIN_control;

    /** Finger bio reference check */
    2: required bool finger_bio_control;
}

struct User_rule_reference_check
{
    /** Terminal reference check <br> if enabled reference for user must be terminal */
    1: required bool terminal;

    /** Smartcard reference check */
    2: required bool smart_card;
}

struct User_rule_trigger_check
{
    /** Finger bio trigger check<br> if enabled Finger BIO trigger is valid source of trigger for user */
    1: required bool finger_bio;

    /** contactless card trigger check */
    2: required bool contactless;

    /** keyboard trigger check */
    3: required bool keyboard;

    /** external_port trigger check */
    4: required bool external_port;
}

struct User_access_rule
{
    /** Trigger check parameter */
    1: required User_rule_trigger_check trigger_check;

    /** reference check parameter */
    2: required User_rule_reference_check reference_check;

    /** Control check parameter */
    3: required User_rule_control_check control_check;

    /** BIO substitution */
    4: required bool allow_bio_substitution;
}
 
struct User_DB_record
{
    /** User name */
    1: optional string                  name_UTF8;
    /** First name */
    2: optional string                  first_name_UTF8;
    /**
     * Non compressed templates.<br>
     * Max number of templates per user is 3.
     */
    3: optional list<Biofinger_types.User_templates>    templates;
    /** Quality of the first enrolled finger.*/
    4: optional i16                                     first_finger_qual;
    /** Quality of the second enrolled finger.*/
    5: optional i16                                     second_finger_qual;
    /** Quality of the third enrolled finger.*/
    6: optional i16                                     third_finger_qual;
    /**
     * Number that represents the first finger enrolled.</br>
     * 1 for left little finger, up to 10 for right little finger.
     */
    7: optional byte                    first_finger_nb;
    /**
     * Number that represents the second finger enrolled.</br>
     * 1 for left little finger, up to 10 for right little finger.
     */
    8: optional byte                    second_finger_nb;
    /**
     * Number that represents the third finger enrolled.</br>
     * 1 for left little finger, up to 10 for right little finger.
     */
    9: optional byte                    third_finger_nb;
    /**
     * Index of the duress finger amoung the enrolled finger.</be>
     * From 1 to 3.
     */
    10: optional byte                   duress_finger_index;
    /** Schedule number that applies to the user.*/
    11: optional byte                   schedule_nb;
    /** UTF8 string that represents user PIN code.*/
    12: optional string                 PIN_code_UTF8;
    /** Card Serial Number (CSN) of the user card.*/
    13: optional binary                 user_card_sn;
    /** Job code list associated to a user.*/
    14: optional i16                   job_code_list;
    /** Flag to indicate if holiday schedule apply to the user.*/
    15: optional bool                   apply_holiday_schedule;
    /**
     * Specific duration for relay triggering.</br>
     * 0 for N/A (i.e. used duration from terminal configuration), else duration in seconds (from 1 to 3600 seconds).
     */
    16: optional i16                    specific_relay_duration_in_sec;
    /**
     * User expiration data.</br>
     * If according feature is enabled, after that date the user will be rejected if control is successful.
     */
    17: optional Generic_types.Date_time    expiry_date;
    /** User specific access rule.*/
    18: optional User_access_rule           access_rule;
    /** Flag to indicate if user is part of the white list.*/
    19: optional bool                       white_list_flag;
    /** MorphoAccess 2G legacy timemask.*/
    20: optional binary                     legacy_timemask;
    /** L1/Bioscrypt legacy extended ID.*/
    21: optional binary                     legacy_extended_id;
    /** Role of the user */
    22: optional byte                       user_role;
    /** Flag to indicate if user is part of the VIP list.*/
    23: optional bool                       VIP_list_flag;
    /** Customer additional data (Not used by terminal)*/
    24: optional binary                     additional_data;
}

/** No more space to create a new record. Can be because of licence.*/
exception DB_full_error
{
    1: required Generic_types.Generic_error_code err_code
}

/** The database is empty.*/
exception DB_empty_error
{
    1: required Generic_types.Generic_error_code err_code
}

/** A similar record already exists in the database.*/
exception DB_duplicate_record_error
{
    1: required Generic_types.Generic_error_code err_code
}


struct Access_schedule_slots
{
    /** Time slots of 15 mins of interval. value of slot should be between 0-96 */
    1: byte                   start_interval_1;
    /** Time slots of 15 mins of interval. value of slot should be between 0-96 */
    2: byte                   stop_interval_1;
    /** Time slots of 15 mins of interval. value of slot should be between 0-96 */
    3: byte                   start_interval_2;
    /** Time slots of 15 mins of interval. value of slot should be between 0-96 */
    4: byte                   stop_interval_2;
}

struct Access_schedule
{
    /** name of defined schedule */
    1:string                  schedule_name;
	/** Schedule index value should be between 1 to 58.
    *   Schedule 0 is never allowed schedule.Value of this schedule can not be modified.
    *   Schedule 63 is always allowed schedule.Value of this schedule can not be modified.
    *   Schedule 59 to 62 are reserved schedule.Value of this schedule can not be modified.
    */        
    2:byte                    schedule_index;
	/** Schedule weekly slots */
    3:list<Access_schedule_slots> schedule_slots;
}

struct Door_open_schedule_interval
{
    /** Time slots of 15 mins of interval. value of slot should be between 0-96 */
    1: byte                   start_interval;
    /** Time slots of 15 mins of interval. value of slot should be between 0-96 */
    2: byte                   stop_interval;
}

struct Door_open_schedule
{
    /** Door open schedule slots. Maximum 10 slots can be defined **/
    1: list<Door_open_schedule_interval> schedule_interval;
}

struct Holiday_schedule
{
    /** name of defined schedule */
    1:string                  schedule_name;
	/** Schedule index value should be between 0 to 63 */
    2:byte                    schedule_index;
	/** Start date for holiday schedule */
    3:Generic_types.Date_time  start_date;
	/** End date for holiday schedule */
    4:Generic_types.Date_time  end_date;
}

/** Invalid schedule index exception */
exception Invalid_schedule_index
{
    1: required Generic_types.Generic_error_code err_code
}

/** Invalid schedule data exception */
exception Invalid_schedule_data
{
    1: required Generic_types.Generic_error_code err_code
}

/** Schedule store exception */
exception Schedule_store_error
{
    1: required Generic_types.Generic_error_code err_code
}

/** Schedule retrieve exception */
exception Schedule_retrieve_error
{
    1: required Generic_types.Generic_error_code err_code
}

/** Job code list array full.*/
exception Job_code_list_array_full
{
    1: required Generic_types.Generic_error_code err_code
}
/** Invalid job code array length.*/
exception Invalid_job_code_array_length
{
    1: required Generic_types.Generic_error_code err_code;
    2: required i16 list_number;
}

/** Job code list data invalid.*/
exception Job_code_list_data_invalid
{
    1: required Generic_types.Generic_error_code err_code;
    2: required i16 list_number;
}
/** Job_code_validation_failed.*/
exception Job_code_validation_failed
{
    1: required Generic_types.Generic_error_code err_code
}
