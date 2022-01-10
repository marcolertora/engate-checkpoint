/**
 * @section LICENSE
 * Copyright &copy; 2012 Safran Morpho - Safran Morpho confidential - all rights reserved
 *
 * @section DESCRIPTION
 *
 *
 * @file Generic_commands.thrift
 *
 * CHANGELOG
 * 23 nov 2012  - Initiate header
 * 30 nov 2012  - Add cancel exception in get_key command
 *              - Change parameter of config_get_params from set type to list type
 * 10 dec 2012  - Change namespace to comply MPH coding rules.
 * 11 dec 2012  - Add terminal_echo command
 *              - Change return type of terminal_get_key command
 *              - Change service name to comply MPH coding rules.
 * 14 dec 2012  - Change Biofinger_enroll return type.
 *              - Change type names to comply MPH coding rules.
 * 18 dec 2012  - Add enable_intermediate_replies in enroll command.
 * 19 dec 2012  - Create terminal_get_version command.
 * 03 jan 2013  - Changed return type of user_DB_delete_users from void to
 *                map<string, bool> containing delete status of user list.
 *              - Added command "get_wiegand_or_clock_data_string".
 * 08 jan 2013  - Add types for terminal_get_status command
 * 09 jan 2013  - Update biofinger_authenticate_ref to specify the type of the reference templates.
 *              - user_DB_get_all_user_IDs is renamed to user_DB_get_user_IDs to be able to get all
 *                the user IDs of biometric database or all user IDs in white list
 * 14 jan 2013  - get_wiegand_or_clock_data_string -> wiegand_clock_data_get_string
 * 16 jan 2013  - Added command to get IP restraining list in form of string list.
 * 18 jan 2013  - Added command to delete IP from IP restraining list.
 * 18 jan 2013  - Added command wiegand_clock_data_send_string for sending wiegand or clock&data string.
 * 18 jan 2013  - Added commands of security password.
 * 19 jan 2013  - Added command "transaction_log_retrieve"
 *              - Added command "transaction_log_delete_all"
 *              - Added command "transaction_logs_retrieve_info"
 * 21 jan 2013  - Added command of reset parameters to factory settings.
 * 24 jan 2013  - updated argument type to binary in command"wiegand_clock_data_send_string"
 * 25 jan 2013  - Added command "transaction_log_get_status".
 *              - Renamed command "transaction_log_retrieve_info" to "transaction_log_get_fields".
 * 30 jan 2013  - Add enable_intermediate_replies parameter in Terminal_get_key command
 * 04 feb 2013  - Changed return type of get_sdac_status() function to Sdac_status structure.
 * 07 feb 2013  - Added command "retrieve_touchscreen_input".
 *              - Added get access schedule commands.
 *              - Added set access schedule commands.
 *              - Added reset access schedule commands.
 *              - Modified signatures of 'file_get', 'file_load', 'file_get_filenames', and 'file_erase' commands.
 * 12 feb 2013  - Added door open schedule commands
 *              - Modified access schedule commands and related exceptions.
 * 14 feb 2013  - Added Holiday schedule commands
 * 16 feb 2013  - Added "config_get_range" command.
 * 16 feb 2013  - Changed signature of 'file_get', and 'file_load'
 * 18 feb 2013  - Changed return type of "config_get_range" command.
 * 20 feb 2013  - Added  "configure_WIFI_network" and "scan_WIFI_networks" command.
 *              - Added "trigger_relay" command.
 *              - Modified command "reset_factory_settings".
 *              - Added "terminal_retrieve_peripherals" command.
 *              - Added "terminal_change_threat_level" command.
 * 21 feb 2013  - Added parameter in API get_terminal_configuration to retrieve interface name and IP version.
 * 21 feb 2013  - Modified parameter of function 'get_terminal_configuration'
 * 22 feb 2013  - Updated signature of 'file_get' to remove enabling of multiple chunks -- chunking is mandatory
 * 23 feb 2013  - Added "get_WIFI_network_status" command
 * 24 feb 2013  - Modified wifi related functions for thowring exception "WIFI_module_not_connected" exception
 * 05 mar 2013  - Added exceptions in commands: 'transaction_log_retrieve', 'terminal_set_configuration'
 *              - Removed intermediate repy required option from command 'transaction_log_retrieve'
 *              - Added "product_get_info" command.
 *              - Added "cls_write_admin_card" command.
 *              - Added "terminal_set_brightness" command.
 *              - Removed "modify_password" and "store_password" and added "password_set" command.
 *              - Renamed "verify_password" command to "password_verify" and modified it.
 *              - Renamed "delete_password" command to "password_reset" and modified it.
 *              - Removed "modify_passphrase", "store_passphrase" and "verify_passphrase" and added "passphrase_set" command.
 *              - Renamed "delete_passphrase" command to "passphrase_reset" and modified it.
 * 13 mar 2013  - Added commands for Event configuration settings. "set_events_configuration", "get_events_configuration" and 		"reset_events_configuration"
 * 13 mar 2013  - Exception added in "terminal_get_configuration" and "terminal_set_configuration"
 * 13 mar 2013  - "password_set" command's arguement changed to 2 arguements. 1. password_old 2. password_new
 *				- removed command "set_cryptographic_key"
 *              - renamed command "modify_cryptographic_key" to "cryptographic_key_set"
 *              - renamed command "delete_cryptographic_key" to "cryptographic_key_reset"
 * 14 mar 2013  - "password_verify", "Security_default_password" exception added.
 *              - "passphrase_set", "Security_default_password" exception added.
 * 14 mar 2013  - Added 'NTP_server_config' & 'get_NTP_server_configuration' commands.
 * 15 mar 2013  - Add cls_authenticate_user
 *              - Change Terminal_settings_option parameter to Terminal_settings_type in terminal_get_configuration
 * 18 mar 2013  - Rename "set_events_configuration" and "get_events_configuration" into "events_set_config" and "events_get_config"
 *              - removed "reset_event_configuration"
 *              - Added licences (get,set) commands.
 *              - Added "cls_keys_load" and "cls_keys_reset" commands.
 *              - Removed "modify_cryptographic_key", "store_cryptographic_key", "verify_cryptographic_key" and "delete_cryptographic_key" commands.
 *              - Added Out_of_memory exception to Terminal_echo command
 *              - Added "cls_authenticate_user" command.
 *              - Change in terminal_get_configuration, Terminal_settings_type to Terminal_configuration_type
 * 25 mar 2013  - Added exception in command 'transaction_log_get_status'
 * 28 mar 2013  - Added commands 'config_set_video_phone_params' and 'config_get_video_phone_params'exception
 * 05 apr 2013  - Updated command 'user_DB_get_status', added argument user type
 * 10 apr 2013  - Added commands 'job_code_load_lists', 'job_code_retrieve_lists', 'job_code_check_value_against_user',
 *                'job_code_empty_lists' and 'job_code_remove_all_lists'
 * 15 apr 2013  - removed 'NTP_server_config' & 'get_NTP_server_configuration' commands.
 * 15 apr 2013  - Added command 'job_code_retrieve_list_indices'
 * 16 apr 2013  - Added exception in command 'job_code_retrieve_lists'
 * 06 may 2013	- Added exception in command wiegand_clock_data_get_string & wiegand_clock_data_send_string
 * 09 may 2013  - Updated command 'user_DB_get_users', added exception 'Generic_types.Invalid_argument_error'
 * 15 May 2013  - Changed 'enrol' word(UK english) to 'enroll' (US english change)
 * 21 May 2013  - Added "display_text" command.
 * 21 May 2013  - Added set/get/reset dynamic message data commands.
 * 22 May 2013  - Renamed "retrieve_touchscreen_input" to "retrieve_keypad_input"
 * 23 May 2013  - Removed command 'wiegand_clock_data_get_string'
 * 27 May 2013  - Added command 'send_to_host'
 *              - Added flag in 'user_db_set_users' to bypass similar finger check to improve the template transfer performance.
 * 17 June 2013 - Modified argument of access_schedule_retrieve, access_schedule_delete, holiday_schedule_retrieve ,holiday_schedule_delete
 */

/** (continuing in another comments section as above comments section is too large for Thrift compiler)
 * 28 May 2013  - Renaming:
 *                         From                          To
 *                  get_ip_restrain_list        authorized_IP_get_list
 *                  add_ip_restrain             authorized_IP_add
 *                  delete_ip_restrain          authorized_IP_delete
 *                  get_ip_restrain_range_list  authorized_IP_get_range_list
 *                  add_ip_restrain_range       authorized_IP_add_range
 *                  delete_ip_restrain_range    authorized_IP_delete_range
 * 19 Jun 2013  - Added command 'external_db_verify_id'.
 * 19 Jun 2013  - Modified command name from 'external_db_verify_id' to 'external_db_verify_user'
 * 20 Jun 2013  - Added exception 'Duplicated_finger_error' and 'DB_duplicate_record_error' in command 'user_DB_set_users'.
 * 24 Jun 2013  - Modified command external_db_verify_user, added user id as input argument
 * 27 Jun 2013  - Added exception 'Invalid_argument_error' in 'PIN_authenticate_db' command to return error if parameters are invalid.
 * 20 July 2013 - Removed 'terminal_change_threat_level' distant command.
 *              - Modified 'licence' to 'license' in commands for spell correction.
 *              - Remove list of files from cls_write. Those files are now in card description
 * 25 July 2013 - Updated command 'password_reset' and 'password_set'
 *                used enum for passphrase ID
 *              - Removed exception 'Security_default_password' from 'password_set' command
 *              - Added argument 'l1_keys' in command 'cls_keys_load'
 *              - Added exception 'License_not_found' in command 'config_set_params'
 *              - Added exception 'SD_card_not_found' in command 'licenses_add'
 *              - Removed "terminal_set_brightness" command.
 * 30 July 2013 - Added exception 'License_not_found' in wifi related commands
 *              - Added exception 'Invalid_argument_error' in picture display command
 * 31 July 2013 - Added exception Timeout_error in command retrieve_keypad_input to fix jira bug 606
 * 02 Aug  2013 - Added exception 'SD_card_not_found' in command 'config_set_params'
 *                Added exception 'SD_card_not_found' in dynamice messages related commands
 *              - Added exception '' for following commands:
 *                'file_load', 'file_get', 'file_erase'
 * 06 Aug 2013  - Removed command 'terminal_get_status'
 * 07 Aug 2013  - Polling command comment updated
 * 14 Aug 2013  - Removed firmware upgrade command
 * 16 Aug 2013  - Updated command 'cls_keys_load', replaced all arguments by 'crypto_keys'
 *              - Renamed command 'cls_keys_load' to 'key_load'
 *              - Renamed command 'cls_keys_reset' to 'key_reset'
 * 27 Aug 2013  - Added comments in command 'file_load'
 * 12 Sep 2013  - Added comments in command 'retrieve_language_file_list'
 * 12 Sep 2013  - Removed command 'terminal_get_key'
 * 18 Oct 2013  - Added supported events configuration table in command 'events_set_config'
 * 26 Oct 2013  - Thrift auto generation for csharp cannot parse 6000 character long line so broken comment in several lines for command 'events_set_config'
 * 26 Oct 2013  - Added comment in command 'cls_write_user_card' that it supports only pkcompv2 template data only
 * 20 Dec 2013  - Added command 'dynamic_message_get_user_IDs' to get list of User IDs having dynamic message
 * 26 Dec 2013  - Added exception 'Generic_error' in 'throws' section of every command
 * 26 Dec 2013  - Added command 'get_terminal_capabilities'
 */

