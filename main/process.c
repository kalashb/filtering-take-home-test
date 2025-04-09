#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include "process.h"

#define NUM_CHANNELS 256
#define SAMPLES_TO_DISPLAY 10
#define EXPECTED_FRAME_TIME_US 1000

void apply_filter(IIRFilter *f, float in, float *out) {
    float b0 = 0.99901921f, b1 = -1.99790074f, b2 = 0.99901921f;
    float a1 = -1.99790074f, a2 = 0.99803843f;

    float y = b0 * in + b1 * f->x[1] + b2 * f->x[2]
                    - a1 * f->y[1] - a2 * f->y[2];

    // shift x and y
    f->x[2] = f->x[1];
    f->x[1] = in;

    f->y[2] = f->y[1];
    f->y[1] = y;

    *out = y;
}

int read_data(const char* output_filename) {
    FILE *fp_in, *fp_out = NULL;
    int16_t *buffer;
    size_t bytes_read;
    int i;

    // Open input file in binary read mode
    fp_in = fopen("neural_data_256ch_16b.dat", "rb");
    if (fp_in == NULL) {
        perror("Error opening input file");
        return 1;
    }

    // If output filename is provided, open output file
    if (output_filename != NULL) {
        fp_out = fopen(output_filename, "w");
        if (fp_out == NULL) {
            perror("Error opening output file");
            fclose(fp_in);
            return 1;
        }
    }

    // Allocate memory for one sample set (256 channels)
    buffer = (int16_t *)malloc(NUM_CHANNELS * sizeof(int16_t));
    if (buffer == NULL) {
        perror("Error allocating memory");
        fclose(fp_in);
        if (fp_out) fclose(fp_out);
        return 1;
    }

    // Print/write header
    const char* header = "Neural Data (256 channels, 16-bit samples)\n";
    printf("%s", header);
    if (fp_out) fprintf(fp_out, "%s", header);

    // Read and display/write samples
    for (i = 0; i < SAMPLES_TO_DISPLAY; i++) {
        bytes_read = fread(buffer, sizeof(int16_t), NUM_CHANNELS, fp_in);
        if (bytes_read != NUM_CHANNELS) {
            const char* error_msg = "Error reading data or reached end of file\n";
            printf("%s", error_msg);
            if (fp_out) fprintf(fp_out, "%s", error_msg);
            break;
        }

        // Print/write sample header
        printf("Sample %d:\n", i + 1);
        if (fp_out) fprintf(fp_out, "Sample %d:\n", i + 1);

        if (fp_out) fprintf(fp_out, "\n");
    }

    // Clean up
    free(buffer);
    fclose(fp_in);
    if (fp_out) {
        fclose(fp_out);
        printf("Data has been saved to %s\n", output_filename);
    }

    return 0;
}

int process_neural_data(const char* input_file, const char* output_file) {
    FILE *infile = fopen(input_file, "rb");
    FILE *outfile = fopen(output_file, "wb");

    if (!infile || !outfile) {
        perror("File error");
        return 1;
    }

    IIRFilter filters[NUM_CHANNELS] = {0};

    int16_t raw[NUM_CHANNELS];
    float f_in[NUM_CHANNELS];
    float f_out[NUM_CHANNELS];
    int16_t result[NUM_CHANNELS];

    struct timespec start, end;
    double total_time = 0.0;
    size_t frames = 0;

    while (fread(raw, sizeof(int16_t), NUM_CHANNELS, infile) == NUM_CHANNELS) {
        clock_gettime(CLOCK_MONOTONIC, &start);

        // Convert to float
        for (int i = 0; i < NUM_CHANNELS; i++)
            f_in[i] = (float)raw[i];

        // Filter
        for (int i = 0; i < NUM_CHANNELS; i++){
            apply_filter(&filters[i], f_in[i], &f_out[i]);
            double duration = (end.tv_sec - start.tv_sec) * 1e6 + (end.tv_nsec - start.tv_nsec) / 1e3;
            printf("Frame %zu took %.2f us\n", frames, duration);
            if (duration > EXPECTED_FRAME_TIME_US) {
                printf("Warning: Frame %zu took %.2f us, exceeding real-time limit!\n", frames, duration);
            }
        }

        // Convert back to int16_t
        for (int i = 0; i < NUM_CHANNELS; i++) {
            if (f_out[i] > 32767.0f) f_out[i] = 32767.0f;
            if (f_out[i] < -32768.0f) f_out[i] = -32768.0f;
            result[i] = (int16_t)f_out[i];
        }

        fwrite(result, sizeof(int16_t), NUM_CHANNELS, outfile);

        clock_gettime(CLOCK_MONOTONIC, &end);
        double duration = (end.tv_sec - start.tv_sec) * 1e6 +
                          (end.tv_nsec - start.tv_nsec) / 1e3;
        total_time += duration;
        frames++;
    }

    printf("Average time per frame: %.2f us\n", total_time / frames);
    printf("Average time per sample: %.4f us\n", total_time / (frames * NUM_CHANNELS));

    fclose(infile);
    fclose(outfile);
    return 0;
} 
