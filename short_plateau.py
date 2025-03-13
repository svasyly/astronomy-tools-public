# Simplified Bolometric Light Curve Plotter for Hiramatsu Short-Plateau LCs (Hiramatsu+21)

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# Set plot style
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

def plot_bolometric_curve(data_dir, file_index=None, file_name=None):
    """
    Simple function to plot bolometric light curves from files in a directory.
    
    Parameters:
    -----------
    data_dir : str
        Directory containing light curve data files
    file_index : int, optional
        Index of file to plot (if None and file_name is None, all files will be plotted)
    file_name : str, optional
        Name of specific file to plot (takes precedence over file_index)
    """
    # Find all data files in the directory
    file_patterns = ["*.txt", "*.dat", "*.csv", "*.lbol"]
    file_paths = []
    
    for pattern in file_patterns:
        files = glob.glob(os.path.join(data_dir, pattern))
        file_paths.extend(files)
    
    # Sort files alphabetically
    file_paths.sort()
    
    print(f"Found {len(file_paths)} files in directory {data_dir}")
    
    if not file_paths:
        print(f"No files found in directory: {data_dir}")
        return
    
    # Display list of files found
    for i, file_path in enumerate(file_paths):
        print(f"{i+1}. {os.path.basename(file_path)}")
    
    # Determine which files to plot
    files_to_plot = []
    
    if file_name is not None:
        # Plot specific file by name
        specific_path = os.path.join(data_dir, file_name)
        if os.path.exists(specific_path):
            files_to_plot = [specific_path]
        else:
            print(f"File {file_name} not found in {data_dir}")
            return
    elif file_index is not None:
        # Plot specific file by index
        if 0 <= file_index < len(file_paths):
            files_to_plot = [file_paths[file_index]]
        else:
            print(f"Invalid file index: {file_index}. Must be between 0 and {len(file_paths)-1}")
            return
    else:
        # Plot all files
        files_to_plot = file_paths
    
    # Process each file
    for file_path in files_to_plot:
        file_basename = os.path.basename(file_path)
        print(f"\nProcessing file: {file_basename}")
        
        try:
            # Read the file with whitespace delimiter
            df = pd.read_csv(file_path, delim_whitespace=True, skiprows=1,
                           names=["time", "L_ubvri", "L_bol", "XEUV<325", "IR>890"])
            
            # Sort by time
            df = df.sort_values('time')
            
         
            print("Data preview:")
            display(df.head())
            
            # Create plot
            plt.figure(figsize=(12, 8))
            
            # Convert logarithmic luminosity to linear scale (10^X)
            linear_lbol = 10**df['L_ubvri']

            plt.plot(df['time'], linear_lbol, 'r-', linewidth=2, label='L_bol')
            plt.yscale('log')
            
            # Calculate and display peak (find peak index from log values)
            peak_idx = df['L_ubvri'].idxmax()
            peak_time = df.loc[peak_idx, 'time']
            peak_lum = linear_lbol.loc[peak_idx] 
            
            plt.xlabel('Time', fontsize=14)
            plt.ylabel('Luminosity (erg s$^{-1}$)', fontsize=14)
            plt.title(f'Bolometric Light Curve - {file_basename}', fontsize=16)
            plt.grid(True, alpha=0.3)
            plt.legend(fontsize=12)
            plt.tight_layout()
            plt.show()
            
            print(f"Statistics for {file_basename}:")
            print(f"Peak time: {peak_time:.3f}")
            print(f"Peak luminosity: {df['L_ubvri'].max():.3f} (log erg/s)")
            print(f"Time range: {df['time'].min():.3f} to {df['time'].max():.3f}")
            
        except Exception as e:
            print(f"Error processing file {file_basename}: {e}")

# Example usage:
# 1. Plot all files in a directory:
plot_bolometric_curve('D:\\Short Plateau')

# 2. Plot a specific file by index (0 is the first file):
#plot_bolometric_curve('D:\\Short Plateau', file_index=886)

# 3. Plot a specific file by name:
# plot_bolometric_curve('D:\\Short Plateau', file_name='example.txt')