include "Generic_types.thrift"
include "Config_types.thrift"
include "Biofinger_types.thrift"
include "Db_types.thrift"
include "Cls_types.thrift"
include "File_types.thrift"
include "Security_types.thrift"

namespace cpp Distant_cmd

service Generic_commands
{

    /**************************************************
    * Job code commands
    **************************************************/
   /**
    * To load one or more job code lists
    *
    * This command will add job code list and if list is already
    * exist then it will update the list
    */
   void job_code_load_lists(
                       /** List number to be created */
                       1: list<Db_types.Jobcode_list> list_values)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** List data is not valid */
                2: Db_types.Job_code_list_data_invalid jc_invalid_list_ex,
                /** List array full, no more list can be added */
                3: Db_types.Job_code_list_array_full jc_list_full_ex,
                /** Invalid job code array size */
                4: Db_types.Invalid_job_code_array_length jc_invalid_array_length_ex);
   /**
    * To retrieve one or more job code lists data
    *
    * @return The job code list array.
    */
   list<Db_types.Jobcode_list> job_code_retrieve_lists(
                                               /** List numbers to be retrieved */
                                               1: set<i16> list_numbers)
               throws (
                       /** Generic exception */
                       1: Generic_types.Generic_error generic_xcept
                       /** List number is not valid */
                       2: Db_types.Job_code_list_data_invalid jc_invalid_list_ex);

   /**
    * To retrieve all job code list number and name
    *
    * @return All job code list number and name.
    */
    list<Db_types.Jobcode_list> job_code_retrieve_list_indices()
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );

   /**
    * Job code value validate against user
    *
    */
   void job_code_check_value_against_user(
                               /** User ID for which job code is to be checked */
                               1: string user_id,
                               /** Job code value to be validated */
                               2: i32 jobcode_value)
                   throws (
                           /** Generic exception */
                           1: Generic_types.Generic_error generic_xcept
                           /** List number is not valid */
                           2: Db_types.Job_code_validation_failed jc_validation_failed_ex);

   /**
    * To remove one or more job code lists
    * @return Map of list number to the delete status, if successful then 'true'
    */
   map<i16, bool> job_code_empty_lists(/** List array to be removed */
                               1: set<i16> list_numbers)
                               throws (
                                       /** Generic exception */
                                       1: Generic_types.Generic_error generic_xcept
                               );

   /**
    * To remove all job code lists
    *
    */
   void job_code_remove_all_lists()
       throws (
               /** Generic exception */
               1: Generic_types.Generic_error generic_xcept
       );



    /**************************************************
     * Transaction log commands
     **************************************************/

    /**
     * Command to get the transaction log status.
     *
     * @return Transaction log status values.
     *
     */
    Db_types.Transaction_log_status transaction_log_get_status
    (
        /** Filter to be applied for getting transaction log count as per filter.*/
        1: Db_types.Transaction_log_filter                  filter
    )
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid parameter set */
                2: Generic_types.Invalid_argument_error invalid_arg_xcept
        );

    /**
     * Command to retrieve the transaction log entries.
     *
     * This command is multi response command. It will give data in multiresponse.
     * @return List of the transaction log entries as per the filter applied.<br></br>
     * <b>Functionality change required in Thrift generated client code (C++ sample)</b><br>
     * <pre>
     * void Generic_commandsClient::transaction_log_retrieve(std::vector< ::Distant_cmd::Transaction_log_DB_record> & _return, const  ::Distant_cmd::Transaction_log_filter& filter, const std::set< ::Distant_cmd::Transaction_log_DB_fields::type> & required_fields)
     * {
     *     send_transaction_log_retrieve(filter, required_fields);
     *     <span style="color:green">// recv_transaction_log_retrieve(_return); // Original line in the generate code</span>
     * &nbsp;
     *     <span style="color:green">// BEGIN: Custom section for receiving and processing intermediate data</span>
     *     uint32_t loop_id = 0;
     *     while (true)
     *     {
     *         recv_transaction_log_retrieve (_return);
     * &nbsp;
     *         <span style="color:green">// Check if the perticular data chunk is final or not.
     *         //If it is the final data chunk, the data will be returned in normal way not as callback.</span>
     *         if (_return.empty() || _return[_return.size() - 1].is_final_response)
     *         {
     *             break;
     *         }
     *         else
     *         {
     *             <span style="color:green">// If the data chunk is not final, the data chunk will be returned as callback function manner
     *             // Following is the client's callaback, if set, assumed to take necessary action on the received data,
     *             // e.g. Do process (store somewhere in file or memory) the retrieved transaction log chunk as other chunks are yet to be received.</span>
     *             if (Multiresponse_handler::client_tlog_command)
     *             {
     *                 Multiresponse_handler::client_tlog_command(_return);
     *             }
     *         }
     *     }
     *     <span style="color:green">// END: Custom section for receiving and processing intermediate data</span>
     * }
     * </pre>
     */
    list<Db_types.Transaction_log_DB_record> transaction_log_retrieve
    (

        /** Filter to be applied for retrieving transaction logs.*/
        1: Db_types.Transaction_log_filter          filter,

        /** List of the transaction log fields to be retrieved */
        2: set<Db_types.Transaction_log_DB_fields>  required_fields
    )
    throws (
            /** Generic exception */
            1: Generic_types.Generic_error generic_xcept
            /** Invalid parameter set */
            2: Generic_types.Invalid_argument_error invalid_arg_xcept
           );


    /**
     * Command to delete all the transaction log entries.
     */
    void transaction_log_delete_all()
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


    /**
     * Gets the available fields in the transaction log records
     *
     * @return The list of available transaction log record fields.
     */
    set<Db_types.Transaction_log_DB_fields> transaction_log_get_fields()
                                       throws (
                                               /** Generic exception */
                                               1: Generic_types.Generic_error generic_xcept
                                       );


    /**************************************************
     * Configuration commands
     **************************************************/

    /**
     * Returns a list of name of all terminal parameters
     */
     set<string>    config_get_all_params_name()
                                       throws (
                                               /** Generic exception */
                                               1: Generic_types.Generic_error generic_xcept
                                       );


    /**
     * Returns a list of values corresponding to requested parameters
     */
    list<Generic_types.Variant> config_get_params(  /** List of UTF8 string representing names of requested parameters */
                                                    1: list<string> param_list_UTF8)
            throws (
                    /** Generic exception */
                    1: Generic_types.Generic_error generic_xcept
                    /** A requested parameter does not exist in terminal */
                    2: Config_types.Config_inexistent_parameter_error inexistant_param_xcept);

    /**
     * Set requested parameters with given values
     */
    void config_set_params( /**
                             * List of key-value pairs.<br>
                             * Parameters are represented by a UTF8 string
                             */
                            1: map<string, Generic_types.Variant> param_map)
            throws (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** A requested parameter does not exist in terminal*/
                        2: Config_types.Config_inexistent_parameter_error   inexistant_param_xcept,
                        /** A parameter value is rejected by the terminal*/
                        3: Config_types.Config_invalid_value_error          invalid_value_xcept,
                        /** License not found exception */
                        4: Generic_types.License_not_found license_not_xcept,
                        /** SD card not found */
                        5:Generic_types.SD_card_not_found    sd_card_not_found_xcept);

    /**
     * Get the value range of the required or all configuration parameters.
     *
     */
    map<string, Generic_types.Parameter_range> config_get_range( /**
                                                                  * List of key-value pairs.<br>
                                                                  * Parameters are represented by a UTF8 string
                                                                  */
                                                                  1: list<string> param_keys)
    throws (
            /** Generic exception */
            1: Generic_types.Generic_error generic_xcept
            /** A requested parameter does not exist in terminal */
            2: Config_types.Config_inexistent_parameter_error inexistant_param_xcept);

    /**************************************************
     * Biometric commands
     **************************************************/
    /**
     * Use data contained in a contactless card to authenticate an user (biometric and/or PIN and/or BIOPIN check)<br><br>
     * <b>Functionality change required in Thrift generated client code (C++ sample)</b><br>
     * Similar to the <a href=#SampleBiofingerIdentify>C++ sample code</a> provided for the method <code>biofinger_identify</code>
     */
     Cls_types.cls_authent_user_reply cls_authenticate_user(    /**
                                                                  * Max. duration of Smartcard detection process<br>
                                                                  * 0 implies an infinite process.
                                                                  */
                                                                1: i32      timeout_in_sec,
                                                                /** Contactless authentication parameters */
                                                                2: Cls_types.cls_authent_user_params authent_param)
            throws (
                    /** Generic exception */
                    1: Generic_types.Generic_error generic_xcept
                    /** No finger or card was detected during process*/
                    2: Generic_types.Timeout_error              timeout_xcept,
                    /** Invalid parameter*/
                    3: Generic_types.Invalid_argument_error     invalid_argument_xcept,
                    /** Command is cancelled by distant command*/
                    4: Generic_types.Cancelled_error            cancelled_xcept,
                    /** Finger was misplaced or withdrawn during acquisition*/
                    5: Biofinger_types.Misplaced_finger_error   misplaced_finger_xcept);

    /**
     * Identify an user using its finger against the terminal database
     *
     * The reference templates are stored in one (and only one) specified record.<br>
     * The search template is compared to all the templates found in the database
     *
     * <b>Warning:</b> If @a enable_intermediate_replies is true, you will need a modified version of the Thrift client that supports
     *          the reception of several T_REPLY messages for one command.<br><br>
     * <b id="SampleBiofingerIdentify">Functionality change required in Thrift generated client code (C++ sample)</b><br>
     * <pre>
     * void Generic_commandsClient::biofinger_identify(::Distant_cmd::Biofinger_control_operation_reply& _return,
     *         const int8_t database_id, const int32_t timeout_in_sec, const int8_t threshold,
     *         const bool enable_intermediate_replies, const ::Distant_cmd::Biofinger_control_optional_param& optional_param)
     * {
     *     send_biofinger_identify(database_id, timeout_in_sec, threshold, enable_intermediate_replies, optional_param);
     *     <span style="color:green">// recv_biofinger_identify(_return); // Original line in the generated code</span>
     * &nbsp;
     *     <span style="color:green">// BEGIN: Custom section for receiving and processing intermediate data</span>
     *     uint32_t loop_id = 0;
     *     while (true)
     *     {
     *         <span style="color:green">// receive intermediate response</span>
     *         recv_biofinger_identify(_return);
     * &nbsp;
     *         <span style="color:green">// check for final_result status</span>
     *         if (_return.__isset.final_result)
     *         {
     *             break; <span style="color:green">// if final_result callback, break from loop</span>
     *         }
     *         else if (_return.__isset.cb_bio_command) <span style="color:green">// check for interested callback</span>
     *         {
     *             _return.__isset.cb_bio_command = false; <span style="color:green">// reset the callback flag</span>
     *             if (Multiresponse_handler::client_cb_bio_command)
     *             {
     *                 <span style="color:green">// process callback data</span>
     *                 Multiresponse_handler::client_cb_bio_command(_return.cb_bio_command);
     *             }
     *         }
     *         else if (_return.__isset.cb_low_resol_live_image)
     *         {
     *             <span style="color:green">// Process similar to "if (_return.__isset.cb_bio_command)" block</span>
     *         }
     *         else if (_return.__isset.cb_high_resol_capture_image)
     *         {
     *             <span style="color:green">// Process similar to "if (_return.__isset.cb_bio_command)" block</span>
     *         }
     *         else if (_return.__isset.cb_capture_quality)
     *         {
     *             <span style="color:green">// Process similar to "if (_return.__isset.cb_bio_command)" block</span>
     *         }
     *         else if (_return.__isset.cb_live_quality)
     *         {
     *             <span style="color:green">// Process similar to "if (_return.__isset.cb_bio_command)" block</span>
     *         }
     *     }
     *     <span style="color:green">// END: Custom section for receiving and processing intermediate data</span>
     * }
     * </pre>
     */
     Biofinger_types.Biofinger_control_operation_reply biofinger_identify(  /** Database identifier */
                                                                            1: byte     database_id,
                                                                            /**
                                                                             * Max. duration of identification process<br>
                                                                             * 0 implies an infinite process.
                                                                             */
                                                                            2: i32      timeout_in_sec,
                                                                            /**
                                                                             * This parameter specifies the value of the False Acceptance Ratio (FAR) of the MorphoSmart\99 device.<br>
                                                                             * The value of this parameter can be set from 0 to 10, by 1 value steps.
                                                                             */
                                                                            3: byte     threshold,
                                                                            /**
                                                                             * If set to false, you will receive only one reply containing the final result of the
                                                                             * identification, otherwise you may also receive asynchronous replies containing the
                                                                             * progress status of the identification.
                                                                             */
                                                                            4: bool enable_intermediate_replies,
                                                                            /** Identification optional parameters */
                                                                            5: Biofinger_types.Biofinger_control_optional_param optional_param)
            throws (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** The user database is empty.*/
                        2: Db_types.DB_empty_error                  DB_empty_xcept,
                        /** No finger was detected during process*/
                        3: Generic_types.Timeout_error              timeout_xcept,
                        /** Invalid parameter*/
                        4: Generic_types.Invalid_argument_error     invalid_argument_xcept,
                        /** Command is cancelled by distant command*/
                        5: Generic_types.Cancelled_error            cancelled_xcept,
                        /** Finger was misplaced or withdrawn during acquisition*/
                        6: Biofinger_types.Misplaced_finger_error   misplaced_finger_xcept);

    /**
     * Authenticates an user using its finger against its database references
     *
     *
     * The reference templates are stored in one (and only one) specified record.<br>
     * The search template is compared to all the templates found in the specified record
     * (the number of fingerprint templates depends on the database format).
     *
     *
     * <b>Warning:</b> If @a enable_intermediate_replies is true, you will need a modified version of the Thrift client that supports
     *          the reception of several T_REPLY messages for one command.<br><br>
     * <b>Functionality change required in Thrift generated client code (C++ sample)</b><br>
     * Similar to the <a href=#SampleBiofingerIdentify>C++ sample code</a> provided for the method <code>biofinger_identify</code>
     */
    Biofinger_types.Biofinger_control_operation_reply biofinger_authenticate_db(    /** Database identifier */
                                                                                    1: byte     database_id,
                                                                                    /**
                                                                                     * Max. duration of authentication process<br>
                                                                                     * 0 implies an infinite process.
                                                                                     */
                                                                                    2: i32      timeout_in_sec,
                                                                                    /**
                                                                                     * This parameter specifies the value of the False Acceptance Ratio (FAR) of the MorphoSmart\99 device.<br>
                                                                                     * The value of this parameter can be set from 0 to 10, by 1 value steps.
                                                                                     */
                                                                                    3: byte     threshold,
                                                                                    /** User ID to authenticate (UTF8 string)*/
                                                                                    4: string user_id_UTF8,
                                                                                    /**
                                                                                     * If set to false, you will receive only one reply containing the final result of the
                                                                                     * authentication, otherwise you may also receive asynchronous replies containing the
                                                                                     * progress status of the authentication.
                                                                                     */
                                                                                    5: bool enable_intermediate_replies
                                                                                    /** Authentication optional parameters */
                                                                                    6: Biofinger_types.Biofinger_control_optional_param optional_param)
            throws (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** The specified user ID has not been found in the database.*/
                        2: Generic_types.Inexistent_user_id_error   inexistant_user_xcept
                        /** The user database is empty.*/
                        3: Db_types.DB_empty_error                  DB_empty_xcept,
                        /** No finger was detected during process*/
                        4: Generic_types.Timeout_error              timeout_xcept,
                        /** Invalid parameter*/
                        5: Generic_types.Invalid_argument_error     invalid_argument_xcept,
                        /** Command is cancelled by distant command*/
                        6: Generic_types.Cancelled_error            cancelled_xcept,
                        /** Finger was misplaced or withdrawn during acquisition*/
                        7: Biofinger_types.Misplaced_finger_error   misplaced_finger_xcept);

    /**
     * <b>Functionality change required in Thrift generated client code (C++ sample)</b><br>
     * Similar to the <a href=#SampleBiofingerIdentify>C++ sample code</a> provided for the method <code>biofinger_identify</code>
     */
    Biofinger_types.Biofinger_control_operation_reply biofinger_authenticate_ref(   /**
                                                                                     * Max. duration of authentication process<br>
                                                                                     * 0 implies an infinite process.
                                                                                     */
                                                                                    1: i32          timeout_in_sec,
                                                                                    /**
                                                                                     * This parameter specifies the value of the False Acceptance Ratio (FAR) of the MorphoSmart\99 device.<br>
                                                                                     * The value of this parameter can be set from 0 to 10, by 1 value steps.
                                                                                     */
                                                                                    2: byte         threshold,
                                                                                    /**
                                                                                     * List of reference templates<br>
                                                                                     * The templates can be in any format handled by the terminal<br>
																					 * Max number of templates per list is 20
                                                                                     */
                                                                                    3: list<Biofinger_types.User_templates> ref_template_list,
                                                                                    /**
                                                                                     * If set to false, you will receive only one reply containing the final result of the
                                                                                     * authentication, otherwise you may also receive asynchronous replies containing the
                                                                                     * progress status of the authentication.
                                                                                     */
                                                                                    4: bool enable_intermediate_replies
                                                                                    /** Authentication optional parameters */
                                                                                    5: Biofinger_types.Biofinger_control_optional_param optional_param)
            throws (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** A reference template is not supported by the terminal*/
                        2: Biofinger_types.Unsupported_format_error unsupported_format_xcept
                        /** A reference template does not match sensor security policy */
                        3: Biofinger_types.Incompatible_ref_error   incomptible_ref_xcept,
                        /** No finger was detected during process*/
                        4: Generic_types.Timeout_error              timeout_xcept,
                        /** Invalid parameter*/
                        5: Generic_types.Invalid_argument_error     invalid_argument_xcept,
                        /** Command is cancelled by distant command*/
                        6: Generic_types.Cancelled_error            cancelled_xcept,
                        /** Finger was misplaced or withdrawn during acquisition*/
                        7: Biofinger_types.Misplaced_finger_error   misplaced_finger_xcept);

    /**
     * Captures user fingers, optionally stores them in terminal database,
     * and/or returns finger templates, and/or returns fingerprint images.
     *
     *
     * The template is calculated after three finger acquisitions (the user has to put each finger three times on the sensor).<br>
     * To obtain the best accuracy, users are advised to use the fore, the thumb or the middle fingers.<br><br>
     * <b>Functionality change required in Thrift generated client code (C++ sample)</b><br>
     * Similar to the <a href=#SampleBiofingerIdentify>C++ sample code</a> provided for the method <code>biofinger_identify</code>
     */
    Biofinger_types.Biofinger_enroll_operation_reply biofinger_enroll(/**
                                                                         * Database identifier<br>
                                                                         * That parameter is useless if the function does not store in terminal database
                                                                         */
                                                                        1: byte                                             database_id,
                                                                        /**
                                                                         * Max. duration of authentication process<br>
                                                                         * 0 implies an infinite process. Allowed range is 0 - 65535 seconds
                                                                         */
                                                                        2: i32                                              timeout_in_sec,
                                                                        /**
                                                                         * This function can create a new record in terminal user database,
                                                                         * or can return the captured templated, or can perform both.
                                                                         */
                                                                        3: Biofinger_types.Enrollment_type                   enrollment_type,
                                                                        /**
                                                                         * Number of fingers to enroll.
                                                                         * It can be 1, 2 or 3 fingers.
                                                                         */
                                                                        4: byte                                             nb_of_finger,
                                                                        /**
                                                                         * User ID to enroll<br>
                                                                         * That parameter is useless if the function does not store in terminal database
                                                                         */
                                                                        5: string                                           user_id_UTF8,
                                                                        /**
                                                                         * The user's data to store along with templates<br>
                                                                         * That parameter is useless if the function does not store in terminal database
                                                                         */
                                                                        6: Db_types.User_DB_record                          user_fields,
                                                                        /**
                                                                         * If set to false, you will receive only one reply containing the final result of the
                                                                         * enrollment, otherwise you may also receive asynchronous replies containing the
                                                                         * progress status of the enrollment.
                                                                         */
                                                                        7: bool                                             enable_intermediate_replies,
                                                                        /** Enrollment optional parameter */
                                                                        8: Biofinger_types.Biofinger_enroll_optional_param   optional_param)
            throws  (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** A captured template does not match sensor security policy */
                        2: Biofinger_types.Incompatible_ref_error   incompatbile_ref_xcept,
                        /** No finger was detected during process*/
                        3: Generic_types.Timeout_error              timeout_xcept,
                        /** Invalid parameter*/
                        4: Generic_types.Invalid_argument_error     invalid_argument_xcept,
                        /** Command is cancelled by distant command*/
                        5: Generic_types.Cancelled_error            cancelled_xcept,
                        /** User ID already exists in terminal database*/
                        6: Db_types.DB_duplicate_record_error       duplicate_record_xcept,
                        /** Failure due to missing available space in the database*/
                        7: Db_types.DB_full_error                   DB_full_xcept,
                        /** The user record is containing a field which is not supported by the terminal database */
                        8: Db_types.User_DB_unavailable_field       unavailable_field_xcept,
                        /** User uses a finger more than once*/
                        9: Biofinger_types.Duplicated_finger_error  duplicated_finger_xcept);

    /**
     * Authenticates an user using its PIN code stored in terminal database
     *
     *
     * User has to enter a PIN code on the terminal keypad.
     *
     *
     * @return True, if the code keyed by the user matches the database user's PIN code, otherwise false.
     */
    bool PIN_authenticate_db(   /**
                                 * Max. duration of authentication process<br>
                                 * Limited to 60s.
                                 */
                                1: i32      timeout_in_sec,
                                /** User ID to authenticate (UTF8 string)*/
                                2: string   user_id_UTF8)
    throws (
            /** Generic exception */
            1: Generic_types.Generic_error generic_xcept
            /** Tried to enroll using duplicate fingers*/
            2: Generic_types.Invalid_argument_error invalid_argument_xcept);

    /**
     * Reset selected parameters to factory settings.
     *
     */
    void reset_factory_settings(   /** List of the settings to reset.*/
                                    1: list<Generic_types.Terminal_reset_settings_type> list_of_settings)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


    /**************************************************
     * User database commands
     **************************************************/

    /**
     * Gets the user's database status
     *
     * @return The database capacity and number of records.
     */
    Db_types.DB_status user_DB_get_status(/** Type of user to retrieve status*/
                                      1: Db_types.User_type type)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


    /**
     * Gets the available fields
     *
     *
     * This command returns the list of available user fields in the terminal database.
     *
     * @return The list of available user fields.
     */
    set<Db_types.User_DB_fields> user_DB_get_fields()
                                       throws (
                                               /** Generic exception */
                                               1: Generic_types.Generic_error generic_xcept
                                       );


    /**
     * Adds or modify one or more user records in the database
     *
     *
     * Only the fields which are present in the DB_record structure will be modified.
     *
     * <b>Warning:</b> If the command is used to set non compressed templates, they all shall be of the same type.
     *  users list should be limited to 100 entries otherwise terminal may misbehave.
     */
    void user_DB_set_users( /** Mapping of User IDs (UTF8 string) to their database fields*/
                            1: map<string, Db_types.User_DB_record> users
							/**
                              * If set to true,  checks  on  reference  templates  are performed:  same  finger  cannot  be  used  twice,<br>
                              * and  the  person  must  not  be  already  enrolled.<br>
                              * If set to false, these checks are not performed.<br>
                              * This  option  is  useful  to  reduce  the  time  taken  to  fill  large databases.<br>
                              * In this case, the database coherence must be previously checked.
                              */
                            2: bool   enable_similar_finger_check)
            throws (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** Not all of the user records have been added or modified due to missing available space in the database*/
                        2: Db_types.DB_full_error               DB_full_xcept,
                        /** One of the user record is containing a field which is not supported by the terminal database */
                        3: Db_types.User_DB_unavailable_field   unavailable_field_xcept,
                        4: Generic_types.Invalid_argument_error invalid_argument_xcept,
                        /** Tried to enroll using duplicate fingers*/
                        5: Biofinger_types.Duplicated_finger_error duplicate_finger_xcept,
                        /** Other user is already enrolled using the same fingers*/
                        6: Db_types.DB_duplicate_record_error duplicate_user_xcept);

    /**
     * Deletes one or more user record from the terminal database
     *
     *
     * <b>Warning:</b> If a user is not found, no error is reported.
     */
    map<string, bool> user_DB_delete_records(   /** User IDs (UTF8 string) of records to delete*/
                                                1: set<string> user_IDs_UTF8)
                                                throws (
                                                        /** Generic exception */
                                                        1: Generic_types.Generic_error generic_xcept
                                                );


    /**
     * Deletes all user records from the terminal database
     */
    void user_DB_delete_all_records()
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


    /**
     * Returns one or more user records.
     *
     *
     * <b>Warning:</b> The list of user ID shall be limited to 100 items max.
     *
     *
     * @return A map of UserIDs and their corresponding records.<br>
     *         If a user_IDs is not found, it will not be present in the map.
     */
    map<string, Db_types.User_DB_record> user_DB_get_users( /** List of User IDs to return*/
                                                            1: set<string>                      user_IDs_UTF8,
                                                            /**
                                                             * Fields to return in the DB_record structure. It can be empty if you just
                                                             * want to check for a User ID presence.
                                                             */
                                                            2: set<Db_types.User_DB_fields> requested_fields)
                                                   throws (
                                                           /** Generic exception */
                                                           1: Generic_types.Generic_error generic_xcept
                                                           /** Invalid argument*/
                                                           2: Generic_types.Invalid_argument_error invalid_argument_xcept);




    /**
     * Returns the list of all user IDs (UTF8 string) present in terminal database based on user type
     *
     * @note For the moment, only the users ID of users in biometric database or in white list can be retrieved.
     */
    set<string> user_DB_get_user_IDs( /** Kind of user to retrieve*/
                                      1: Db_types.User_type type)
                                      throws (
                                              /** Generic exception */
                                              1: Generic_types.Generic_error generic_xcept
                                      );



    /**************************************************
     * Dynamic message commands
     **************************************************/

	/**
	 * Set dynamic message of users.
	 *
	 * <b>Warning:</b> Dynamic messages list should be limited to 500 entries otherwise terminal may misbehave.
	 */
	void dynamic_message_set( /** Mapping of User IDs (UTF8 string) to their dynamic message database fields*/
	                             1: map<string, Db_types.Dynamic_msg_DB_record> dm_list)
	                         throws (
                                 /** Generic exception */
                                 1: Generic_types.Generic_error generic_xcept
	                             /** Invalid argument*/
	                             2: Generic_types.Invalid_argument_error invalid_argument_xcept,
                                 /** SD card not found */
                                 3:Generic_types.SD_card_not_found    sd_card_not_found_xcept);

	/**
	 * Get dynamic message of users.
	 *
	 * <b>Warning:</b> User IDs list should be limited to 500 entries otherwise terminal may misbehave.
	 *
	 * @return The list of read files/data
	 */
	map<string, Db_types.Dynamic_msg_DB_record> dynamic_message_get( /** Set of User IDs to return*/
	                                                                 1: set<string> user_IDs_UTF8)
	                                                             throws (
	                                                                     /** Generic exception */
	                                                                     1: Generic_types.Generic_error generic_xcept
                                                                         /** Invalid argument*/
                                                                         2: Generic_types.Invalid_argument_error invalid_argument_xcept,
                                                                         /** SD card not found */
                                                                         3:Generic_types.SD_card_not_found    sd_card_not_found_xcept);

	/**
	 * Reset dynamic message data of users.
	 *
	 */
	void dynamic_message_reset( /** Set of User IDs whose dynamic message have to be reset*/
	                            1: set<string> user_IDs_UTF8)
	                        throws (
                                /** Generic exception */
                                1: Generic_types.Generic_error generic_xcept
                                /** Invalid argument*/
                                2: Generic_types.Invalid_argument_error invalid_argument_xcept,
                                /** SD card not found */
                                3:Generic_types.SD_card_not_found    sd_card_not_found_xcept);


	/**
	 * Returns the list of all user IDs (UTF8 string) present in terminal database having dynamic message
	 *
	 */
	set<string> dynamic_message_get_user_IDs()
	                        throws (
	                                /** Generic exception */
	                                1: Generic_types.Generic_error generic_xcept
	                                /** SD card not found */
                                    2:Generic_types.SD_card_not_found    sd_card_not_found_xcept);


    /**************************************************
     * Polling commands
     **************************************************/

	/**
	 * Get id from terminal polling buffer for external database verification.
	 *
	 * @return id for external database verification
	 */
	string external_db_get_id()
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


    /**
     * Verify external database user data.
     *
     * @return Verify_result_code
     */
	Generic_types.Verify_result_code external_db_verify_user(
                                                                /** User ID */
	                                                        1: string     user_id_UTF8,
                                                                /** User data */
	                                                        2: Db_types.User_DB_record user_data)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


	/**
	 * clears the id from terminal polling buffer
	 *
	 * @return none
	 */
	 void external_db_clear_id()
         throws (
                 /** Generic exception */
                 1: Generic_types.Generic_error generic_xcept
         );



    /**************************************************
     * Contactless commands
     **************************************************/

    /**
     * Get contactless card information<br>
     * Containing the Smartcard CSN as per the configuration, wheather Standard CSN or Reverse CSN
     */
    Cls_types.Cls_info cls_get_info(    /** Duration max. of the operation in seconds*/
                                        1: i32 timeout_in_sec)
                        throws (
                                /** Generic exception */
                                1: Generic_types.Generic_error generic_xcept
                                /** No suitable cards were detected during the defined duration*/
                                2: Generic_types.Timeout_error ex1);

    /**
     * Read files from a contactless card.
     *
     *
     * @return The list of read files/data
     */
    list<binary> cls_read(  /** Duration max. of the operation in seconds*/
                            1: i32                              timeout_in_sec,
                            /** List of card to support*/
                            2: Cls_types.Cls_cards_definition   cards)
            throws (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** Timeout has been reached*/
                        2: Generic_types.Timeout_error          ex1,
                        /** Invalid argument*/
                        3: Generic_types.Invalid_argument_error ex2,
                        /** One of the specified contactless key is invalid*/
                        4: Cls_types.Cls_invalid_key_error      ex3);

    /**
     * Write files on a contactless card.
     */
    void cls_write( /** Duration max. of the operation in seconds*/
                    1: i32                              timeout_in_sec,
                    /** List of card to support*/
                    2: Cls_types.Cls_cards_definition   cards)
            throws (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** Timeout has been reached*/
                        2: Generic_types.Timeout_error          ex1,
                        /** Invalid argument*/
                        3: Generic_types.Invalid_argument_error ex2,
                        /** One of the specified contactless key is invalid*/
                        4: Cls_types.Cls_invalid_key_error      ex3);


    /**
     * Encode an user contactless card
     *
     *
     * The card is encoded according to terminal configuration.
     * The card will contains fields required for access on Morpho terminals.
     * This command supports only pkcompv2 template data write on card.
     */
    void cls_write_user_card(   /** Duration max. of the operation in seconds*/
                                1: i32                      timeout_in_sec,
                                2: Cls_types.Cls_user_card  card_data)
            throws (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** Timeout has been reached*/
                        2: Generic_types.Timeout_error             ex1,
                        /** Invalid argument*/
                        3: Generic_types.Invalid_argument_error    ex2);

    /**
     * Encode an admin contactless card
     *
     *
     * The card is encoded according to terminal configuration.
     * The card will contain the new contactless keys to load on other Morpho terminals.
     */
    void cls_write_admin_card(  /** Duration max. of the operation in seconds*/
                                1: i32                      timeout_in_sec,
                                /** Admin card type to encode*/
                                2: Cls_types.Cls_card_type  card_type)
            throws (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** Timeout has been reached*/
                        2: Generic_types.Timeout_error             ex1,
                        /** Invalid argument*/
                        3: Generic_types.Invalid_argument_error    ex2,
                        /** The card detected by the terminal is not a card of input parameter card_type*/
                        4: Cls_types.Cls_invalid_card_type_error   ex3);

    /**
     * Erase a contactless card
     *
     *
     * For DESFire cards, according to the cards definition, this command will erase either one or several files,
     * either one or several applications or will format the card.<br>
     * In case of card formatting, the master PICC key will be set to 3DES legacy default value.
     *
     *
     * For MIFARE cards, this command will set every writable sectors to 0xFF.<br>
     * Sector keys will be set to NXP default keys (0x00).
     */
    void cls_erase( /** Duration max. of the operation in seconds*/
                    1: i32                              timeout_in_sec,
                    /** List of card to support*/
                    2: Cls_types.Cls_cards_definition   cards)
            throws (
                        /** Generic exception */
                        1: Generic_types.Generic_error generic_xcept
                        /** Timeout has been reached*/
                        2: Generic_types.Timeout_error          ex1,
                        /** Invalid argument*/
                        3: Generic_types.Invalid_argument_error ex2,
                        /** One of the specified contactless key is invalid*/
                        4: Cls_types.Cls_invalid_key_error      ex3);

    /**
     * Load contactless keys<br/><br/>
     *
     * - For MIFARE cards, this command will load CRYPTO1 (MIFARE Classic) and/or AES (MIFARE Plus) keys.<br/>
     * - For DESFire cards, this command will load 3DES and/or AES keys.<br/>
     * - For iClass cards, this command will load the iClass key.<br/>
     * - For RSA, this command will load the RSA key(s).<br/>
     * - For l1 cards, this command will load the L1 site key.<br/>
     */
    void key_load( /** Crypto key object*/
                        1: Cls_types.Crypto_keys  crypto_keys)
            throws (
                 /** Generic exception */
                 1: Generic_types.Generic_error generic_xcept
                 /** One of the specified contactless key is invalid*/
                 2: Cls_types.Cls_invalid_key_error      ex1);

    /**
     * Restore default contactless keys<br/><br/>
     *
     * - For MIFARE cards, this command will restore all MIFARE Classic and/or MIFARE Plus keys to default value.<br/>
     *
     * - For DESFire cards, this command will restore all DESFire 3DES and/or DESFire AES keys to default value.<br/>
     *
     * - For iClass cards, this command will restore the default iClass key.
     */
    void key_reset(    /** List of keys to reset to default value*/
                            1: list<Cls_types.Cls_card_type>  types)
            throws (
                    /** Generic exception */
                    1: Generic_types.Generic_error generic_xcept
                    /** Invalid argument*/
                    2: Generic_types.Invalid_argument_error ex1);

    /**************************************************
     * Other commands
     **************************************************/

    /**
     * When the command returns, terminal is going to reboot
     */
    void terminal_reboot()
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


    /**
     * Send back a received buffer
     *
     * Buffer shall be less than 64 bytes
     *
     * @return The received buffer
     */
    binary terminal_echo(   /** Buffer to be repeated */
                            1: binary buffer)
                  throws(
                          /** Generic exception */
                          1: Generic_types.Generic_error generic_xcept
                          /** The input parameter's size is over size limit (64 bytes) */
                          2: Generic_types.Out_of_memory_error      out_of_memory_xcept);


    /**
     * That functions is used to retrieve information like:
     * <ol>
     * <li> Terminal's local date and time </li>
     * <li> Terminal's IP configuration </li>
     * <li> Terminal's WIFI configuration </li>
     * <li> Terminal's GPRS configuration </li>
     * <li> Terminal's serial channel configuration </li>
     * </ol>
     */
    Generic_types.Terminal_configuration terminal_get_configuration(    /** Terminal setting options */
                                                                        1: Generic_types.Terminal_configuration_type terminal_settings_type
                                                                    )
                            throws (
                                    /** Generic exception */
                                    1: Generic_types.Generic_error generic_xcept
                                    /** Failed to get Ethernet configuration */
                                    2: Generic_types.Ethernet_config_not_found  ethernet_config_xcept
                                    /** WIFI module not connected */
                                    3: Generic_types.WIFI_module_not_connected WIFI_mod_xcept,
                                    /** License not found exception */
                                    4: Generic_types.License_not_found license_not_xcept
                                    );
    /**
     * That functions is used to configure:
     * <ol>
     *   <li> Terminal's local date and time (i.e. not Network Time Protocol) </li>
     *   <li> Terminal's IP configuration </li>
     *   <li> Terminal's WIFI configuration </li>
     *   <li> Terminal's serial channel configuration </li>
     * </ol>
     * <b>Note:</b>
     * <ul>
     *   <li>While setting the serial channel configuration, a delay of 3 seconds is provided after sending the response
     *       to the client, so that the configuration is applied only after the response is sent to the client.
     * </ul>
     */
    void terminal_set_configuration(    /**
                                         * Structure that contains configuration to apply. <br>
                                         * It can contain several configurations.
                                         */
                                        1: Generic_types.Terminal_configuration terminal_config)
                            throws (
                                        /** Generic exception */
                                        1: Generic_types.Generic_error generic_xcept
                                        /** Invalid parameter set */
                                        2: Generic_types.Invalid_argument_error invalid_arg_xcept,
                                        /** Failed to configure Ethernet settings */
                                        3: Generic_types.Ethernet_configuration_failed ethernet_config_xcept,
                                        /** WIFI module not connected */
                                        4: Generic_types.WIFI_module_not_connected WIFI_mod_xcept,
                                        /** License not found exception */
                                        5: Generic_types.License_not_found license_not_xcept
                                    );

    /**
     * Get the list of terminal's predefined time zones
     *
     *
     * The terminal contains a list of predefined time zones that can be used
     * to configure terminal's date and time (see @a terminal_set_configuration).
     *
     * @return  A list of UTF-8 strings that represents predefined time zones handled
     *          by the terminal
     */
    set<string> time_get_predefined_time_zone_list()
                                       throws (
                                               /** Generic exception */
                                               1: Generic_types.Generic_error generic_xcept
                                       );


    /**
     * Open or close a distant session
     *
     *
     * When a distant session is opened, the terminal only waits for distant commands.
     * No local operation can be done.
     */
    void distant_session_set_state( /** Open or Close the distant session */
                                    1: Generic_types.Distant_session_state state)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


    /**
     * Get the terminal's distant session state
     *
     *
     * When a distant session is opened, the terminal only waits for distant commands.
     * No local operation can be done.
     *
     * @return The distant session's status (opened or closed)
     */
    Generic_types.Distant_session_state distant_session_get_state()
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


    /**
     * Cancel current delayed command
     */
    void cancel_operation()
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


    /**
     * Get firmware versions
     *
     *
     * Return firmware version of requested board type (Terminal or Sensor)
     *
     * @return Firmware version
     */
    string terminal_get_version(    /** Board to retrieve firmware version from */
                                    1: Generic_types.Generic_firmware_type firmware_type)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );



    /**
     * Retrieve the list of terminal internal peripherals.
     */
    list<Generic_types.Terminal_peripherals> terminal_retrieve_peripherals()
                                       throws (
                                               /** Generic exception */
                                               1: Generic_types.Generic_error generic_xcept
                                       );


    /**
     * Get product information from terminal board and sensor board.
     *
     * @return Requested information
     */
    Generic_types.Product_info product_get_info(   /** List of requested information */
                                                   1: set<Generic_types.Product_info_type> info_type)
        throws  (
                    /** Generic exception */
                    1: Generic_types.Generic_error generic_xcept
                    /** Invalid parameter*/
                    2: Generic_types.Invalid_argument_error invalid_argument_xcept);

    /**
     * Gets the specified capabilities of the terminal.
     */
    map< Generic_types.Capability, list< Generic_types.Variant > > get_terminal_capabilities (
            /** List of the capabilities required */
            1: set < Generic_types.Capability > capability_list)
            throws (
                    /** Generic exception */
                    1: Generic_types.Generic_error generic_xcept
        );
    /**************************************************
     * Communication commands
     **************************************************/

    /**
     * send wiegand or clock&data string
     */
    void    wiegand_clock_data_send_string( /** binary wiegand or clock & data data to send */
                                            1: binary  data_to_send)

        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                2: Generic_types.Invalid_wiegand_string  invalid_wiegand_string_exception,
				3: Generic_types.Wiegand_output_disabled wiegand_out_disable_exception
        );
    /**************************************************
     * Multimedia commands
     **************************************************/

    /**
     * Capture a picture in specified format
     *
     *
     * The terminal will capture a picture from camera or will perform a screenshot,
     * and will return the picture in specified format.
     *
     * @return The raw data of the captured picture
     */
    binary picture_capture( /** Interface that will capture the picture (Cameras or screen) */
                            1: Generic_types.Picture_interface input_interface,
                            /** Format of the picture to retrieve (JPEG, BMP ...) */
                            2: Generic_types.Picture_format format)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );

    /**
     * Display a picture in specified format
     *
     *
     * The terminal will display a picture on the screen.<br>
     * The picture will start at the specified coordinates and will be displayed
     * during the specified duration
     */
    void picture_display(   /** Format of the picture to display (JPEG, BMP ...) */
                            1: Generic_types.Picture_format format
                            /** Raw data of the picture file */
                            2: binary picture_data,
                            /** Screen coordinates of the right-upper corner of the picture */
                            3: Generic_types.XY_coordinates coordinates,
                            /** Duration in seconds during which the picture is displayed */
                            4: i32 duration_in_sec)
    throws(
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid argument */
                2: Generic_types.Invalid_argument_error invalid_argument_xcept);


    /**
     * Display a text message
     *
     *
     * The terminal will display a text message on the screen.<br>
     * The text message will start at the specified coordinates and will be displayed
     * during the specified duration.<br>
     * Min-Max range for duration is (0-255 seconds) where 0 = infinite time.<br>
     * Min-Max range for X- co-ordinate is (0-720).<br>
     * Min-Max range for Y- co-ordinate is (0-450)
     */
    void display_text(   /** String message text to be display on terminal screen*/
                            1: string message_text,
                            /** Screen coordinates of the right-upper corner of the message text */
                            2: Generic_types.XY_coordinates coordinates,
                            /** Duration in seconds during which the text message is displayed */
                            3: i32 duration_in_sec)
        throws (
                    /** Generic exception */
                    1: Generic_types.Generic_error generic_xcept
                    /** Invalid parameter*/
                    2: Generic_types.Invalid_argument_error     invalid_argument_xcept);

    /**
     * Load a file into the terminal.<br>
     * <b>Note:</b>
     * <ol>
     *   <li>The <code>File_types.File_chunk.action</code> shall be taken into consideration only for the last chunk,
     *     i.e., when <code>File_types.File_chunk.is_last</code> is true.
     *   <li>Maxixum file sizes:
     *     <ul>
     *       <li><code>File_types.File_type.video</code>:    10 MB
     *       <li><code>File_types.File_type.audio</code>:   500 KB
     *       <li><code>File_types.File_type.picture</code>:   1 MB
     *       <li>Others:                                      5 MB
     *     </ul>
     *   <li>Maximum chunk size is 10240 bytes, i.e. 10 KB
     *   <li>Make sure video file is in proper format. (MPEG4 or VP8)
     *   <li>While updating stolen card entries, all previous entries will be deleted
     * </ol><br>
     * <b>Warning:</b><br>
     * <ol>
     *   <li>You shall need a modified version of the generated code that supports
     *       handling of several request/response messages for the single call to the command.
     *   <li>For file type <code>File_types.File_type.stolen_card_list</code>, No error will be return.
     *       And maximum 250000 valid stolen card entried will be stored and rest of the entries will be ignored.
     * </ol><br>
     * <b>Functionality change required in Thrift generated client code (C++ sample)</b><br>
     * <pre>
     * void Generic_commandsClient::file_load(const  ::Distant_cmd::File_details& file_details, const  ::Distant_cmd::File_chunk& chunk)
     * {
     *     <span style="color:green">// Original code section in the generated code
     *     // send_file_load(file_details, chunk);
     *     // recv_file_load();</span>
     * &nbsp;
     *     <span style="color:green">// BEGIN: Custom section for receiving and processing intermediate data
     *     // This is actually multi-request handling</span>
     *     ::Distant_cmd::File_chunk actual_chunk; <span style="color:green">// a non-const chunk required</span>
     *     while(true)
     *     {
     *         <span style="color:green">// Client's call-back is supposed to load the data that shall be available in the 'actual_chunk' parameter to send to the Thrift server.
     *         //  Note that in case of the last chunk of data to be uploaded the 'actual_chunk.is_last' flag must be set.</span>
     *         Multiresponse_handler::client_cb_file_load(actual_chunk);
     *         send_file_load(file_details, actual_chunk);
     * &nbsp;
     *         recv_file_load(); <span style="color:green">// required to see if exception was received -- so that further sending is stopped</span>
     * &nbsp;
     *         if(actual_chunk.is_last) <span style="color:green">// Exit the loop since the last chunk has been sent and its corresponding response received</span>
     *         {
     *             break;
     *         }
     *     }
     *     <span style="color:green">// END: Custom section for receiving and processing intermediate data</span>
     * }
     * </pre>
     */
    void file_load(
            /** In cases where file name is required, the file shall be uploaded with the same name as the file name provided */
            1: File_types.File_details  file_details,
            /** The chunk of the file */
            2: File_types.File_chunk    chunk)
        throws(
            /** Generic exception */
            1: Generic_types.Generic_error generic_xcept
            /** The specified file does not exist or insufficient data provided */
            2: Generic_types.File_inexistent_error file_inexistent_xcept,
            /** The speficied file or chunk exceeds its maximum limit */
            3: Generic_types.File_too_large_error file_large_xcept,
            /** The file-name is missing */
            4: Generic_types.File_name_missing_error file_name_missing_xcept,
            /** The particular type of file with the specified extension is not allowed */
            5: Generic_types.Invalid_file_extension_error invalid_file_ext_xcept,
            /** The SD card not found (might be required for specific files) */
            6: Generic_types.SD_card_not_found SD_card_not_found_xcept
            );

    /**
     * Retrieve a file from the terminal.<br>
     * <b>Functionality change required in Thrift generated client code (C++ sample)</b><br>
     * <pre>
     *  void Generic_commandsClient::file_get( ::Distant_cmd::File_chunk& _return, const  ::Distant_cmd::File_details& file_details)
     *  {
     *      send_file_get(file_details);
     *      <span style="color:green">// recv_file_get(_return); // Original line in the generated code</span>
     * &nbsp;
     *      <span style="color:green">// BEGIN: Custom section for receiving and processing intermediate data</span>
     *      while (true)
     *      {
     *          recv_file_get(_return); <span style="color:green">// Multiple reception in loop</span>
     * &nbsp;
     *          <span style="color:green">// Following is the client's callaback assumed to take necessary action on the received data,
     *          //  e.g., keep writing the received partial data to the file until the last chunk of data is received.</span>
     *          Multiresponse_handler::client_cb_file_get(_return);
     * &nbsp;
     *          if(_return.is_last) <span style="color:green">// Exit the loop if the data received was last of all the multiple data received, i.e., no more data to be received</span>
     *          {
     *              break;
     *          }
     *      }
     *      <span style="color:green">// END: Custom section for receiving and processing intermediate data</span>
     *  }
     * </pre>
     */
    File_types.File_chunk    file_get(
                                        /** File details of the file to obtain
                                         * (<code>File_types.File_details.name_UTF8</code> shall be ignored except where multiple files exist)
                                         */
                                        1: File_types.File_details      file_details)
        throws(
            /** Generic exception */
            1: Generic_types.Generic_error generic_xcept
            /** The specified file does not exist or insufficient data provided */
            2: Generic_types.File_inexistent_error file_inexistent_xcept
            /** The SD card not found (might be required for specific files) */
            3: Generic_types.SD_card_not_found SD_card_not_found_xcept
              );

    /**
     * Retrieve all the files name for a given file type
     *
     * <h5>Returns</h5> List of structure for files' details
     */
    list<File_types.File_details>    file_get_filenames( 1: File_types.File_type file_type)
        throws(
            /** Generic exception */
            1: Generic_types.Generic_error generic_xcept
            /** Invalid file type specified */
            2: Generic_types.File_inexistent_error file_inexistent_xcept);

    /**
     * Erase a file represented by name and type
     */
    void file_erase( 1: File_types.File_details file_details)
        throws(
            /** Generic exception */
            1: Generic_types.Generic_error generic_xcept
            /** The specified file does not exist or insufficient data provided */
            2: Generic_types.File_inexistent_error file_inexistent_xcept
            /** The SD card not found (might be required for specific files) */
            3: Generic_types.SD_card_not_found SD_card_not_found_xcept
            );


    /**************************************************
     * SDAC commands
     **************************************************/

    /**
     * Returns a structure containing 4 integers. The values in list are as follows :
     * <ul>
     * <li> SDAC mode : 0=Off, 1=On </li>
     * <li> Relay state : 0=Door locked, 1=Door unlocked </li>
     * <li> Door status : 0=Closed, 1=Open, -1=Error </li>
     * <li> Request to exit state : 0=Off, 1=On, -1=Error </li>
     * </ul>
     */
    Generic_types.Sdac_status get_sdac_status()
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
        );


    /**
     * Trigger the relay for a given duration. A duration less or equal to 0 is forbidden.
     */
    void trigger_relay( /** duration in second for relay activation */
                        1: i32  duration_in_sec)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid parameter*/
                2: Generic_types.Invalid_argument_error     invalid_argument_xcept);

    /**************************************************
     * Stringlist commands
     **************************************************/

    /**
     * Returns a list of string of authorized IPs
     */
    list<string> authorized_IP_get_list(  /** IP protocol type i.e. v4, v6 or all */
                                        1: Generic_types.IP_protocol_type ip_protocol_type)
                                        throws (
                                                /** Generic exception */
                                                1: Generic_types.Generic_error generic_xcept
                                        );


    /**
     * Adds an authorized IP
     */
    void authorized_IP_add(   /** UTF8 string containing authorized IP */
                            1: string str_ip)
        throws(
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** The database memory of authorized IP range list is full */
                2: Db_types.DB_full_error DB_full_xcept,
                /** Invalid parameter*/
                3: Generic_types.Invalid_argument_error     invalid_argument_xcept);

    /**
     * Remove an authorized IP
     */
    void authorized_IP_delete(    /** UTF8 string containing authorized IP to be deleted */

                                1: string str_ip)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid parameter*/
                2: Generic_types.Invalid_argument_error     invalid_argument_xcept);

    /**
     * Returns a list of string of authorized IP ranges
     */
    list<string> authorized_IP_get_range_list(    /** IP protocol type i.e. v4, v6 or all */
                                                1: Generic_types.IP_protocol_type ip_protocol_type)
                                                throws (
                                                        /** Generic exception */
                                                        1: Generic_types.Generic_error generic_xcept
                                                );


    /**
     * Adds an authorized IP range
     */
    void authorized_IP_add_range( /** UTF8 string containing authorized IP range start address */
                                1: string str_start_ip,
                                /** UTF8 string containing authorized IP range end address */
                                2: string str_end_ip)
        throws(
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** The database memory of IP authorized range list is full */
                2: Db_types.DB_full_error DB_full_xcept,
                /** Invalid parameter*/
                3: Generic_types.Invalid_argument_error invalid_argument_xcept);

    /**
     * Remove an authorized IP range
     */
    void authorized_IP_delete_range(  /** UTF8 string containing an authorized IP range start address to be deleted */
                                    1: string str_start_ip,
                                    /** UTF8 string containing an authorized IP range end address to be deleted */
                                    2: string str_end_ip)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid parameter*/
                2: Generic_types.Invalid_argument_error invalid_argument_xcept);

    /**
     * To set a password
     *
     * @return True, if set successfully.
     *
     */
     bool password_set( /**
                         * password ID<br>
                         * Must be 0 (terminal password)
                         */
                        1: Security_types.Sec_obj_ID id,
                        /** old password */
                        2: string password_old,
                        /** new password */
                        3: string password_new)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** A default password detected */
                2: Generic_types.Security_default_password default_password_xcept,
                /** Invalid parameter*/
                3: Generic_types.Invalid_argument_error invalid_argument_xcept);

    /**
     * To verify a given password with stored password
     *
     * @return True, if verify successfully.
     *
     */
     bool password_verify(  /**
                            * password ID<br>
                            * Must be 0 (terminal password)
                            */
                            1: Security_types.Sec_obj_ID id,
                            /** password to be verified with stored password*/
                            2: string password)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid parameter*/
                2: Generic_types.Invalid_argument_error invalid_argument_xcept,
                /** A default password detected */
                3: Generic_types.Security_default_password default_password_xcept);

    /**
     * To reset a password
     *
     * @return True, if reset successfully.
     *
     */
     bool password_reset(   /**
                            * password ID<br>
                            * Must be 0 (terminal password)
                            */
                            1: Security_types.Sec_obj_ID id)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid parameter*/
                2: Generic_types.Invalid_argument_error invalid_argument_xcept);

    /**
     * To set a passphrase
     *
     * @return True, if set successfully.
     *
     */
     bool passphrase_set(   /**
                             * passphrase ID
                             */
                        1: Security_types.Passphrase_id id,
                        /** passphrase */
                        2: string passphrase)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid parameter*/
                2: Generic_types.Invalid_argument_error invalid_argument_xcept
        );

    /**
     * To reset a passphrase
     *
     * @return True, if reset successfully.
     *
     */
     bool passphrase_reset( /**
                             * passphrase ID
                             */
                            1: Security_types.Passphrase_id id)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid parameter*/
                2: Generic_types.Invalid_argument_error invalid_argument_xcept);

    /**
     * To get user input from LCD GUI
     *
     * @return entered input from terminal
     */
     string retrieve_keypad_input( /** timeout in second for getting input */
                                        1: i32  timeout_in_sec)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Command is cancelled by user*/
                2: Generic_types.Cancelled_error cancelled_xcept,
                /** User input form timed out*/
                3: Generic_types.Timeout_error timeout_xcept)

    /**************************************************
     * Access schedule commands
     **************************************************/

    /**
     * Command to get the access schedule entries.
     *
     * @return list of access_schedule data according to schedule_index.
     *         List of Access_schedule provides data from sunday to saturday.
     *
     */
     list<Db_types.Access_schedule>  access_schedule_retrieve
    (
        /** access schedule index. Value should be between 1 to 58.
        *   Schedule 0 is never allowed schedule.
        *   Schedule 63 is always allowed schedule.
        *   Schedule 59 to 62 are reserved schedule.
        */
        1:list<byte>        schedule_index
    )
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid schedule index exception */
                2: Db_types.Invalid_schedule_index invalid_schedule_index_ex,
                /** Access schedule parameter not present in database */
                3: Config_types.Config_inexistent_parameter_error inexistant_param_xcept
        );

    /**
     * Command to set the access schedule entries.
     */
    void access_schedule_store
    (
        /** access schedule data. List of Access_schedule takes data from sunday to saturday */
        1:list<Db_types.Access_schedule>        schedule_data
    )
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid schedule index exception */
                2: Db_types.Invalid_schedule_index invalid_schedule_index_ex,
                /** Access schedule parameter not present in database */
                3: Config_types.Config_inexistent_parameter_error inexistant_param_xcept
                /** Access schedule data invalid */
                4: Config_types.Config_invalid_value_error invalid_value_xcept
        );

    /**
     * Command to reset the access schedule entries.
     */
    void access_schedule_delete
    (
        /** access schedule index. Value should be between 1 to 58.
        *   Schedule 0 is never allowed schedule.
        *   Schedule 63 is always allowed schedule.
        *   Schedule 59 to 62 are reserved schedule.
        */
        1:list<byte>        schedule_index
    )
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid schedule index exception */
                2: Db_types.Invalid_schedule_index invalid_schedule_index_ex,
                /** Access schedule parameter not present in database */
                3: Config_types.Config_inexistent_parameter_error inexistant_param_xcept
                /** Access schedule data invalid */
                4: Config_types.Config_invalid_value_error invalid_value_xcept
        );

    /**************************************************
     * Door open schedule commands
     **************************************************/

    /**
     * Command to get the door open schedule entries.
     *
     * @return list of Door_open_schedule data
     *         List of Door_open_schedule provides data from sunday to saturday.
     *
     */
     list<Db_types.Door_open_schedule>  door_open_schedule_retrieve()
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Door open schedule parameter not present in database */
                2: Config_types.Config_inexistent_parameter_error inexistant_param_xcept
        );

    /**
     * Command to set the door open schedule entries.
     */
    void door_open_schedule_store
    (
        /** door open schedule data. List of Door_open_schedule takes data from sunday to saturday. */
        1:list<Db_types.Door_open_schedule>        schedule_data
    )
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Door open schedule parameter not present in database */
                2: Config_types.Config_inexistent_parameter_error inexistant_param_xcept
                /** Door open schedule data invalid */
                3: Config_types.Config_invalid_value_error invalid_value_xcept
        );

    /**
     * Command to reset the door open schedule entries.
     */
    void door_open_schedule_delete()
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Door open schedule parameter not present in database */
                2: Config_types.Config_inexistent_parameter_error inexistant_param_xcept
                /** Door open schedule data invalid */
                3: Config_types.Config_invalid_value_error invalid_value_xcept
        );

    /**************************************************
     * Holiday schedule commands
     **************************************************/

    /**
     * Command to get the Holiday schedule entries.
     *
     * @return list of Holi_schedule data according to schedule_index
    *
     */
     list<Db_types.Holiday_schedule>  holiday_schedule_retrieve
    (
        /** holiday schedule index .  Value should be between 0 to 63*/
        1:list<byte>        schedule_index
    )
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid schedule index exception */
                2: Db_types.Invalid_schedule_index invalid_schedule_index_ex,
                /** Access schedule parameter not present in database */
                3: Config_types.Config_inexistent_parameter_error inexistant_param_xcept
        );

    /**
     * Command to set the holiday schedule entries.
     */
    void holiday_schedule_store
    (
        /** holiday schedule data */
        1:list<Db_types.Holiday_schedule>        schedule_data
    )
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid schedule index exception */
                2: Db_types.Invalid_schedule_index invalid_schedule_index_ex,
                /** Access schedule parameter not present in database */
                3: Config_types.Config_inexistent_parameter_error inexistant_param_xcept
                /** Access schedule data invalid */
                4: Config_types.Config_invalid_value_error invalid_value_xcept
        );

    /**
     * Command to reset the holiday schedule entries.
     */
    void holiday_schedule_delete
    (
        /** holiday schedule index . Value should be between 0 to 63 */
        1:list<byte>        schedule_index
    )
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid schedule index exception */
                2: Db_types.Invalid_schedule_index invalid_schedule_index_ex,
                /** Access schedule parameter not present in database */
                3: Config_types.Config_inexistent_parameter_error inexistant_param_xcept
                /** Access schedule data invalid */
                4: Config_types.Config_invalid_value_error invalid_value_xcept
        );

   /**
    * Command to scan WIFI networks
    * @return list of WIFI_network_info which contains network informations
    */
    list<Generic_types.WIFI_network_info> scan_WIFI_networks
    (
    )
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** WIFI module not connected */
                2: Generic_types.WIFI_module_not_connected WIFI_module_connect_xcept,
                /** License not found exception */
                3: Generic_types.License_not_found license_not_xcept
        );

    // /**
    // * Command to configure WIFI network
    // */
    // void configure_WIFI_network
    // (
        // /** configuration network information structure */
        // 1:Generic_types.WIFI_configuration_info        config_network_info
    // )
    // throws (
                // /** Generic exception */
                // 1: Generic_types.Generic_error generic_xcept
                // /** WIFI invalid parameter configuration error */
                // 2: Config_types.Config_invalid_value_error  invalid_value_xcept
                // /** WIFI module not connected */
                // 3: Generic_types.WIFI_module_not_connected  WIFI_module_connect_xcept
           // );

    // /**
    // * Command to get WIFI network status
    // * @return  WIFI_network_status which contains current network status informations
    // */
    // Generic_types.WIFI_network_status get_WIFI_network_status
    // (
    // )
    // throws (
                // /** Generic exception */
                // 1: Generic_types.Generic_error generic_xcept
                // /** WIFI module not connected */
                // 2: Generic_types.WIFI_module_not_connected  WIFI_module_connect_xcept
           // );

    /**
     Set one or more event configurations.<br />
     Following table shows which configurations are allowed for given event.<br /><br />
<div style="margin:0 0 0 30px">
<table border="5" cellpadding="0" cellspacing="0" width="800"><colgroup><col width="185"/><col width="64" span="6"/></colgroup><tbody><tr height="20"><td height="20" width="185"><strong>Event Name</strong></td><td width="64"><strong>Enable</strong></td><td width="64"><strong>Send To Cotroller</strong></td><td width="64"><strong>Trigger TTL0</strong></td><td width="64"><strong>Trigger TTL1</strong></td><td width="64"><strong>Trigger TTL2</strong></td><td width="64"><strong>Clock n Data ID</strong></td></tr>
<tr height="20"><td height="20"><strong>tlac_duress_finger_detected</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td></tr><tr height="20"><td height="20"><strong>tlac_fake_finger_detected</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td></tr><tr height="40"><td height="40" width="185"><strong>tlac_user_control_successful</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes
</td><td> Yes </td><td></td></tr><tr height="20"><td height="20" width="185"><strong>tlac_biometric_mismatch</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td></tr><tr height="20"><td height="20" width="185"><strong>tlac_pin_mismatch</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td></tr><tr height="20"><td height="20" width="185"><strong>tlac_user_id_not_in_db</strong></td><td> Yes </td><td> Yes </td><td> Yes </td>
<td> Yes </td><td> Yes </td><td> Yes </td></tr><tr height="20"><td height="20" width="185"><strong>tlac_control_timed_out</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td></tr><tr height="20"><td height="20" width="185"><strong>tlac_rejected_by_schedule</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td> Yes </td></tr><tr height="20"><td height="20" width="185"><strong>tlac_temp_validity_expired</strong></td><td> Yes
</td><td> Yes </td><td></td><td></td><td></td><td> Yes </td></tr><tr height="20"><td height="20" width="185"><strong>tlac_useruser_not_in_white_list</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td></tr><tr height="20"><td height="20"><strong>tlac_black_listed_card</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td></tr><tr height="20"><td height="20"><strong>tlac_face_not_detected</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td> Yes </td></tr><tr height="20"><td height="20"><strong>tlac_multi_user_intermediate_id</strong></td><td> Yes
</td><td></td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_transaction_log_full</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_controller_feedback_action</strong></td><td> Yes </td><td></td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_job_code_check_failure</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td> Yes </td></tr><tr height="20"><td height="20"><strong>tlac_door_opened_for_too_long</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr>
<tr height="20"><td height="20"><strong>tlac_door_forced_open</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_door_closed_after_alarm</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_door_unlocked</strong></td><td> Yes </td><td> Yes
</td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_door_locked_back</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_management_menu_login</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td></td></tr><tr height="20"><td height="20"><strong>tlac_management_menu_logout</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr>
<tr height="20"><td height="20"><strong>tlac_database_deleted</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_enrollment_completed</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_user_deleted</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_user_modification_completed</strong></td><td> Yes </td><td> Yes
</td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_cls_card_encoded</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_cls_card_reset</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_settings_changed</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_cls_card_security_key_reset</strong></td>
<td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_security_policy_changed</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_tamper_detected</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td></tr><tr height="20"><td height="20"><strong>tlac_tamper_cleared</strong></td><td> Yes
</td><td></td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_terminal_boot_completed</strong></td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td> Yes </td><td></td></tr><tr height="20"><td height="20"><strong>tlac_firmware_upgrade</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_add_user</strong></td><td> Yes </td><td> Yes </td><td></td>
<td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_reboot_initiated</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td></td></tr><tr height="20"><td height="20"><strong>tlac_user_rule_check_failure</strong></td><td> Yes </td><td> Yes </td><td></td><td></td><td></td><td> Yes </td></tr></tbody></table></div>
     */
    void events_set_config( /** Mapping of Event IDs to their config structure fields*/
                                 1: map<Db_types.Transaction_log_action_code, Generic_types.Event_config> events)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                2: Generic_types.Invalid_argument_error invalid_argument_xcept);

    /**
     * Returns one or more event configuration.
     *
     *
     * @return A map of Event IDs and their corresponding records.<br>
     */
    map<Db_types.Transaction_log_action_code, Generic_types.Event_config> events_get_config( /** List of Event IDs to return*/
                                1: set<Db_types.Transaction_log_action_code>                      event_IDs)
                                throws (
                                        /** Generic exception */
                                        1: Generic_types.Generic_error generic_xcept
                                        2: Generic_types.Invalid_argument_error invalid_argument_xcept);

