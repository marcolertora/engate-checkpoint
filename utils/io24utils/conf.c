#include <stdio.h>
#include <stdio.h>
#include <stdint.h>
#include <sys/socket.h>

typedef struct _io24conf
{
    uint8_t reserved[8];
    uint8_t controlbits1, controlbits2;
    uint8_t fixedipaddr1, fixedipaddr2, fixedipaddr3, fixedipaddr4;
    
} __attribute__((__packed__)) io24conf;

int main(void)
{
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    
    return 0;
}
