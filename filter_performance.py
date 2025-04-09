import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

def read_binary_data(filename, num_channels=256, dtype=np.int16):
    """Read binary data from file and return as numpy array."""
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        return None
    
    try:
        with open(filename, 'rb') as f:
            data = np.fromfile(f, dtype=dtype)
            # Reshape data into frames of num_channels
            num_frames = len(data) // num_channels
            data = data[:num_frames * num_channels].reshape(num_frames, num_channels)
            return data
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None

def plot_data_analysis(input_file, output_file, num_channels=256, sample_rate=32000):
    """Plot detailed analysis of input and output data."""
    # Read data
    input_data = read_binary_data(input_file, num_channels)
    output_data = read_binary_data(output_file, num_channels)
    
    if input_data is None or output_data is None:
        return
    
    # Create time axis
    time = np.arange(input_data.shape[0]) / sample_rate  # in seconds
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 12))
    
    # 1. Time domain plot - Full view of channel 0
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(time, input_data[:, 0], 'b-', label='Input', alpha=0.7)
    ax1.plot(time, output_data[:, 0], 'r-', label='Filtered', alpha=0.7)
    ax1.set_title('Full Signal View - Channel 0')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True)
    ax1.legend()
    
    # 2. Zoomed view of a small section (first 100 samples)
    ax2 = plt.subplot(3, 1, 2)
    zoom_samples = 100
    ax2.plot(time[:zoom_samples], input_data[:zoom_samples, 0], 'b-', label='Input', linewidth=2)
    ax2.plot(time[:zoom_samples], output_data[:zoom_samples, 0], 'r-', label='Filtered', linewidth=2)
    ax2.set_title('Zoomed View - First 100 Samples')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Amplitude')
    ax2.grid(True)
    ax2.legend()
    
    # 3. Frequency domain analysis
    ax3 = plt.subplot(3, 1, 3)
    # Compute FFT for both signals
    freqs_input = np.abs(np.fft.rfft(input_data[:, 0]))
    freqs_output = np.abs(np.fft.rfft(output_data[:, 0]))
    freq_axis = np.fft.rfftfreq(len(input_data[:, 0])) * sample_rate
    
    ax3.semilogy(freq_axis, freqs_input, 'b-', label='Input', alpha=0.7)
    ax3.semilogy(freq_axis, freqs_output, 'r-', label='Filtered', alpha=0.7)
    ax3.set_title('Frequency Response')
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Magnitude (log scale)')
    ax3.grid(True)
    ax3.legend()
    ax3.set_xlim(0, sample_rate/2)
    
    plt.tight_layout()
    plt.savefig('filter_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Print statistics
    print("\nSignal Statistics:")
    print("-" * 30)
    print(f"Input data shape: {input_data.shape}")
    print(f"Output data shape: {output_data.shape}")
    print(f"Input data range: [{input_data.min()}, {input_data.max()}]")
    print(f"Output data range: [{output_data.min()}, {output_data.max()}]")
    
    # Calculate RMS values with proper handling of data types
    input_data_float = input_data.astype(np.float64)  # Convert to float64 to avoid overflow
    output_data_float = output_data.astype(np.float64)
    
    input_rms = np.sqrt(np.mean(input_data_float**2))
    output_rms = np.sqrt(np.mean(output_data_float**2))
    
    print(f"\nRMS Values:")
    print("-" * 30)
    print(f"Input RMS: {input_rms:.2f}")
    print(f"Output RMS: {output_rms:.2f}")
    print(f"RMS ratio (output/input): {output_rms/input_rms:.4f}")
    
    # Calculate signal changes
    attenuation_db = 20 * np.log10(output_rms/input_rms)
    print(f"\nSignal Analysis:")
    print("-" * 30)
    print(f"Signal level change: {attenuation_db:.2f} dB")
    
    # Calculate mean and standard deviation
    input_mean = np.mean(input_data_float)
    output_mean = np.mean(output_data_float)
    input_std = np.std(input_data_float)
    output_std = np.std(output_data_float)
    
    print(f"\nMean and Standard Deviation:")
    print("-" * 30)
    print(f"Input mean: {input_mean:.2f}, std: {input_std:.2f}")
    print(f"Output mean: {output_mean:.2f}, std: {output_std:.2f}")
    print(f"Mean change: {output_mean - input_mean:.2f}")
    print(f"Std change: {((output_std - input_std)/input_std)*100:.2f}%")

if __name__ == "__main__":
    # Default file paths
    input_file = "data/neural_data_256ch_16b.dat"
    output_file = "data/filtered_neural_data.dat"
    
    # Check if files exist, if not try alternative paths
    if not os.path.exists(input_file):
        input_file = "../data/neural_data_256ch_16b.dat"
    if not os.path.exists(output_file):
        output_file = "../data/filtered_neural_data.dat"
    
    # Plot data
    plot_data_analysis(input_file, output_file)
    print("\nAnalysis plots saved as 'filter_performance.png'") 