# Project 1.3 - Groep A5 - Nagalmtijd Software v0.1
import time
import numpy as np
import scipy.ndimage
import sounddevice as sd
import matplotlib.pyplot as plt
import csv
from scipy.signal import argrelextrema
from scipy.interpolate import make_interp_spline


#  de 'main' class houdt alle basis structuur van de code, zoals variabelen en de 'main_loop'
class Main:
    def __init__(self):
        self.run_program = True
        # TODO: add variables


    # 'main_loop' is de hoofd-loop die het programma laat draaien
    def main_loop(self):
        # zolang 'self.run_program' True is, blijft 'main_loop' draaien
        while self.run_program == True:
            pass
        # TODO: code


    # gebruik voor veel testjes achter elkaar doen
    def test_loop(self):
        while self.run_program == True:
            mic = Microphone()
            mic.perform_test_recording()


    #  de 'recording_loop' is de loop die wordt re-runt voor elke enkele meting
    # return: dB np.array()
    def recording_loop(self):
        pass
        # TODO: - neem input
        # TODO: - doe opname
        # TODO: - verander in dB
        # TODO: - bereken nagalmtijd
        # TODO: - sla data op in .csv
        return dB_recording


# de 'microphone' class houdt alle functies die er voor nodig zijn om een opname met de microfoon te doen
class Microphone:
    def __init__(self):
        self.frames = 44100             # (Hz): frequentie van opnamen (standaard waarde)
        sd.default.channels = 1    # hoeveel kanelen beschikbaar voor opname (laat 1)
        sd.default.device = 'Microphone (USB Audio Device)'    # selecteren de juiste microfoon
        self.test_recording_duration = 5   # hoeveel seconde lang is de test_recording
        self.pre_recording_sleep_time = 0.5 # hoelang wachten tot recording start
        self.data_management = Data_management()
        print(sd.query_devices())


    # doet een (rauwe) opnamen van geluid voor een bepaald aantal aangegeven secondes ('duration')
    # return: np.array()
    def record_raw(self, duration, frames):
        raw_recording = sd.rec(int(frames * duration), samplerate=frames)
        sd.wait()
        return raw_recording


    def perform_test_recording(self):
        print('-'*60)
        print('Started recording test')
        click = input(f'[ENTER]: START RECORDIING ({self.test_recording_duration}s)')
        print(f'Recording starts in {self.pre_recording_sleep_time}s')
        time.sleep(self.pre_recording_sleep_time)
        print('Recording...')
        # try:
        raw_recording = self.record_raw(self.test_recording_duration, self.frames)
        # except Exception as e:
        #     print('ERROR DURING RECORDING:')
        #     print(e)
        # try:
        dB_recording = self.data_management.raw_recording_to_dB_recording(raw_recording)
        # except Exception as e:
        #     print('ERROR DURING DATA VERWERKING (dB_recording):')
        #     print(e)
        # try:
        plot = Plot()
        filtered_dB_recording = self.data_management.filter_dB(dB_recording)
        self.data_management.calculate_nagalmtijd(self.test_recording_duration, filtered_dB_recording)
        plot.plot_dB_and_filtered(self.test_recording_duration, dB_recording, filtered_dB_recording)
        # plot.plot_dB(self.test_recording_duration, dB_recording)
        # plot.plot_Int(self.test_recording_duration, raw_recording)
        # except Exception as e:
        #     print('ERROR DURING DATA VISUALISATION (plot.plot_dB):')
        #     print(e)
        print('End of recording test')
        print('-' * 60)


