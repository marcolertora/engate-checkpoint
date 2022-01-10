// DemoTarghe.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

#include "dvsH.h"
#include "dvs.nsmap"
#include "dvsStub.h"

static void *dime_write_open(struct soap *soap, const char *id,
                             const char *type, const char *options);
static void  dime_write_close(struct soap *soap, void *handle);
static int   dime_write(struct soap *soap, void *handle,
                        const char *buf, size_t len);


int
_tmain(int argc, _TCHAR* argv[])
{
    int cam;
    // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    // Specify the service url to connect to, where the IP is the DVS IP
    // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#define SERVER "http://83.211.218.157:8888/dvs.cgi"
    char *server = SERVER;
    struct soap soap;
    // Dime variables.
    struct CamerasCntxArray camerasCntx;
    struct ns1__DimeData *dmd;
    struct DimeDataArray dimeDataArray;


    // Init gSOAP.
    soap_init(&soap);

    // Set DIME callbacks.
    //
    // DIME gSOAP callbacks method according to the manual gSOAP chapter:
    //
    //   15.4 Streaming DIME
    soap.fdimewriteopen = dime_write_open;
    soap.fdimewriteclose = dime_write_close;
    soap.fdimewrite = dime_write;

    // Call soap plate function.
    // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    // Specify the camera on which search the plate ( here 3 )
    // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cam = _tstoi(argv[1]);

    camerasCntx.__size = 0; // No contect cameras for this example
    soap_set_namespaces(&soap, dvs_namespaces);
    soap.user = "getDimePlateArray";
    soap_call_ns1__getDimePlateArray(&soap, server, "",
                                     cam,
                                     &camerasCntx,
                                     &dimeDataArray);
    if (soap.error) {
        // If error is:
        //   1 -> no plate is identified
        //   n -> generic error
        // 
        // soap_print_fault print more details on error.
        // In case of 'no plate identified', it returns plate 'XXXXXXX'.

        printf("Error calling 'getDimePlateArray': %d (N:%d)\n",
               soap.error, dimeDataArray.__size);
        soap_print_fault(&soap, stdout);
        return -1;
    }

    // On success, print how many images ( always one in this case ).
    printf("Received %d images\n", dimeDataArray.__size);

    // Close gSOAP.
    soap_destroy(&soap);
    soap_end(&soap);
    soap_free(&soap);
    soap_done(&soap);

	return 0;
}

static void *
dime_write_open(struct soap *soap, const char *id,
                const char *type, const char *options)
{
    FILE *handle = NULL;
    char plate[32];
    char filename[256];

    // The plate name is written in the 'options' of the
    // DIME gSOAP struct according to the manual gSOAP chapter:
    //
    //   15.3 Serializing Binary Data in DIME
    //
    //   char *soap_dime_option(struct soap *soap, 
    //                          unsigned short type,
    //                          const char *option)
    //
    // Here, how to retrieve this information.
    //
    memset(plate, 0, sizeof(plate));
    memset(filename, 0, sizeof(filename));
    if (options)
    { 
        size_t len = ((unsigned char)options[2] << 8) | 
                     ((unsigned char)options[3]);

        strncpy(plate, options + 4, len);
        plate[len] = '\0';
    }
    sprintf(filename, "plate-%s-%d.jpg", plate, time(NULL));

    handle = fopen(filename, "wb");
    return (void *)handle;
}

static void
dime_write_close(struct soap *soap, void *handle)
{
    fclose((FILE *)handle);
}

#define HEADER_LEN      20
static int
dime_write(struct soap *soap, void *handle, const char *buf, size_t len)
{
    // The jpg image plate starts after 20 bytes offset.
    //
    fwrite(buf + HEADER_LEN, 1, len - HEADER_LEN, (FILE *)handle);
    return SOAP_OK;
}

