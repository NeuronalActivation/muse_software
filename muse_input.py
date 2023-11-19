import pylsl
import numpy as np
import serial
import time
import matplotlib.pyplot as plt
import scipy as sp
from plotting_functions import plot_fourier, plot_compare, plot

def main():
    streams = pylsl.resolve_stream('name', 'PetalStream_eeg')
    inlet = pylsl.StreamInlet(streams[0])
    sample, timestamp_0 = inlet.pull_sample()
    ser = serial.Serial('COM5')
    time.sleep(2)

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


       # print("Before smoothing")
        #plot(x, channel_1, channel_2, channel_3, channel_4)

        #smooth the data
        smoothed_channel_1 = smooth_eeg(channel_1)
        smoothed_channel_2 = smooth_eeg(channel_2)
        smoothed_channel_3 = smooth_eeg(channel_3)
        smoothed_channel_4 = smooth_eeg(channel_4)
        #fourier transform  
        plotFreq_1, plotMag_1 = fourier(smoothed_channel_1)
        plotFreq_2, plotMag_2 = fourier(smoothed_channel_2)
        plotFreq_3, plotMag_3 = fourier(smoothed_channel_3)
        plotFreq_4, plotMag_4 = fourier(smoothed_channel_4)    

        # ratio = get_beta_alpha_ratio(plotFreq_1, plotMag_1, plotFreq_2, plotMag_2, plotFreq_3, plotMag_3, plotFreq_4, plotMag_4)
        # print("ratio", ratio)  

        ratio_1 = get_beta_alpha_ratio(plotFreq_1, plotMag_1)
        ratio_2 = get_beta_alpha_ratio(plotFreq_2, plotMag_2)
        ratio_3 = get_beta_alpha_ratio(plotFreq_3, plotMag_3)
        ratio_4 = get_beta_alpha_ratio(plotFreq_4, plotMag_4)

        ratio = (ratio_1 + ratio_2 + ratio_3 + ratio_4)/4
        print("ratio", ratio)

        if (ratio < 0.52):
            ser.write(b'blue\n')
        else:
            ser.write(b'red\n')
        
        time.sleep(1)
         
        
        # #plot fourier
        # plot_fourier(plotFreq_1, plotMag_1)
        # plot_fourier(plotFreq_2, plotMag_2)
        # plot_fourier(plotFreq_3, plotMag_3)
        # plot_fourier(plotFreq_4, plotMag_4)        
        # plt.show()

        # mean_1 = mean(plotFreq_1, plotMag_1)
        # mean_2 = mean(plotFreq_2, plotMag_2)
        # mean_3 = mean(plotFreq_3, plotMag_3)
        # mean_4 = mean(plotFreq_4, plotMag_4)

        # print("mean 1", mean_1)
        # print("mean 2", mean_2)
        # print("mean 3", mean_3)
        # print("mean 4", mean_4)
        # print("overall mean", (mean_1+mean_2+mean_3+mean_4)/4)
        # print(" ")

       

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

def smooth_eeg(channel):
    # Smooth the data using a savgol filter
    smooth_channel = sp.signal.savgol_filter(channel, 51, 3)
    return smooth_channel

def mean(plotFreq, plotMag):
    return np.sum(plotFreq*plotMag)/np.sum(plotMag)

def get_beta_alpha(plotFreq, plotMag):
    eight = find_nearest(plotFreq, 8)
    thirteen = find_nearest(plotFreq, 13)
    thirty_two = find_nearest(plotFreq, 32)

    alpha_lower = np.where(plotFreq == eight)[0][0]
    alpha_upper = np.where(plotFreq == thirteen)[0][0]
    beta_upper = np.where(plotFreq == thirty_two)[0][0]
    alphaMag = plotMag[alpha_lower:alpha_upper]
    betaMag = plotMag[alpha_upper:beta_upper]
    alphaFreq = plotFreq[alpha_lower:alpha_upper]
    betaFreq = plotFreq[alpha_upper:beta_upper]
    return betaMag, betaFreq, alphaMag, alphaFreq

def get_beta_alpha_ratio(plotFreq, plotMag):
    betaMag, betaFreq, alphaMag, alphaFreq = get_beta_alpha(plotFreq, plotMag)
    return mean(alphaFreq, alphaMag)/mean(betaFreq, betaMag)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

main()