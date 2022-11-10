#include "firFixed.h"
 
// FIR init
void firFixedInit(fir_fixed_t *fir,int inputLen,int filterLen,int16_t *coeffs)
{
    int insampSize = (filterLen - 1 + inputLen)*sizeof(int16_t);
    fir->length = inputLen;
    fir->filterLength = filterLen;
    fir->coeffs = coeffs;
    fir->insamp =(int16_t *)malloc(insampSize);
    memset( fir->insamp, 0, insampSize);
}

void firFixedRelease(fir_fixed_t *fir){
    free(fir->insamp);
}
// the FIR filter function
void applyFirFixed(fir_fixed_t *fir, int16_t *input, int16_t *output)
//void firFixed( int16_t *coeffs, int16_t *input, 
//       int length, int filterLength )
{
    int32_t acc;     // accumulator for MACs
    int16_t *coeffp; // pointer to coefficients
    int16_t *inputp; // pointer to input samples
    int n;
    int k;

    // put the new samples at the high end of the buffer
    memcpy( &fir->insamp[fir->filterLength - 1], input,
            fir->length * sizeof(int16_t) );
 
    // apply the filter to each input sample
    for ( n = 0; n < fir->length; n++ ) {
        // calculate output n
        coeffp = fir->coeffs;
        inputp = &fir->insamp[fir->filterLength - 1 + n];
        // load rounding constant
        acc = 1 << 14;
        // perform the multiply-accumulate
        for ( k = 0; k < fir->filterLength; k++ ) { 
            acc += (int32_t)(*coeffp++) * (int32_t)(*inputp--); 
        } 
        // saturate the result 
        if ( acc > 0x3fffffff ) {
            acc = 0x3fffffff;
        } else if ( acc < -0x40000000 ) { 
            acc = -0x40000000; 
        } 
        // convert from Q30 to Q15 
        output[n] = (int16_t)(acc >> 15);
    }
 
    // shift input samples back in time for next time
    memmove( &fir->insamp[0], &fir->insamp[fir->length],
            (fir->filterLength - 1) * sizeof(int16_t) );
 
}
 
/* 
int16_t coeffs_1500_2500_test[ MAX_FLT_LEN ] =
{
-42,    4,   63,  133,  207,  278,  338,  379,  394,  378,  328,  245,
  132,   -5, -157, -311, -456, -578, -667, -712, -707, -650, -543, -391,
 -205,    2,  216,  419,  597,  735,  822,  852,  822,  735,  597,  419,
  216,    2, -205, -391, -543, -650, -707, -712, -667, -578, -456, -311,
 -157,   -5,  132,  245,  328,  378,  394,  379,  338,  278,  207,  133,
   63,    4,  -42
};
//tb 250
void firFixed2ch(const void *buffer, uint16_t frames){
    int16_t Left[MAX_INPUT_LEN];
    int16_t * input16 = (int16_t *)buffer;
    for (int i = 0; i < frames; i++)
    {
        int16_t *l_p = input16;
        int16_t *r_p = input16+1;

        Left[i] = *l_p;
        input16 += 2;
    }

    firFixed(coeffs_1500_2500_test,Left,MAX_INPUT_LEN,MAX_FLT_LEN);

    input16 = (int16_t *)buffer;
    for (int i = 0; i < frames; i++)
    {
        int16_t *l_p = input16;
        int16_t *r_p = input16+1;

        *l_p = Left[i];
        input16 += 2;
    }
}
*/
