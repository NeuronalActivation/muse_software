import pylsl
import numpy as np
import time
import matplotlib.pyplot as plt
import scipy as sp


def main():
    streams = pylsl.resolve_stream('name', 'PetalStream_eeg')
    inlet = pylsl.StreamInlet(streams[0])
    sample, timestamp_0 = inlet.pull_sample()

    #loop than runs for a second
    while True:
        end_time = time.time() + 1
        channel_1, channel_2, channel_3, channel_4 = [], [], [], []
        x = []
        while time.time() < end_time:
            sample, timestamp = inlet.pull_sample()
            channel_1.append(sample[0])
            channel_2.append(sample[1])
            channel_3.append(sample[2])
            channel_4.append(sample[3])
            x.append(timestamp)


        print("Before smoothing")
        #plot(x, channel_1, channel_2, channel_3, channel_4)

        #smooth the data
        smoothed_channel_1 = smooth_eeg(channel_1)
        smoothed_channel_2 = smooth_eeg(channel_2)
        smoothed_channel_3 = smooth_eeg(channel_3)
        smoothed_channel_4 = smooth_eeg(channel_4)

        #plot the smoothed data
        # plot_compare(channel_1,smoothed_channel_1)
        # plot_compare(channel_2,smoothed_channel_2)
        # plot_compare(channel_3,smoothed_channel_3)
        # plot_compare(channel_4,smoothed_channel_4)
        print("After smoothing")
        #plot(x, smoothed_channel_1, smoothed_channel_2, smoothed_channel_3, smoothed_channel_4)

        #fourier transform  
        plotFreq_1, plotMag_1 = fourier(channel_1)
        plotFreq_2, plotMag_2 = fourier(channel_2)
        plotFreq_3, plotMag_3 = fourier(channel_3)
        plotFreq_4, plotMag_4 = fourier(channel_4)

    

        #plot(x, channel_1, channel_2, channel_3, channel_4, channel_5)
    

        print(len(plotFreq_1))
        print(len(plotMag_1))
        #get mean of all frequencies
       

        #get mean of all samples
        # mean_1 = np.mean(channel_1)
        # mean_2 = np.mean(channel_2)
        # mean_3 = np.mean(channel_3)
        # mean_4 = np.mean(channel_4)
        # mean_5 = np.mean(channel_5)
        
        # #plot fourier
        plot_fourier(plotFreq_1, plotMag_1)
        plot_fourier(plotFreq_2, plotMag_2)
        plot_fourier(plotFreq_3, plotMag_3)
        plot_fourier(plotFreq_4, plotMag_4)        
        plt.show()

        mean_1 = mean(plotFreq_1, plotMag_1)
        mean_2 = mean(plotFreq_2, plotMag_2)
        mean_3 = mean(plotFreq_3, plotMag_3)
        mean_4 = mean(plotFreq_4, plotMag_4)

        print("mean 1", mean_1)
        print("mean 2", mean_2)
        print("mean 3", mean_3)
        print("mean 4", mean_4)
        print("overall mean", (mean_1+mean_2+mean_3+mean_4)/4)
        print(" ")

       

def fourier(channel):
    # Fourier transform
    fftData = np.fft.fft(channel)
    freq = np.fft.fftfreq(len(channel)) * 256

    # Now we just plot the transformed data (the exact same wave but in the frequency domain)
    plotFreq    = freq[1:int(len(freq)/2)]                  # Remove negative reflection
    plotFftData = fftData[1:int(len(fftData)/2)]            # Remove negative reflection
    plotMag     = plotFftData.real**2 + plotFftData.imag**2 # FFT is a complex function, so we need to cast to the real domain

    nearest_num = find_nearest(plotFreq, 60)
    index = np.where(plotFreq == nearest_num)[0][0]
    plotMag = plotMag[0:index]
    plotFreq = plotFreq[0:index]

    return plotFreq, plotMag

def plot(x, channel_1, channel_2, channel_3, channel_4):
    plt.plot(x, channel_1)
    plt.plot(x, channel_2)
    plt.plot(x, channel_3)
    plt.plot(x, channel_4)

def smooth_eeg(channel):
    # Smooth the data using a savgol filter
    smooth_channel = sp.signal.savgol_filter(channel, 51, 3)
    return smooth_channel

def plot_compare(channel, smoothed_channel):
    plt.figure()
    plt.plot(channel, label="Original")
    plt.plot(smoothed_channel, label="Smoothed")
    plt.legend()
    plt.show()

def plot_fourier(plotFreq, plotMag):
    isShowingBinLines = True

# Create the plot

    # Add the special spacing
    if(isShowingBinLines):
        subsets=[0, 4, 7.5, 12.5, 30]
        plt.xticks(subsets)

    # Add the vertical lines
    if(isShowingBinLines):
        plt.axvline(x=4, color="darkgrey")
        plt.axvline(x=7.5, color="darkgrey")
        plt.axvline(x=12.5, color="darkgrey")
        plt.axvline(x=30, color="darkgrey")

    # Plot
    plt.margins(x=0)
    plt.plot(plotFreq, plotMag)

def mean(plotFreq, plotMag):
    return np.sum(plotFreq*plotMag)/np.sum(plotMag)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

main()