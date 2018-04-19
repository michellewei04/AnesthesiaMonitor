import numpy as np
from scipy import signal


class EMGPeakDetection:

    def __init__(self, filename='scope_8.csv'):
        self.emg_raw_data = np.genfromtxt(filename, delimiter=',', skip_header=2)
        self.voltage = []
        self.tof_ratio = None

    def emg_peak_detection(self):
        """ Returns an array of voltages where peak was detected
        :param filename: the .csv file that contains the raw EMG data
        :rtype: 1-d array
        """

        temp_emg_data = self.emg_raw_data
        # if there is a missing time, average it from the surrounding points
        for x in range(1, len(temp_emg_data[:, 0])):
            if temp_emg_data[x, 0] == 0.0:
                temp_emg_data[x, 0] = (temp_emg_data[x + 1, 0] +
                                       temp_emg_data[x - 1, 0]) / 2

        self.emg_raw_data = temp_emg_data

        print(self.emg_raw_data[:, 1])

        peakind = signal.find_peaks_cwt(self.emg_raw_data[:, 1],
                                        np.arange(1, 250))

        largest_peak_value = max(self.emg_raw_data[:, 1])

        print(peakind)

        final_peakind = []
        print(peakind[1])
        for peaks in peakind:
            if self.emg_raw_data[peaks,1] > (.1*largest_peak_value):
                final_peakind.append(self.emg_raw_data[peaks, 1])
        print(final_peakind)

        self.voltage = final_peakind

        print(self.voltage)

        self.tof_ratio = 100 * (self.voltage[-1]/self.voltage[0])
        print(self.tof_ratio)


def main():
    current_emg = EMGPeakDetection()
    current_emg.emg_peak_detection()


if __name__ == "__main__":
    main()
