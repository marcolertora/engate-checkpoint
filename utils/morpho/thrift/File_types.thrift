/**
 * @section LICENSE
 * Copyright &copy; 2012 Safran Morpho - Safran Morpho confidential - all rights reserved
 *
 * @section DESCRIPTION
 *
 *
 * @file File_types.thrift
 *
 * CHANGELOG
 * 23 nov 2012 - Initiate header
 * 10 dec 2012 - Change namespace to comply MPH coding rules.
 * 07 feb 2013 - Added 'File_subtype' enum and 'File_details' structure.
 * 16 feb 2013 - Renamed 'File_details.name' to 'File_details.name_UTF8'
 * 20 feb 2013 - Added 'stolen_card_list' in 'File_type' enum
 *             - Make subtype optional in File_details
 * 05 mar 2013 - Added 'diagnostic_info' in 'File_type' enum
 * 05 mar 2013 - Added 'ssl_component' in 'File_type' enum
 * 29 mar 2013 - Renamed 'ssl_component' to 'SSL_component' in 'File_type' enum
 *             - Changed 'File_subtype' enum
 * 31 mar 2013 - Added 'language' entry to 'File_type' enum
 * 14 aug 2013 - Added comment for enum play in 'File_action' 
 * 07 oct 2013 - Removed 'picture_slideshow' element from enum 'File_subtype'
 * 08 oct 2013 - Added 'firmware_upgrade' to enum 'File_type'
 */

namespace cpp Distant_cmd

enum File_type
{
    video,
    audio,
    picture,
    stolen_card_list,
    diagnostic_info,
    language,
    SSL_component,
    firmware_upgrade,
}

enum File_subtype
{
    // Video file subtypes
    no_subtype,

    // Audio file subtypes
    audio_verification_failed,
    audio_verification_succeeded,
    audio_message_attention,
    audio_tamper,
    audio_test,

    // Picture file subtypes
    picture_dynamic_message,
    picture_wallpaper,
    
    // SSL_component subtypes
    SSL_profile_0,
    SSL_profile_1,
}

struct File_details
{
    1: File_type type;
    2: optional File_subtype subtype;
    3: optional string name_UTF8;
}

enum File_action
{
    /** Do nothing after upload  */
    nothing,
    /** Play file after upload, only applicable for audio and picture files */
    play
}

struct File_chunk
{
    /** File index of the data present in this chunk */
    1: i32      index;
    /** Set to true if this chunk is the last, false otherwise */
    2: bool     is_last;
    /** File data */
    3: binary   data;
    /** Action performed after transfer */
    4: optional File_action action;
}