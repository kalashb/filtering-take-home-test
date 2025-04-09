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

## External Tools Used
1. **IIR Filter Design**: I didn't know what a two-pole Butterworth IIR filter was - hence used [MathWorks IIR Filter Design Guide](https://www.mathworks.com/help/signal/ug/iir-filter-design.html). I was really considering processing everything in MATLAB as opposed to C because MATLAB has very specific functionality already documented and could be used - but I didn't find it more useful than modeling. C is more useful to apply in real systems and MATLAB would be good if I had to model it. I might still consider writing a short script to make an IIR filter in MATLAB.

2. **C syntax and time library**: I also used C syntax pages (for printing, converstions) online and figured out how to use libraries to make my work easier

3. **AI Usage**: I used AI to speed up my coding process significantly (ended up rewriting a lot lol) - mostly, AI helped me write comments, print statements, add visualization in python. I learned how to make a Makefile properly and had some gitignore issues due to large database being accidentally pushed - used AI for these.

## What I can do more
1. Add testing, and add more visualization
2. Actually try feeding it real time somehow and try to draw a real time output to a VGA
3. Make code more modular - right now the "read_data" function and the "process" function are a bit redundant, although that provides some degree of control over what can be shown on the output, it could be turned into 2 functions with called in the other
4. Figure out what the output is actually supposed to look like honestly I'm confused here - I could try matlab in this case