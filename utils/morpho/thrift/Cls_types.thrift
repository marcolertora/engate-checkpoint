/**
 * @section LICENSE
 * Copyright &copy; 2012 Safran Morpho - Safran Morpho confidential - all rights reserved
 *
 * @section DESCRIPTION
 *
 *
 * @file Cls_types.thrift
 *
 * CHANGELOG
 * 23 nov 2012  - Initiate header
 * 10 dec 2012  - Change namespace to comply MPH coding rules.
 * 05 mar 2013  - Added 'Cls_invalid_card_type_error' exception.
 *              - Added 'Cls_card_type' enum.
 * 13 mar 2013  - Removed 'Cls_key' struct.
 *              - Added 'Cls_key_iclass', 'Cls_key_mifare' and Cls_key_desfire' struct.
 *              - Modified 'Cls_desfire_application' and 'Cls_desfire_card' struct.
 *              - Renamed 'Cls_mif_classic_sector' struct to 'Cls_mifare_sector' and modified it.
 *              - Renamed 'Cls_mif_classic_card' struct to 'Cls_mifare_card' and modified it.
 *              - Modified 'Cls_card_definition' struct.
 *              - Renamed 'Cls_mif_classic_security_policy' enum to 'Cls_mifare_security_policy'
 * 14 mar 2013  - Added 'cls_authent_user_params' and 'cls_authent_user_reply' struct.
 *              - Added 'cls_authent_user_checks' and 'cls_authent_user_final_result' enum.
 * 15 mar 2013  - Added 'Cls_iclass_card' struct and modified 'Cls_cards_definition' struct.
 * 15 mar 2013  - Added 'wiegand_string' in 'Cls_prox_card' struct.
 * 23 may 2013  - Updated structure 'Cls_prox_card', added member 'user_id', 'port_id' and 'protocol_type'
 * 20 jul 2013  - Update Cls_iclass_card, Cls_desfire_file and Cls_mifare_card struct to support
 *                the file to encode.
 * 25 Jul 2013  - Added structure 'Cls_key_l1'
 *              - Updated enum 'Cls_card_type', added element 'l1_site_key'
 * 27 Jul 2013  - Added enum 'Cls_keys_update_type'
 * 02 Aug 2013  - Removed Internal command enums
 * 05 Aug 2013  - Addec comment 
 * 06 Aug 2013  - Updated structure 'Cls_key_iclass', 
 *              - Renamed member 'key' to 'key_1' 
 *              - added member 'key_2' 
 * 14 Aug 2013  - Added comments in 'Cls_key_desfire' structure
 * 16 Aug 2013  - Added structure 'Crypto_keys'
 *              - Added structure 'Cls_key_rsa'
 *              - Updated structure 'Cls_key_iclass', Added member 'validity_start', 'validity_duration' and 'version'
 *              - Updated structure 'Cls_key_mifare' Added member 'validity_start', 'validity_duration' and 'version'
 *              - Updated enumeration 'Cls_card_type', Added elements 'rsa1024'
 * 13 Sept 2013 - Added comments for Cls key version
 */

namespace cpp Distant_cmd

include "Generic_types.thrift"
include "Security_types.thrift"
include "Biofinger_types.thrift"

/**
 * Contactless card type.
 */
enum Cls_card_type
{
    mifare_classic,
    mifare_aes,
    mifare_desfire_3des,
    mifare_desfire_aes,
    iclass,
    l1_site_key,
    rsa1024,
}

/**
 * Contactless card information.
 */
enum Cls_iso14443_layer
{
    level_3,
    level_4
}

enum Cls_iso14443_type
{
    type_A,
    type_B
}

struct Cls_iso14443_card
{
    /** Indicates if the detected card is compliant to level 3 or 4 of ISO14443 standard*/
    1: required Cls_iso14443_layer  iso14443_layer,
    /** Indicates if the detected card is an ISO14443 B or A card*/
    2: required Cls_iso14443_type   iso14443_type,
    /** Serial number of detected card*/
    3: required binary              serial_number
    /** Serial number of detected card in string format*/
    4: required string              user_id_string
}

