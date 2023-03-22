# Project 1.3 - Groep A5 - Nagalmtijd Software v0.1
import time
import numpy as np
import scipy.ndimage
import sounddevice as sd
import matplotlib.pyplot as plt
import csv
from scipy.optimize import curve_fit


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
        self.pre_recording_sleep_time = 1 # hoelang wachten tot recording start
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

        raw_recording = self.record_raw(self.test_recording_duration, self.frames)

        dB_recording = self.data_management.raw_recording_to_dB_recording(raw_recording)

        plot = Plot()
        filtered_dB_recording = self.data_management.filter_dB(dB_recording)
        mean_array, peak_array, data_message_string = self.data_management.calculate_nagalmtijd(self.test_recording_duration, filtered_dB_recording, raw_recording)
        plot.plot_dB_and_filtered(self.test_recording_duration, dB_recording, filtered_dB_recording, mean_array, peak_array, data_message_string)
        plot.plot_Int(self.test_recording_duration, raw_recording)

        print('End of recording test')
        print('-' * 60)


class Data_management:
    def __init__(self):
        self.file_naam = 'metingen_pathe_experiment.csv'
        self.data_opnames = []
        self.csf_titel = ['meting', 'stoel', 'tijd', 'nagalmtijd', 'x', 'y', 'z']
        self.nagalmtijd_diff_threschold_percentage = 5 # %

    # slaat de data van elke meting op in een csv file
    def save_data(self, new_data):

        # het scrhijven van nieuw lines, oftwel nieuwe data overnemen in de csv file.
        self.data_opnames.insert(len(self.data_opnames), new_data)

        # het schrijven van de CSV file
        with open('metingen_pathe_experiment.csv', 'w', encoding='UTF8', newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(self.csf_titel)
            csvwriter.writerows(self.data_opnames)


    # veranderd de 'raw_recording' naar een gecorigeerde en gekalibreerde dB array
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
        dB_recording_peaks = scipy.signal.find_peaks(corrected_dB, height=30, distance=800)
        print(dB_recording_peaks)
        filtered_dB_recording = corrected_dB[dB_recording_peaks[0]]
        return filtered_dB_recording



    def nagalmtijd_function(self, nagalm_array, tijd_array):
        # functie variabelen
        tRT20 = 0
        tRT30 = 0

        def func(x, a, b):
            return a * x + b

        x = tijd_array
        y = nagalm_array

        # bereken y (dB) waardes
        max_dB = np.max(y)
        rt20_dB = max_dB - 20
        rt30_dB = max_dB - 30

        # maak een linear fit van x en y
        popt = curve_fit(func, x, y)

        # a en b uit formule halen
        a = popt[0][0]
        b = popt[1][0]

        # algebrarisch berekeningen voor tijd tot RT20 en RT30
        t0 = ((max_dB-b)/a)
        if rt20_dB > 0:
            tRT20 = ((rt20_dB-b)/a)
        else:
            print(f'WARNING: COULD NOT CALCULATE RT20; (RT20_dB={rt20_dB})')
        if rt30_dB > 0:
            tRT30 = ((rt30_dB-b)/a)
        else:
            print(f'WARNING: COULD NOT CALCULATE RT30; (RT30_dB={rt30_dB})')
        RT20 = tRT20 - t0
        RT30 = tRT30 - t0

        # neem gemmidelde van RT20 + RT30 om RT60 te berekenen
        RT60 = ((RT20*2)+(RT30*2))/2
        return RT60


    def calculate_nagalmtijd(self, duration, filtered_dB_recording, raw_recording):
        # bereken np.arrays voor 'filtered_dB_recording' en 'raw_recording'
        x_filtered = np.linspace(0, duration, (len(np.absolute(filtered_dB_recording))))
        y_filtered = filtered_dB_recording
        x_raw = np.linspace(0, duration, len(np.absolute(raw_recording)))
        y_raw = np.absolute(raw_recording)

        # functie lokale variabelen
        frame_array = []
        mean = 0
        last_mean = 0
        mean_list = []
        mode = ''
        peak_list = []
        peak_time_list = []
        is_peak_mode = False
        counted_peak = False
        peak_counts = 0
        maximum_dB = 0
        minimum_dB = 0
        clipping_audio = False
        clipping_time = 0
        warning_string = ''

        # check in 'raw_recording' of de waarde ergens 1 is, flag als 'clipping_audio'
        for i, raw_frame in enumerate(y_raw):
            if raw_frame >= 0.99:
                time_frame = x_raw[i]
                clipping_audio = True
                clipping_time = time_frame


        # reken voor elke 'frame' in 'filtered_dB_recording' (y_filtered) waardes uit
        for i, dB_filtered_frame in enumerate(y_filtered):

            time_frame = x_filtered[i]
            frame_array.append(dB_filtered_frame)

            # bereken gemiddelde
            mean = np.mean(np.asarray(frame_array))

            # bereken verschil van frame t.o.v. het gemiddelde
            difference_from_mean = (dB_filtered_frame - mean)
            difference_percentage = 100 - (mean/dB_filtered_frame)*100

            # check of dB niveau hoger of lager is dan minimum_dB en maximum_dB en verander als dat zo is
            if dB_filtered_frame > maximum_dB:
                maximum_dB = dB_filtered_frame
            if dB_filtered_frame < minimum_dB:
                minimum_dB = dB_filtered_frame

            # check of er een spike is in dB en of de modus naar DETECT PEAK moet gaan
            if difference_percentage >= self.nagalmtijd_diff_threschold_percentage:
                # check of het niet het eerste frame is, negeer de eerste piek op t=0:
                if time_frame == 0:
                    mode = 'NORMAL'
                    mean_list.append(mean)
                    peak_list.append(None)
                    peak_time_list.append(None)
                    is_peak_mode = False
                    counted_peak = False
                    last_mean = mean
                else:
                    mode = 'PEAK DETECTION'
                    mean_list.append(last_mean)
                    peak_list.append(dB_filtered_frame)
                    peak_time_list.append(time_frame)
                    is_peak_mode = True
                    last_mean = mean
            else:
                mode = 'NORMAL'
                mean_list.append(mean)
                peak_list.append(None)
                peak_time_list.append(None)
                is_peak_mode = False
                counted_peak = False
                last_mean = mean

            # telt hoeveel pieks er zijn gemeten
            if is_peak_mode and counted_peak != True:
                peak_counts += 1
                counted_peak = True
                is_peak_mode = False


            print(f''
                  f'mean: {round(mean, 2)}, '
                  f'dB: {round(dB_filtered_frame, 2)}, '
                  f't: {round(time_frame, 2)}s --- '
                  f'diff: {round(difference_from_mean, 2)} ({round(difference_percentage, 2)}%) --- '
                  f'MODE: [{mode}]')

        # check of meer dan een piek gevonden
        if peak_counts > 1:
            warning_string += f'\nWARNING: DETECTED {peak_counts} PEAKS; MORE THEN ONE PEAK!'
        if clipping_audio:
            warning_string += f'\nWARNING: AUDIO CLIPPED AT {clipping_time}'

        # print klein rapport aan het einde van de berekeningen
        print('-'*60)
        print(f'COUNTED PEAKS: {peak_counts}x')
        print(f'\nMINIMUM dB: {minimum_dB}dB')
        print(f'MAXIMUM dB: {maximum_dB}dB')
        print(f'{warning_string}')
        data_message_string = f'COUNTED PEAKS: {peak_counts}x' \
                              f'\nMINIMUM dB: {minimum_dB}dB' \
                              f'MAXIMUM dB: {maximum_dB}dB' \
                              f'{warning_string}'

        # filteren van peak_list als array
        nagalmtijd_array = np.asarray(peak_list)
        nagalmtijd_tijd_array = np.asarray(peak_time_list)

        nagalmtijd_array = nagalmtijd_array[nagalmtijd_array != None]
        nagalmtijd_tijd_array = nagalmtijd_tijd_array[nagalmtijd_tijd_array != None]

        # berekenen van daadwerkelijke nagalmtijd
        RT60 = (self.nagalmtijd_function(nagalmtijd_array, nagalmtijd_tijd_array))[0]
        if RT60 < 0:
            print('WARNING: RT60 VALUE IS NOT ACCURATE, PERFORM NEW MEASUREMENT')
        print(f'\n{("-"*60)}\nRT60 = {RT60}\n{("-"*60)}')

        mean_array = np.asarray(mean_list)
        peak_array = np.asarray(peak_list)
        return mean_array, peak_array, data_message_string
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


    def plot_dB_and_filtered(self, duration, dB_recording, filtered_dB_recording, mean_array, peak_array, data_message_string):
        x_dB = np.linspace(0, duration, len(np.absolute(dB_recording)))
        y_dB = dB_recording
        x_filtered = np.linspace(0, duration, (len(np.absolute(filtered_dB_recording))))
        y_filtered = filtered_dB_recording

        fig = plt.figure()
        ax = fig.add_subplot(111)

        plt.plot(x_dB, y_dB, label='Ongefilterde dB opname', color='lightgray')
        plt.plot(x_filtered, y_filtered, label='Gefilterde dB opname', color='blue')
        plt.plot(x_filtered, mean_array, label='dB gemiddelde', color='orange')
        plt.plot(x_filtered, peak_array, '--', label='PEAK DETECTION', color='red')
        plt.plot(x_filtered, peak_array, marker='1', color='red')
        # plt.set_facecolor("darkgray")

        plt.legend()
        ax.text(30, 5, data_message_string, fontsize = 22)
        plt.title('dB tegen tijd grafiek')
        plt.ylabel('Geluidsniveau [dB] →')
        plt.xlabel('Tijd [s] →')

        plt.rcParams["figure.figsize"] = (60,10)
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

