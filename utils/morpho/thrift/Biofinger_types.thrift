/**
 * @section LICENSE
 * Copyright &copy; 2012 Safran Morpho - Safran Morpho confidential - all rights reserved
 *
 * @section DESCRIPTION
 *
 *
 * @file Biofinger_types.thrift
 *
 * CHANGELOG
 * 23 nov 2012  - Initiate header
 * 03 dec 2012  - In Biofinger_compression_type, add _algo (because null is interpreted by SWIG)
 *              - Change "set" to "list" in structure because std::set is a mess in SWIG
 * 06 dec 2012  - Change standard member in Biofinger_sensor_matching_strategy and Biofinger_sensor_coder
 *                so that files generated with pure_enums option can compile
 * 10 dec 2012  - Change namespace to comply MPH coding rules.
 * 13 dec 2012  - Erase useless Biofinger_mode
 *              - Add comments
 *              - Add Biofinger_enroll_operation_reply for reply of Biofinger_enroll command
 *              - Change Biofinger_control_operation_reply, no need for enrollment steps
 *              - Change members' names of Biofinger_sensor_image to indicate the type
 *              - Correct name of Biofinger_control_optional_param required_matching_score
 * 18 dec 2012  - Change returned image of enroll command into best_image
 * 08 jan 2013  - Modify enroll distant command to be able to export FP templates and FV at same time.
 *              - Rename some variables for better understanding
 * 09 jan 2013  - Change images requirement in enroll command
 *              - Enroll now returns a security compatibility per template
 * 15 may 2013  - Changed 'enrol' word(UK english) to 'enroll' (US english change)
 *              - Response of enrollment command changed to include template type field as well
 * 10 july 2013 - Removed 'cfv' as template type from Biofinger_template_type enum.
 */

include "Generic_types.thrift"

// Access Control (authenticate, identify ,enrollment) types

namespace cpp Distant_cmd

/** Enumeration representing of the biometric operation failure.*/
enum Biofinger_failure_cause
{
    Biofinger_matching_no_hit,
    Biofinger_matching_FFD,
    Biofinger_matching_moist_finger,
    Biofinger_enrollment_bad_quality
}

struct Biofinger_control_final_result
{
    /**
     * Indicate matching result.</br>
     * True for hit, false for error or no hit.
     */
    1: required bool success,
    /**
     * Indicate the cause of the error.</br>
     * Present if success field is false.
     */
    2: optional Biofinger_failure_cause cause,
    /**
     * If success field if true, score of the matching operation. </br>
     * It shall have been requested in the request.
     */
    3: optional byte matching_score,
    /** If success field is true, number of the finger that matched with captured one (see Biofinger_control_optional_param::require_matching_score).*/
    4: optional byte matching_template_number,
    /**
     * User ID.</br>
     * It is filled once the user ID is known, whatever the final result is.
     */
    5: optional string user_ID_UTF8
}

/** Enumeration representing the finger position/command event sent by the sensor.*/
enum Biofinger_command
{
    biofinger_move_no_finger = 0,
    biofinger_move_finger_up = 1,
    biofinger_move_finger_down = 2,
    biofinger_move_finger_left = 3,
    biofinger_move_finger_right = 4,
    biofinger_press_finger_harder = 5,
    biofinger_latent = 6,
    biofinger_remove_finger = 7,
    biofinger_finger_ok = 8,
    biofinger_finger_detected = 9,
    biofinger_finger_misplaced = 10,
    biofinger_live_ok = 11
}

struct Biofinger_callback_command
{
    /**
    * Finger placement modification required, or finger data acquisition completed.</br>
    * Sent as intermediate reply of biometric command.
    */
    1: required Biofinger_command command;
}

/** Enumeration representing compression used in an exported image.*/
enum Biofinger_compression_type
{
    null_algo,
    v1_algo,
    wsq_algo,
}

