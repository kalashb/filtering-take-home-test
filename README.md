# Filtering Take-Home Test

## Overview
Data filtering in C (IIR filter application)

## Processing Steps
1. **Read Data**: Basic `fopen` and `fread` implemented, with robust error handling for edge cases
2. **Apply IIR Filter**: Implemented with the given coefficients
3. **Store Results**: Save filtered data to file and display output

## Performance Results
The last time I ran it, this was my output/result:

```
Using default filenames:
  Input: ../data/neural_data_256ch_16b.dat
  Output: ../data/filtered_neural_data.dat

Final timing statistics:
Total time: 498871.00 us
Average time per frame: 1.95 us
Average time per sample: 0.0076 us
Processing complete. Filtered data saved to ../data/filtered_neural_data.dat
```

## Usage:

1. input file name and output file name: to use different files, run: ./neural_reader input.dat output.dat
2. display the raw data: ./neural_reader -d
3. display the filtered data: ./neural_reader -f
4. might have to make a "data" folder before running as the file path is specified if you run default

## Files:

1. Main file main.c - main function handling, a link between makefile, command file, and my actual code
2. process.c - read and filter

## Visualization Files

1. `filter_response.py`: Shows the filter's frequency response (magnitude, phase, group delay) to understand its behavior across different frequencies.

2. `filter_performance.py`: Analyzes filter effects on neural data with time-domain plots and frequency analysis.

3. `neural_data_comperison.py`: Side-by-side comparison of raw and filtered neural data across multiple channels.

## External Tools Used
1. **IIR Filter Design**: I didn't know what a two-pole Butterworth IIR filter was - hence used [MathWorks IIR Filter Design Guide](https://www.mathworks.com/help/signal/ug/iir-filter-design.html). I was really considering processing everything in MATLAB as opposed to C because MATLAB has very specific functionality already documented and could be used - but I didn't find it more useful than modeling. C is more useful to apply in real systems and MATLAB would be good if I had to model it. I might still consider writing a short script to make an IIR filter in MATLAB.

2. **C syntax and time library**: I also used C syntax pages (for printing, converstions) online and figured out how to use libraries to make my work easier

3. **AI Usage**: I used AI to speed up my coding process significantly (ended up rewriting a lot lol) - mostly, AI helped me write comments, print statements, add visualization in python. I learned how to make a Makefile properly and had some gitignore issues due to large database being accidentally pushed - used AI for these.

## What I can do more
1. Add testing, and add more visualization
2. Actually try feeding it real time somehow and try to draw a real time output to a VGA
3. Make code more modular - right now the "read_data" function and the "process" function are a bit redundant, although that provides some degree of control over what can be shown on the output, it could be turned into 2 functions with called in the other
4. Figure out what the output is actually supposed to look like honestly I'm confused here - I could try matlab in this case
5. Multithreading!!!

## Compilation and Setup
1. **Requirements**:
   - GCC compiler
   - Make
   - Python 3.x with numpy, matplotlib, scipy (for visualization)

2. **Compilation**:
   ```bash
   make
   ```
   This creates the executable `neural_reader`

## How to Run
1. **Basic Usage**:
   ```bash
   ./neural_reader [input_file] [output_file]
   ```
   If no files specified, uses defaults:
   - Input: `data/neural_data_256ch_16b.dat`
   - Output: `data/filtered_neural_data.dat`

2. **Display Options**:
   ```bash
   ./neural_reader -d  # Display raw data
   ./neural_reader -f  # Display filtered data
   ```

## Filter Implementation
The filter is a second-order IIR (Infinite Impulse Response) filter with coefficients:
```c
b = [0.99901921, -1.99790074, 0.99901921]
a = [1.0, -1.99790074, 0.99803843]
```

### How the Filter Works
1. **Sample-by-Sample Processing**:
   - Each sample is processed independently in real-time
   - No need to wait for future samples
   - Maintains only 2 previous input and output samples in memory

2. **Filter Equation**:
   ```
   y[n] = b0*x[n] + b1*x[n-1] + b2*x[n-2] - a1*y[n-1] - a2*y[n-2]
   ```
   where:
   - x[n] is current input
   - y[n] is current output
   - x[n-1], x[n-2] are previous inputs
   - y[n-1], y[n-2] are previous outputs

3. **Implementation Details**:
   - Direct Form II implementation for better numerical stability
   - Processes each channel independently
   - 32kHz sampling rate
   - Fixed-point arithmetic for efficiency

## Performance Profile
- **Memory Usage**: 
  - Static: ~1KB for filter coefficients and state
  - Dynamic: ~1MB for 256 channels × 2 samples of state
- **Compute Time**: 
  - Average: 0.0076 μs per sample
  - Per frame (256 channels): 1.95 μs
- **Total Processing**: ~499ms for full dataset

## Assumptions and Limitations
1. given filter data would work very well in my application
2. data is properly aligned and i didn't need to process it much
3. data is little endian
4. timing measuremenets are representative of real world performance
5. performance would be similar/consistent across different hardware 

2. **Limitations**:
   - File I/O for testing (core filter logic is real-time capable)
   - Fixed filter coefficients (no adaptive filtering)
   - No error handling for data overflow
   - Limited to 16-bit integer precision
   - No validation of 1ms delay requirement across different hardware

3. **Requirements Status**:
   - Filter delay: ~0.0076 μs per sample (well within 1ms requirement)
   - Data format: Maintains same 16-bit format for input/output
   - Real-time processing: Sample-by-sample processing with minimal delay