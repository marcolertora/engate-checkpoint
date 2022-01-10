/**
 * @section LICENSE
 * Copyright &copy; 2012 Safran Morpho - Safran Morpho confidential - all rights reserved
 *
 * @section DESCRIPTION
 *
 *
 * @file Security_types.thrift
 *
 * CHANGELOG
 * 23 nov 2012 - Initiate header
 * 10 dec 2012 - Change namespace to comply MPH coding rules.
 * 25 Jul 2013 - Added enum 'Passphrase_id'
 */

include "Generic_types.thrift"

namespace cpp Distant_cmd

/**
 * Security object identifier
 */
typedef i32 Sec_obj_ID

/**
* Enum for Passphrase ID
*/
enum Passphrase_id
{
    SSL_profile_0 = 0,
    SSL_profile_1,
}
/**
 * Security object identifier not found in the terminal secure container
 */
exception Sec_obj_ID_not_found_error
{
    1: required Generic_types.Generic_error_code  err_code;
}