struct Cls_prox_card
{
    /** Serial number of detected card(User ID extracted from complete wiegand string), e.g. format of binary data is, For decimal number 12 it's equivalent binary(i.e. 1100) and each bit should be in seperate byte(i.e. 0x01, 0x01, 0x00, 0x00)*/
    1: required binary              serial_number,
    /** Whole wiegand string of detected card*/
    2: required binary              wiegand_string,
    /** user id in string format for ex "12345"*/
    3: required string              user_id,
    /** port id from which data came*/
    4: required i16 port_id,
    /** 0 for wiegand protocol & 1 for clock&data protocol*/
    5: required Generic_types.Wiegand_protocol_type protocol_type
}

/**
 * Contains information about detected card
 *
 *
 * The card can be ISO14443 compliant or a Prox card. But not both.
 */
struct Cls_card_info
{
    1: optional Cls_iso14443_card   iso14443_card,
    2: optional Cls_prox_card       prox_card
}

struct Cls_info
{
    1: required Cls_card_info card_info;
}

/**
 * Contactless key algorithm
 */
enum Cls_algo
{
    /** For MIFARE Classic */
    algo_crypto1,
    /** For MIFARE DESFire (legacy)*/
    algo_legacy3des,
    /** For MIFARE Plus and MIFARE DESFire EV1 */
    algo_aes128,
}

/**
 * List of supported diversification algorithms
 */
enum Cls_diversify_algo
{
    /** Diversify the key using MorphoAccess algorithm */
    diversify_morpho,

    /** Diversify the key using Bioscrypt algorithm */
    diversify_bioscrypt,
}

/**
 * iClass contactless key.
 */
struct Cls_key_iclass
{
    /**
     * Sector index (0 to 8).<br/>
     * Index 0 to 7 for BOOK 0<br/>
     * Index 8 for BOOK 1<br/>
     */
    1: required byte                             index;

    /**
     * Value of the key 1 (8 bytes).
     */
    2: optional binary                              key_1;

    /**
     * Value of the key 2 (8 bytes).
     */
    3: optional binary                              key_2;
    
    /**
     * Key validity start date (Only date is used. Time is not used).
     */
    4: required Generic_types.Date_time             validity_start;
    
    /**
     * Key validity duration (in days).<br/>
     * If 0, then infinite time to live duration (default value).
     */
    5: optional i32                                 validity_duration;
    
    /**
     * Key version.<br/>
     * For a key, if the version is different from 0,
     * the version for a new value to set must be superior to the previous one.<br/>
     * If not present, 0 will be used as default value.
     *
     * Version range: 0 to 255
     */
    6: optional i32                                 version;
}

/**
 * Mifare Classic and Plus contactless key.<br/>
 * At least one of the key (A or B) must be provided.
 */
struct Cls_key_mifare
{
    /**
     * Key algorithm.<br/> 
     * Valid algo: algo_crypto1, algo_aes128
     */
    1: required Cls_algo                            algo;

    /**
     * Sector index (0 to 39).
     */
    2: required byte                                index;

    /**
     * Value of the key A (6 bytes), if algo is algo_crypto1.<br/>
     * Value of the key A (16 bytes), if algo is algo_aes128.
     */
    3: optional binary                              keyA;

    /**
     * Value of the key B (6 bytes), if algo is algo_crypto1.<br/>
     * Value of the key B (16 bytes), if algo is algo_aes128.
     */
    4: optional binary                              keyB;
    
    /**
     * Key validity start date (Only date is used. Time is not used).
     */
    5: required Generic_types.Date_time             validity_start;
    
    /**
     * Key validity duration (in days).<br/>
     * If 0, then infinite time to live duration (default value).
     */
    6: optional i32                                 validity_duration;
    
    /**
     * Key version.<br/>
     * For a key, if the version is different from 0,
     * the version for a new value to set must be superior to the previous one.<br/>
     * If not present, 0 will be used as default value.
     *
     * Version range: 0 to 255
     */
    7: optional i32                                 version;
}

/**
 * DESFire contactless key
 */