struct Biofinger_sensor_image
{
    /** Width of the image in pixels.*/
    1: required i32 width_in_pix,
    /** Height of the image in pixels.*/
    2: required i32 height_in_pix,
    /** Horizontal resolution of the image in dot per inch.*/
    3: required i32 horizontal_resol_dpi,
    /** Vertical resolution of the image in dot per inch.*/
    4: required i32 vertical_resol_dpi,
    /** Compression algorithm used on the image.*/
    5: required Biofinger_compression_type  compression_type,
    /** Image's binary data.*/
    6: required binary image_data,
    /**
     * Number of bits per pixel for the image.</br>
     * Present in intermediate replies' images of biometric commands.
     */
    7: optional byte bits_per_pixel,
}

/** Enumeration representing the format handled by the sensor in biometric operations.*/
enum Biofinger_template_type
{
    /** Morpho legacy native fingerprint template format.*/
    pkcompv2,
    /** Morpho private fingerprint template format dedicated to AFIS.*/
    pkmat,
    /** ANSI INCITS 378-2004 public finger minutiae record format.*/
    ansi378_2004,
    /**
     * Finger Minutiae Card Record, Compact Size.</br>
     * Public fingerprint template format, dedicated to smart card, defined by the ISO organization.
     */
    iso19794_2_fmc_cs,
    /**
     * Finger Minutiae Card Record, Normal Size.</br>
     * Public fingerprint template format, dedicated to smart card, defined by the ISO organization.
     */
    iso19794_2_fmc_ns,
    /**
     * Finger Minutiae Record.</br>
     * Public fingerprint template format, defined by the ISO organization.
     */
    iso19794_2_fmr,
    /**
     * Finger Minutiae Card Record, Compact Size, minutiae ordered by Ascending Angle.</br>
     * Public fingerprint template format, dedicated to smart card, defined by the ISO organization, with minutiae ordered by ascending angle.
     */
    iso19794_2_fmc_cs_aa,
    /** Public fingerprint template format, defined by the NIST organisation for MINEX testing.*/
    minex_a,
    /**
     * DIN V66400 Finger Minutiae Card Record.</br>
     * Public fingerprint template format, dedicated to use with Smart Cards to perform a Match On Card.
     */
    din_v66400_cs,
    /**
     * DIN V66400 Finger Minutiae Card Record, Compact Size, minutiae ordered by Ascending Angle.</br>
     * Public fingerprint template format, dedicated to use with Smart Cards to perform a Match On Card, with minutiae ordered by ascending angle.
     */
    din_v66400_cs_aa,
    /**
     * Morpho private multimodal template format which contains the fingerprint data and the vein data of a finger.</br>
     * This is the format that shall be used for best performance, on FingerVein terminals.
     */
    multimodal,
    /**
     * L1/Bioscrypt legacy native fingerprint template format.</br>
     * This shall be used only for L1/Bioscrypt legacy mode for user_DB_set_users command.
     */
    bioscrypt,
    /**
     * PKLITE is newly added template type in Sensor SDK.
     */
    pklite,
}

struct User_templates
{
    /** Type of the template.*/
    1: required Biofinger_template_type template_type;
    /** Ttemplate data.*/
    2: required binary                                  template_data;
}

struct Biofinger_enroll_final_result
{
    /**
     * Indicate enrollment result.</br>
     * True for success, false for error.
     */
    1: required bool                            success,
    /**
     * Indicate the cause of the error.</br>
     * Present if success field is false.
     */
    2: optional Biofinger_failure_cause         cause,
    /**
     * Binary fingerprint templates of the user.</br>
     * Present if success is true and templates are required in the command.
     */
    3: optional list<User_templates>                    fp_templates,
    /**
     * Binary fingervein templates of the user.</br>
     * Present if success is true and templates are required in the command.
     */
    4: optional list<User_templates>                    fv_templates,
    /**
     * Binary result best images of the fingers.</br>
     * Present if success is true and images are required in the command (see Biofinger_enrolloptional_param::require_best_fingers_images).</br>
     * 1 image per finger.
     */
    5: optional list<Biofinger_sensor_image>    best_finger_images,
    /**
     * Result qualities of the captured fingers.</br>
     * Present if success is true and final qualities are required in the command (see Biofinger_enroll_optional_param::require_fingers_qualities).</br>
     * 1 quality per finger.
     */
    6: optional list<byte>                      finger_qualities,
    /**
     * Indicate if the enrolled templates complies with sensor security level.</br>
     * Present if requested in the command (see Biofinger_enroll_optional_param::require_security_compatibilty).</br>
     * 1 parameter per finger.
     */
    7: optional list<i16>                       security_compatibilities,
}