/**
     * Add license(s) to terminal
     */
    void licenses_add(  /** License file content */
                        1: binary license)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid parameter */
                2:Generic_types.Invalid_argument_error invalid_argument_xcept,
                /** SD card not found */
                3:Generic_types.SD_card_not_found sd_card_not_found_xcept);

    /**
     * Retrieve the list of the licenses stored in the terminal
     * @return A list of the licenses contained in the terminal (empty list if the terminal doesn't contain license)
     */
    list<string> licenses_get()
       throws (
               /** Generic exception */
               1: Generic_types.Generic_error generic_xcept
       );


    /**
     * Gets the list of video phone profiles.
     */
    list<Generic_types.Video_phone_params> config_get_video_phone_params()
       throws (
               /** Generic exception */
               1: Generic_types.Generic_error generic_xcept
       );


    /**
     * Sets the list of video phone profiles<BR>
     * <B>Note:</B>
     * <ol>
     *  <li>A maximum of 20 profiles shall be stored.
     *  <li>If the number of profiles stored is less than 20, say 15, a fresh copy of the profiles,
     *          the 15 which are provided, and the remaining 5 blank profiles shall be stored.<br>
     *          For any GUI application, the blank profiles are like empty slots, which may not be required to be displayed.
     *  <li>To erase all profiles, the parameter <code>params_video_phone</code> with <i>zero</i> size must be passed.
     *  <li>To edit one or more profiles, and set them, the remaining profiles shall be preserved only if the latter profiles
     *          are again provided to set as is.<br>
     *          For instance, if you want to edit profiles #2 and #3, get all the profiles
     *          (via <code>config_get_video_phone_params</code>), edit the profiles of interest (profile #2 and #3),
     *          and using this API, set all the 20 profiles back. This way, the profiles other than profiles #2 and #3
     *          are preserved and not deleted. In case you pass <i>only</i> profiles #2 and #3 to this API, the rest of the profiles
     *          shall be stored as blank profiles, i.e., effectively deleting them.
     *  <li>Any profile entry with all of its parameters empty, i.e., empty strings and <code>0</code> for
     *          <code>Video_phone_params.port</code>, shall be considered as a blank profile (empty slot).
     *  <li>Any profile entry with not all of its parameters empty shall throw appropriate exception.
     * </ol>
     */
    void config_set_video_phone_params
    (
        /**
         * The list of video phone parameters. The list size to be maximum 20.
         */
        1: list<Generic_types.Video_phone_params> params_video_phone
    )
    throws (
            /** Generic exception */
            1: Generic_types.Generic_error generic_xcept
            /**
             * Invalid IP string provided in <code>Video_phone_params.address_IP</code>.
             */
            2: Generic_types.Invalid_IP_error xcept_invalid_IP,
            /**
             * The number of profiles provided exceeded the maximum limit of 20.
             */
            3: Generic_types.Invalid_size_error xcept_invalid_size,
            /**
             * For any profile, incomplete information provided, i.e., both of the following conditions fail:
             * <ul>
             *   <li> All the parameters of the profile provided.
             *   <li> None of the parameters of the profile provided (blank profile).
             * </ul>
             */
            4: Config_types.Config_invalid_value_error xcept_invalid_value
    )

	/**
     * That functions is used to send data on host:
     * <ol>
     * <li> Send data to host on IP network </li>
     * <li> Send data to host on serial channel </li>
     * </ol>
     */
    void send_to_host(/**
                       * Structure that contains configuration of host channel. <br>
                       * It can contain several configurations.
                       */
                      1: Generic_types.Host_configuration host_config,
				      /** data to send on host channel */
				      2: binary data)
        throws (
                /** Generic exception */
                1: Generic_types.Generic_error generic_xcept
                /** Invalid parameter*/
                2: Generic_types.Invalid_argument_error invalid_argument_xcept,
                /** controller not found */
                3: Generic_types.Host_not_found host_not_found_xcept);

    /**
     * Retrieve the list of language files stored in /rootfs_data/Translation
     * @return A list of string of the language files
     */
    list<string> retrieve_language_file_list()
       throws (
               /** Generic exception */
               1: Generic_types.Generic_error generic_xcept
       );

}