class Data_management:
    def __init__(self):
        self.file_naam = 'metingen_pathe_experiment.csv'
        self.data_opnames = []
        self.csf_titel = ['meting', 'stoel', 'tijd', 'nagalmtijd', 'x', 'y', 'z']
        self.nagalmtijd_diff_threschold_percentage = 15 # %

    def save_data(self, new_data):

        # het scrhijven van nieuw lines, oftwel nieuwe data overnemen in de csv file.
        self.data_opnames.insert(len(self.data_opnames), new_data)

        # het schrijven van de CSV file
        with open('metingen_pathe_experiment.csv', 'w', encoding='UTF8', newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(self.csf_titel)
            csvwriter.writerows(self.data_opnames)


    # veranderd de 'raw_recording' naar een gecorigeerde en gekalibreerde dB array
    # return np.array()
    def raw_recording_to_dB_recording(self, raw_recording):
        # verander intensiteit array in absolute waarde intensiteit array
        intensiteit_ongekalibreerd = np.absolute(raw_recording)

        # gekalibreerde correctie factor die experimenteel is bepaald
        correctiefactor_experimenteel = 0.99088

        # verander de ongecalibreerde intensiteit waardes naar gecalibreerde gecorigeerde dB waardes
        dB_recording = (np.log(
            (intensiteit_ongekalibreerd) / (1 * (10 ** -6))) / 0.1141) * 0.8
        return dB_recording


    # filtert de dB_recording data en zorgt voor een grafiek die de bovenkant van die data volgt
    # de functie zoekt naar alle 'lokale maxima' en trekt daar een grafiek door
    def filter_dB(self, dB_recording):
        corrected_dB_list = []
        for item in dB_recording:
            corrected_dB_list.append(float(item))
        corrected_dB = np.asarray(corrected_dB_list)
        print(corrected_dB)
        corrected_dB[corrected_dB < -1e308] = 0.00001
        print(corrected_dB)
        dB_recording_peaks = scipy.signal.find_peaks(corrected_dB, height=15, distance=800)
        print(dB_recording_peaks)
        filtered_dB_recording = corrected_dB[dB_recording_peaks[0]]
        return filtered_dB_recording


    def calculate_nagalmtijd(self, duration, filtered_dB_recording):
        x_filtered = np.linspace(0, duration, (len(np.absolute(filtered_dB_recording))))
        y_filtered = filtered_dB_recording
        frame_array = []
        mean = 0
        for i, filtered_frame in enumerate(y_filtered):
            time_frame = x_filtered[i]
            difference_percentage = 100 - (mean/filtered_frame)*100
            if difference_percentage < self.nagalmtijd_diff_threschold_percentage:
                frame_array.append(filtered_frame)
                mean = np.mean(np.asarray(frame_array))

            print(f'mean: {mean}, frame: {filtered_frame} --- difference: {difference_percentage}%')
            print(f'time: {time_frame}s')
        # print(filtered_dB_recording)


# de 'user_input' class houdt alle functies die er voor nodig zijn om een opname met de microfoon te doen
class User_interface:
    def __init__(self):
        pass


# de 'plot' class zorgt voor snel plotten waar dat nodig is
class Plot:
    def __init__(self):
        pass


    # plot dB niveau verkregen met dB_recording
    def plot_dB(self, duration, dB_recording):
        xpoints = np.linspace(0, duration, len(np.absolute(dB_recording)))
        ypoints = dB_recording

        plt.plot(xpoints, ypoints, label='Decibel over tijd')
        plt.title('dB over tijd')
        plt.ylabel('Geluidsniveau [dB]')
        plt.xlabel('Tijd [s]')
        plt.show()


    def plot_dB_and_filtered(self, duration, dB_recording, filtered_dB_recording):
        x_dB = np.linspace(0, duration, len(np.absolute(dB_recording)))
        y_dB = dB_recording
        x_filtered = np.linspace(0, duration, (len(np.absolute(filtered_dB_recording))))
        y_filtered = filtered_dB_recording

        plt.plot(x_dB, y_dB, label='Decibel over tijd')
        plt.plot(x_filtered, y_filtered, label='Gefilterde dB over tijd')
        plt.title('dB over tijd')
        plt.ylabel('Geluidsniveau [dB] - lokale extrema')
        plt.xlabel('Tijd [s]')
        plt.show()


    # plot de intensiteit gemeten vanaf de microfoon
    def plot_Int(self, duration, raw_recording):
        xpoints = np.linspace(0, duration, len(np.absolute(raw_recording)))
        ypoints = np.absolute(raw_recording)

        plt.plot(xpoints, ypoints, label='I (0 tot 1)')
        plt.title('Intensiteit over tijd')
        plt.ylabel('Intensiteit [W/m2] (0 tot 1)')
        plt.xlabel('Tijd [s]')
        plt.show()


main = Main()
main.test_loop()

# mic = Microphone()
# mic.perform_test_recording()

