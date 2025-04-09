import numpy as np
import matplotlib.pyplot as plt
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

def plot_data(input_file, output_file, num_channels=256, max_frames=1000, channels_to_plot=None):
    """Plot input and output data for comparison."""
    # Read data
    input_data = read_binary_data(input_file, num_channels)
    output_data = read_binary_data(output_file, num_channels)
    
    if input_data is None or output_data is None:
        return
    
    # Limit the number of frames to plot
    input_data = input_data[:max_frames]
    output_data = output_data[:max_frames]
    
    # If no specific channels are specified, plot a few representative ones
    if channels_to_plot is None:
        # Plot channels 0, 64, 128, 192 as examples
        channels_to_plot = [0, 64, 128, 192]
    
    # Create time axis (assuming 32kHz sampling rate)
    time = np.arange(input_data.shape[0]) / 32000.0  # in seconds
    
    # Create figure
    fig, axes = plt.subplots(len(channels_to_plot), 2, figsize=(15, 3*len(channels_to_plot)))
    fig.suptitle('Neural Data: Input vs. Filtered Output', fontsize=16)
    
    # If only one channel, make axes 2D
    if len(channels_to_plot) == 1:
        axes = axes.reshape(1, -1)
    
    # Plot each channel
    for i, channel in enumerate(channels_to_plot):
        # Input data
        axes[i, 0].plot(time, input_data[:, channel])
        axes[i, 0].set_title(f'Channel {channel} - Input')
        axes[i, 0].set_xlabel('Time (s)')
        axes[i, 0].set_ylabel('Amplitude')
        axes[i, 0].grid(True)
        
        # Output data
        axes[i, 1].plot(time, output_data[:, channel])
        axes[i, 1].set_title(f'Channel {channel} - Filtered')
        axes[i, 1].set_xlabel('Time (s)')
        axes[i, 1].set_ylabel('Amplitude')
        axes[i, 1].grid(True)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('neural_data_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Print some statistics
    print("\nData Statistics:")
    print("-" * 30)
    print(f"Input data shape: {input_data.shape}")
    print(f"Output data shape: {output_data.shape}")
    print(f"Input data range: [{input_data.min()}, {input_data.max()}]")
    print(f"Output data range: [{output_data.min()}, {output_data.max()}]")
    
    # Calculate and print RMS values with proper data type handling
    input_data_float = input_data.astype(np.float64)  # Convert to float64 to avoid overflow
    output_data_float = output_data.astype(np.float64)
    
    input_rms = np.sqrt(np.mean(input_data_float**2))
    output_rms = np.sqrt(np.mean(output_data_float**2))
    
    print(f"\nRMS Values:")
    print("-" * 30)
    print(f"Input RMS: {input_rms:.2f}")
    print(f"Output RMS: {output_rms:.2f}")
    print(f"RMS ratio (output/input): {output_rms/input_rms:.4f}")
    
    # Calculate additional statistics
    input_mean = np.mean(input_data_float)
    output_mean = np.mean(output_data_float)
    input_std = np.std(input_data_float)
    output_std = np.std(output_data_float)
    
    print(f"\nAdditional Statistics:")
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
    plot_data(input_file, output_file)
    print("Plot saved as 'neural_data_comparison.png'")