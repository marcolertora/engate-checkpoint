/**
 * @section LICENSE
 * Copyright &copy; 2012 Safran Morpho - Safran Morpho confidential - all rights reserved
 *
 * @section DESCRIPTION
 *
 *
 * @file Config_types.thrift
 *
 * CHANGELOG
 * 23 nov 2012  - Initiate header
 * 10 dec 2012  - Change namespace to comply MPH coding rules.
 * 14 dec 2012  - Add comments
 */

include "Generic_types.thrift"

namespace cpp Distant_cmd

/** The requested parameter does not exist in terminal configuration database.*/
exception Config_inexistent_parameter_error
{
    1: required Generic_types.Generic_error_code    err_code,
    2: required string                              parameter_name_UTF8
}

/** The specified value for the requested parameter is invalid.*/
exception Config_invalid_value_error
{
    1: required Generic_types.Generic_error_code    err_code,
    2: required string                              parameter_name_UTF8
}
