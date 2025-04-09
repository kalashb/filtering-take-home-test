#include <stdio.h>
#include <stdlib.h>
#include "process.h"

// 1. input file name and output file name: to use different files, run: ./neural_reader input.dat output.dat
// 2. display the raw data: ./neural_reader -d
// 3. find processed data in output file
// 4. display the filtered data: ./neural_reader -f
int main(int argc, char *argv[]) {
    const char* input_file = "../data/neural_data_256ch_16b.dat";
    const char* output_file = "../data/filtered_neural_data.dat";
    int result;
    
    // choose file names (addressing 1)
    if (argc >= 3) {
        input_file = argv[1];
        output_file = argv[2];
    } else {
        printf("Using default filenames:\n");
        printf("  Input: %s\n", input_file);
        printf("  Output: %s\n", output_file);
    }
    
    // display the raw data (addressing 2)
    if (argv[1] == "-d") {
        result = read_data(NULL);  // NULL means only display, don't save
        if (result != 0) {
            fprintf(stderr, "Error reading data\n");
            return 1;
        }
    }

    // process the data with IIR filter and store it in output file
    result = process_neural_data(input_file, output_file);
    if (result != 0) {
        fprintf(stderr, "Error processing data\n");
        return 1;
    }

    // display the filtered data (addressing 4)
    if (argv[1] == "-f") {
        result = read_data(output_file);
        if (result != 0) {
            fprintf(stderr, "Error reading data\n");
            return 1;
        }
    }
    printf("Processing complete. Filtered data saved to %s\n", output_file);
    return 0;
}