struct Cls_key_desfire
{
    /**
     * Key algorithm.<br/>
     * Valid algo: algo_legacy3des, algo_aes128
     */
    1: required Cls_algo                            algo;

    /**
     * ID of the key inside the terminal secure container.<br/>
     * List of the IDs used when reading/writing a MorphoAccess card:
     *
     * <br/><b>DESFire Morpho cards</b>
     * <table><tr><th>ID</th><th>Description</th></tr>
     * <tr><td>    0      </td><td>    Master PICC key.         </td></tr>
     * <tr><td>    1      </td><td>    Application master key.  </td></tr>
     * <tr><td>    2      </td><td>    File read key.           </td></tr>
     * </table>
     *
     * <br/><b>DESFire ADP cards</b>
     * <table><tr><th>ID</th><th>Description</th></tr>
     * <tr><td>    3      </td><td>    Master PICC key.         </td></tr>
     * <tr><td>    4      </td><td>    Application master key.  </td></tr>
     * <tr><td>    5      </td><td>    ID file read key.        </td></tr>
     * <tr><td>    6      </td><td>    ID file write key.       </td></tr>
     * <tr><td>    7      </td><td>    BIO file read key.       </td></tr>
     * <tr><td>    8      </td><td>    BIO file write key.      </td></tr>
     * <tr><td>    9      </td><td>    PIN file read key.       </td></tr>
     * <tr><td>    10     </td><td>    PIN file write key.      </td></tr>
     * <tr><td>    11     </td><td>    Template cipher key.     </td></tr>
     * </table>
     *
     * <br/>
     * If algo = algo_aes128
     * ID Range: 0 to 15<br/>
     * <br/>
     * If algo = algo_legacy3des
     * ID Range: 0 to 16<br/>
     * Key with id = 16 will be used to decrypt ADP cards
     */
    2: required Security_types.Sec_obj_ID           id;

    /**
     * Value of the key (16 bytes).
     */
    3: required binary                              data;

    /**
     * Key validity start date (Only date is used. Time is not used).
     */
    4: required Generic_types.Date_time             validity_start;
    
    /**
     * Key validity duration (in days).<br/>
     * If 0, then infinite time to live duration (default value).
     */
    5: optional i32                                 validity_duration;
    
    /**
     * Key version.<br/>
     * For a key, if the version is different from 0,
     * the version for a new value to set must be superior to the previous one.<br/>
     * If not present, 0 will be used as default value.
     *
     * Version range: 0 to 255
     */
    6: optional i32                                 version;
}


/**
 * L1 site key
 */
struct Cls_key_l1
{
    /**
     * Sector index (0 or 1). 0 - Primary key, 1 - Secondary key
     */
    1: required byte                                index;
    /**
     * Value of the key (16 bytes).
     */
    2: required binary                              data;
}




/**
 * RSA key structure.<br/>
 * 
 */
struct Cls_key_rsa
{
    /**
     * Index (0 to 15).
     */
    1: required byte                                index;

    /**
     * Value of the private exponent (128 bytes).
     */
    2: optional binary                              private_exp;
    /**
     * Value of the modulo (128 bytes).
     */
    3: optional binary                              modulo;

    /**
     * Value of the public exponent (4 bytes).
     */
    4: optional binary                              public_exp;
    
    /**
     * Key validity start date (Only date is used. Time is not used).
     */
    5: required Generic_types.Date_time             validity_start;
    
    /**
     * Key validity duration (in days).<br/>
     * If 0, then infinite time to live duration (default value).
     */
    6: optional i32                                 validity_duration;
    
    /**
     * Key version.<br/>
     * For a key, if the version is different from 0,
     * the version for a new value to set must be superior to the previous one.<br/>
     * If not present, 0 will be used as default value.
     *
     * Version range: 0 to 255
     */
    7: optional i32                                 version;
}

/**
 * DESFire file ID
 *
 *
 * Allowed values for a DESFire file ID are from 0x00 to 0x1F.
 */
typedef byte Cls_desfire_file_id

/**
 * Defines the level of security for the communication with the reader
 * (according to DESFire MF3ICD81 functional specification).
 */
