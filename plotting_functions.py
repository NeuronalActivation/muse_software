from matplotlib import pyplot as plt

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

def plot_compare(channel, smoothed_channel):
    plt.figure()
    plt.plot(channel, label="Original")
    plt.plot(smoothed_channel, label="Smoothed")
    plt.legend()
    plt.show()

def plot(x, channel_1, channel_2, channel_3, channel_4):
    plt.plot(x, channel_1)
    plt.plot(x, channel_2)
    plt.plot(x, channel_3)
    plt.plot(x, channel_4)