struct Biofinger_callback_enrollment_step
{
    /** Current finger number for the enrollment process (starting to 1).*/
    1: required byte current_finger,
    /** Total number of fingers for the enrollment process.*/
    2: required byte total_finger,
    /** Current capture of the current finger (starting to 1).*/
    3: required byte current_capture,
    /** Total number of captures for one finger.*/
    4: required byte total_capture
}

struct Biofinger_enroll_operation_reply
{
    /**
     * Final reply of authenticate/identify command. </br>
     * If final_result is present, none of the other fields shall be
     * present.
     */
    1: optional Biofinger_enroll_final_result        final_result,
    /**
     * Intermediate reply that is used to:
     * <ul>
     * <li>indicate that there is a wrongly placed finger on the sensor, and then the action that the user has to perform.</li>
     * <li>provide information about the state of the fingerprint process (fingerprint wait started, fingerprint acquisition completed).</li>
     * </ul>
     * It shall have been requested in the command (see @a Biofinger_async_event::finger_positions).
     */
    2: optional Biofinger_callback_command          cb_bio_command,
    /**
     * Intermediate reply that is used to transmit images from the sensor whatever there is a fingerprint or not.</br>
     * The terminal sends live images in low resolution until the end of the fingerprint acquisition process, with a reduced size to provide a convenient image throughput.</br>
     * It shall have been requested in the command (see @a Biofinger_async_event::low_resol_live_images).
     */
    3: optional Biofinger_sensor_image              cb_low_resol_live_image,
    /**
     * Intermediate reply that is used to indicate the enrollment process steps.</br>
     * For example, during the enrollment of one finger with three images, the terminal sends three messages (enrollment of finger 1 of 1, acquisition 1, 2 and 3).</br>
     * It shall have been requested in the command (see @a Biofinger_async_event::enrollment_steps).
     */
    4: optional Biofinger_callback_enrollment_step   cb_enroll_step,
    /**
     * Intermediate reply that is used to transmit only one image: the image of the current capture (May be several capture per finger).</br>
     * It shall have been requested in the command (see @a Biofinger_async_event::high_resol_captures_image).
     */
    5: optional Biofinger_sensor_image              cb_high_resol_capture_image,
    /**
     * Intermediate reply that is used to provide the quality value of the capture (May be several capture per finger).</br>
     * It shall have been requested in the command (see @a Biofinger_async_event::captures_quality).
     */
    6: optional i32                                 cb_capture_quality,
    /**
     * Intermediate reply that is used to provide the quality note of the live fingerprint image, which is calculated by the presence detection function.</br>
     * It shall have been requested in the command (see @a Biofinger_async_event::live_quality).
     */
    7: optional i32                                 cb_live_quality
}

struct Biofinger_control_operation_reply
{
    /**
     * Final reply of authenticate/identify command. </br>
     * If final_result is present, none of the other fields shall be
     * present.
     */
    1: optional Biofinger_control_final_result      final_result,
    /**
     * Intermediate reply that is used to:
     * <ul>
     * <li>indicate that there is a wrongly placed finger on the sensor, and then the action that the user has to perform.</li>
     * <li>provide information about the state of the fingerprint process (fingerprint wait started, fingerprint acquisition completed).</li>
     * </ul>
     * It shall have been requested in the request (see @a Biofinger_async_event::finger_positions).
     */
    2: optional Biofinger_callback_command          cb_bio_command,
    /**
     * Intermediate reply that is used to transmit images from the sensor whatever there is a fingerprint or not.</br>
     * The terminal sends live images in low resolution until the end of the fingerprint acquisition process, with a reduced size to provide a convenient image throughput.</br>
     * It shall have been requested in the command (see @a Biofinger_async_event::low_resol_live_images).
     */
    3: optional Biofinger_sensor_image              cb_low_resol_live_image,
    /**
     * Intermediate reply that is used to transmit only one image: the image of the current capture (May be several capture per finger).</br>
     * It shall have been requested in the command (see @a Biofinger_async_event::high_resol_captures_image).
     */
    4: optional Biofinger_sensor_image              cb_high_resol_capture_image,
    /**
     * Intermediate reply that is used to provide the quality value of the acquired fingerprint image.</br>
     * It shall have been requested in the command (see @a Biofinger_async_event::captures_quality).
     */
    5: optional i32                                 cb_capture_quality,
    /**
     * Intermediate reply that is used to provide the quality note of the live fingerprint image, which is calculated by the presence detection function.</br>
     * It shall have been requested in the command (see @a Biofinger_async_event::live_quality).
     */
    6: optional i32                                 cb_live_quality
}