enum Cls_desfire_file_security
{
    /** Plain communication*/
    plain_comm,

    /** Plain communication secured by MACing*/
    macing,

    /** Fully enciphered communication*/
    full_enciphered,
}

/**
 * DESFire file access right
 */
enum Cls_desfire_app_key
{
    /** Authentication with master application key needed*/
    access_right_master_app_key = 0;
    /** Authentication with application key 1 needed*/
    access_right_key_1          = 1;
    /** Authentication with application key 2 needed*/
    access_right_key_2          = 2;
    /** Authentication with application key 3 needed*/
    access_right_key_3          = 3;
    /** Authentication with application key 4 needed*/
    access_right_key_4          = 4;
    /** Authentication with application key 5 needed*/
    access_right_key_5          = 5;
    /** Authentication with application key 6 needed*/
    access_right_key_6          = 6;
    /** Authentication with application key 7 needed*/
    access_right_key_7          = 7;
    /** Authentication with application key 8 needed*/
    access_right_key_8          = 8;
    /** Authentication with application key 9 needed*/
    access_right_key_9          = 9;
    /** Authentication with application key 10 needed*/
    access_right_key_10         = 10;
    /** Authentication with application key 11 needed*/
    access_right_key_11         = 11;
    /** Authentication with application key 12 needed*/
    access_right_key_12         = 12;
    /** Authentication with application key 13 needed*/
    access_right_key_13         = 13;
    /** Access always granted*/
    access_right_always         = 14;
    /** Access always denied*/
    access_right_never          = 15;
}

/**
 * DESFire file access rights
 */
struct Cls_desfire_file_access_rights
{
    /** Defines the needed authentication to perform a reading*/
    1: required Cls_desfire_app_key   read_access;

    /** Defines the needed authentication to perform a writing*/
    2: required Cls_desfire_app_key   write_access;

    /** Defines the needed authentication to perform both reading and writing */
    3: required Cls_desfire_app_key   read_write_access;

    /** Defines the needed authentication to modify access rights*/
    4: required Cls_desfire_app_key   chmod_access;
}

/** DESFire file */
struct Cls_desfire_file
{
    /** File ID, from 0x00 to 0x1F*/
    1: required Cls_desfire_file_id             id;
    /** File security*/
    2: required Cls_desfire_file_security       security;
    /** File access rights*/
    3: required Cls_desfire_file_access_rights  access_rights;
    /** For writing operation only, the file to encode*/
    4: optional binary                          file;
}

/**
 * DESFire® application AID number (according to DESFire® MF3ICD84 functional specification).
 * Only the lower 24 bits shall be used.
 */
typedef i32 Cls_application_id

/**
 * DESFire key settings
 *
 *
 * See ChangeKeySettings function in DESFire MF3ICD81 functional specification.
 */
typedef byte Cls_desfire_key_settings

/** DESFire application */
struct Cls_desfire_application
{
    /**
     * DESFire® application AID number (according to DESFire® MF3ICD84 functional specification).<br>
     * @warning AID number 0x000000 is reserved as a reference to the card level (PICC) itself and cannot be used.
     */
    1: required Cls_application_id                  app_id;
    /**
     * Key algorithm.
     */
    2: required Cls_algo                            algo;
    /**
     * Diversification algorithm.<br>
     * If not present, no diversification will be performed on the application keys.
     */
    3: optional Cls_diversify_algo                  diversify;
    /**
     * Application key settings<br>
     * See ChangeKeySettings function in DESFire MF3ICD81 functional specification.
     */
    4: required Cls_desfire_key_settings            app_key_settings;
    /** Application keys*/
    5: required map<Cls_desfire_app_key, Security_types.Sec_obj_ID>   keys;
    /** List of files to read, write or erase from the application*/
    6: required list<Cls_desfire_file>              file;
}

