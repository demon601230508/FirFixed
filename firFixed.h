#ifndef FIRFIXED_H
#define FIRFIXED_H
#include <sys/types.h>
#include <stdlib.h>
#include <string.h>
typedef struct fir_fixed{
    unsigned short length;
    unsigned short filterLength;
    int16_t *coeffs;
    int16_t *insamp;
}fir_fixed_t;

void firFixedInit(fir_fixed_t *fir,int inputLen,int filterLen,int16_t *coeffs);

void firFixedRelease(fir_fixed_t *fir);

void applyFirFixed(fir_fixed_t *fir, int16_t *input, int16_t *output);
#endif