/** Enumeration representing the events that can be monitored.*/
enum Biofinger_async_event
{
    finger_positions,
    low_resol_live_images,
    enrollment_steps,
    high_resol_captures_image,
    captures_quality,
    live_quality
}

/** Enumeration representing the MSI/FVP security level to use.*/
enum Biofinger_sensor_security_level
{
    MSIFFD_low,
    MSIFFD_medium,
    MSIFFD_high,
    FVP_standard,
    FVP_medium,
    FVP_high
}

/* Shall not be used
enum Biofinger_sensor_coder
{
    standard_coder,
    juvenile_coder,
    thin_finger_coder
}
*/

/** Enumeration representing the matching strategy to apply.*/
enum Biofinger_sensor_matching_strategy
{
    standard_strategy,
    advanced_strategy
}

struct Biofinger_control_optional_param
{
    /** List of event to subscribe to.*/
    1: optional list<Biofinger_async_event>         events,
    /** Matching score is required in final answer.*/
    2: optional bool                                require_matching_score,
    /** On MSI or VP equipped terminals, indicate the security level to use for the operation.*/
    3: optional Biofinger_sensor_security_level     security_level,
    /** Shall not be used.*/
    4: optional i32                                 coder,
    /** Shall not be used.*/
    5: optional i32                                 detection_mode,
    /** Shall not be used, right now.*/
    6: optional Biofinger_sensor_matching_strategy  matching_strategy,
}

struct Biofinger_enroll_optional_param
{
    /** List of event to subscribe to.*/
    1: optional list<Biofinger_async_event>         events,
    /** Specify the format of the fingerprint templates to be exported.*/
    2: optional Biofinger_template_type             fp_template_format,
    /** Specify the format of the fingervein templates to be exported. (FingerVein-equipped terminals only)*/
    3: optional Biofinger_template_type             fv_template_format,
    /** Best image of each captured fingers is required in the reply.*/
    4: optional bool                                require_best_fingers_images,
    /**
     * Require latent detection.</br>
     * Not recommanded for standard enrollment.
     * TODO: Will be removed if Enroll CBI API does not allow it
     */
    5: optional bool                                require_latent,
    /** On MSI or VP equipped terminals, indicate the security level to use for the operation.*/
    6: optional Biofinger_sensor_security_level     security_level,
    /** Shall not be used.*/
    7: optional i32                                 coder,
    /** Shall no be used.*/
    8: optional i32                                 detection_mode,
    /** Quality of each captured fingers is required in the reply.*/
    9: optional bool                                require_fingers_qualities,
    /** Compliance with sensor security level is required in the reply.*/
    10: optional bool                               require_security_compatibilty
}

/** Enumeration representing the operation of the enrollment process.*/
enum Enrollment_type
{
    store,
    transfer,
    both
}

/**
 * The finger was misplaced or has been withdrawn during finger acquisition performed.</br>
 * On FingerVein-equipped terminals only.
 */
exception Misplaced_finger_error
{
    /** Error code that represents the error.*/
    1: required Generic_types.Generic_error_code err_code
}

/** The format of the fingerprint template is not supported, or the fingerprint data does not match its type.*/
exception Unsupported_format_error
{
    /** Error code that represents the error.*/
    1: required Generic_types.Generic_error_code err_code
}

/** A reference template does not match sensor security policy.*/
exception Incompatible_ref_error
{
    /** Error code that represents the error.*/
    1: required Generic_types.Generic_error_code err_code
}

/** User uses a finger more than once.*/
exception Duplicated_finger_error
{
    /** Error code that represents the error.*/
    1: required Generic_types.Generic_error_code err_code
}
