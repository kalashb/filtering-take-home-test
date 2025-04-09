#ifndef PROCESS_H
#define PROCESS_H

#include <stdint.h>

#define NUM_CHANNELS 256

typedef struct {
    float x[3];
    float y[3];
} IIRFilter;

// Function to read neural data and optionally save to a file
// If output_filename is NULL, it only displays to console
// Returns 0 on success, 1 on error
int read_data(const char* output_filename);

// Function to apply IIR filter to a single sample
void apply_filter(IIRFilter *f, float in, float *out);

// Function to process neural data file with IIR filter
// Returns 0 on success, 1 on error
int process_neural_data(const char* input_file, const char* output_file);

#endif // PROCESS_H 