/** DESFire card structure definition*/
struct Cls_desfire_card
{
    /**
     * Master PICC key<br>
     * The master PICC key is not needed for reading, but may be needed for writing or formatting
     */
    1: optional Security_types.Sec_obj_ID    master_picc_key;
    /**
     * Key algorithm (required if Master PICC key is provided).
     */
    2: optional Cls_algo                            algo;
    /**
     * Diversification algorithm.<br>
     * If not present, no diversification will be performed on the PICC key.
     */
    3: optional Cls_diversify_algo                  diversify;
    /**
     * PICC key settings<br>
     * See ChangeKeySettings function in DESFire MF3ICD81 functional specification.
     */
    4: optional Cls_desfire_key_settings            picc_key_settings;
    /** List of DESFire applications to read, write or erase*/
    5: required list<Cls_desfire_application>       applications;
}

/** MIFARE security policy*/
enum Cls_mifare_security_policy
{
    /** For read or write*/
    mifare_key_A = 0;
    /** For read or write*/
    mifare_key_B = 1;
    /** For read only */
    mifare_key_A_then_B = 2;
}

/** A list of MIFARE blocks with corresponding policy*/
struct Cls_mifare_blocks_list
{
    /** Index of start block*/
    1: required byte                            index;
    /** Security policy for read and write operations*/
    2: required Cls_mifare_security_policy      security_policy;
    /** For reading operation only, the number of blocks to read*/
    3: optional byte                            nb_blocks
}

/**
 * MIFARE Classic or Plus card structure definition
 *
 *
 * A MIFARE Classic or Plus card is just a list of sectors.
 */
struct Cls_mifare_card
{
    /** The list of blocks to read or write*/
    1: required Cls_mifare_blocks_list blocks;
    /**
     * Algorithm.
     */
    2: required Cls_algo                            algo;
    /**
     * Diversification algorithm.<br>
     * If not present, no diversification will be performed on the keys.
     */
    3: optional Cls_diversify_algo                  diversify;
    /** For writing operation only, the file to encode*/
    4: optional binary                          file;
}

/**
 * iClass card structure definition
 */
struct Cls_iclass_card
{
    /**
     * Page offset.</br>
     * When using a 2K2 card (card containing only 2 applications in 1 page),
     * this parameter specifies the starting block address to read/write data.<br/>
     * Minimum value is 0x13 (default value if parameter is not present). 
     * Maximum value is 0xFF.
     */
    1: optional byte    page_offset;
    /**
     * Book number.<br/>
     * When using a card containing more than one book (32K cards),
     * this parameter specifies the book to use.<br/>
     * Value is 0 (default value if parameter is not present) or 1.
     */
    2: optional byte    book_number;
    /**
     * Book layout.<br/>
     * The book layout parameter specifies which pages and application areas the terminal 
     * is going to use when a 16 application areas card is presented.<br/>
     * Even bits (0 based) are flags that mark the application area 1 of the page for use by the terminal.<br/>
     * Odd bits (0 based) are flags that mark application area 2 of the page for use by the terminal.<br/>
     * <table><tr><th>Bit</th><th>Description</th></tr>
     * <tr><td>0</td><td>Page 0, application area 1</td></tr>
     * <tr><td>1</td><td>Page 0, application area 2</td></tr>
     * <tr><td>2</td><td>Page 1, application area 1</td></tr>
     * <tr><td>...</td><td>...</td></tr>
     * <tr><td>14</td><td>Page 7, application area 1</td></tr>
     * <tr><td>15</td><td>Page 7, application area 2</td></tr>
     * </table><br/>
     * If the parameter is not present, the terminal will use all application areas, 
     * starting at page 1, application area 1.
     */
    3: optional i16     book_layout;
    /**
     * If not present or set to false, no diversification will be performed on the key.
     */
    4: optional bool    diversify
    /** For writing operation only, the file to encode*/
    5: optional binary  file;
}

/** Contactless card definition*/
struct Cls_cards_definition
{
    /** Optional list of zero or more DESFire cards definition to operate on*/
    1: optional list<Cls_desfire_card>      desfire_cards;
    /** Optional list of zero or more MIFARE Classic or Plus cards definition to operate on*/
    2: optional list<Cls_mifare_card>  mifare_cards;
    /** Optional list of zero or more iClass cards definition to operate on*/
    3: optional list<Cls_iclass_card>  iclass_cards;
}

enum Cls_card_mode
{
    id_only,
    bio,
    pin,
    pin_bio
}

/** User contactless card */
struct Cls_user_card
{
    1: required string user_ID_UTF8,
    2: required Cls_card_mode card_mode,
    3: optional binary template_1,
    4: optional binary template_2,
    5: optional binary pin_code,
    6: optional binary biopin_code,
    7: optional string user_name_UTF8,
    8: optional Generic_types.Date_time expiry_date
}

enum cls_authent_user_checks
{
    /** Authenticate user against biometric data contained in the card */
    biometric,
    /** Check PIN entered by user against BIOPIN contained in the card */
    PIN,
    /** Check BIOPIN entered by user against BIOPIN contained in the card */
    BIOPIN,
}

/**
 * Structure representing parameters for authenticating an user 
 * using data contained in a contactless card.
 * 
 * @warning If @a enable_intermediate_replies is true, you will need a modified version of the Thrift client that supports
 *          the reception of several T_REPLY messages for one command.
 */
struct cls_authent_user_params
{
    /** Use card mode information from card.<br/>
      * If set to true, all verifications (biometric, PIN, BIOPIN) 
      * will be done depending policy stored in the card.
      */
    1: optional bool    use_card_mode,
    /** List of the verifications to perform.<br/>
      * This parameter is ignored if card mode is set to true.
      */
    2: optional list<cls_authent_user_checks>    check_list,
    /** This parameter specifies the value of the False Acceptance Ratio (FAR) of the MorphoSmart\99 device.<br>
      * The value of this parameter can be set from 0 to 10, by 1 value steps.<br/>
      * This parameter is used and required only if a biometric verification is performed 
      * (depending on card mode and biometric check parameters ). Otherwise, it is ignored.
      */
    3: optional byte    threshold,
    /** If set to false, you will receive only one reply containing the final result of the
      * authentication, otherwise you may also receive asynchronous replies containing the
      * progress status of the authentication.<br/>
      * This parameter is used and required only if a biometric verification is performed 
      * (depending on card mode and biometric check parameters ). Otherwise, it is ignored.
      */
    4: optional bool    enable_intermediate_replies,
    /** Biometric check optional parameters
      * This parameter is used and required only if a biometric verification is performed 
      * (depending on card mode and biometric check parameters ). Otherwise, it is ignored.
      */
    5: Biofinger_types.Biofinger_control_optional_param bio_optional_param
}

enum cls_authent_user_final_result
{
    verification_succeeded,
    PIN_verification_failed,
    BIOPIN_verification_failed,
    biometric_verification_failed,
    
}

struct cls_authent_user_reply
{
    /**
     * Final reply of "authenticate user with data in contactless card" command.<br/>
     * If final_result is present, it is the final reply.
     */
    1: optional cls_authent_user_final_result       final_result,
    /**
     * This result is present in these contexts:
     * <ul>
     * <li>Final reply containing the biometric result details.</li>
     * <li>Intermediate reply containing information on the biometric check in progress.</li>
     * </ul>
     */
    2: optional Biofinger_types.Biofinger_control_operation_reply   bio_result,
}

/**
 * Structure to manage keys.<br/>
 * At least one key list must be provided
 */
struct Crypto_keys
{
    /** Optional list of MIFARE keys*/
    1: optional list<Cls_key_mifare>  mifare_keys;
    /** Optional list of DESFire keys*/
    2: optional list<Cls_key_desfire> desfire_keys;
    /** Optional list of iClass keys*/
    3: optional list<Cls_key_iclass>  iclass_keys;
    /** Optional list of L1 site keys*/
    4: optional list<Cls_key_l1>  l1_keys;
    /** Optional list of RSA keys*/
    5: optional list<Cls_key_rsa> rsa_keys;
}

/** Invalid contactless key specified*/
exception Cls_invalid_key_error
{
    1: required Generic_types.Generic_error_code err_code;
}

/** Invalid contactless card type*/
exception Cls_invalid_card_type_error
{
    1: required Generic_types.Generic_error_code err_code;
}
