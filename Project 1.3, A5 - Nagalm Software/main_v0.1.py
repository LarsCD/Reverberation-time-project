# Project 1.3 - Groep A5 - Nagalmtijd Software v0.1
import sounddevice as sd
import numpy as np


#  de 'main' class houdt alle basis structuur van de code, zoals variabelen en de 'main_loop'
class main:
    def __init__(self):
        self.run_program = True
        # TODO: add variables


    # 'main_loop' is de hoofd-loop die het programma laat draaien
    def main_loop(self):
        # zolang 'self.run_program' True is, blijft 'main_loop' draaien
        while self.run_program == True:
            pass
        # TODO: code


    #  de 'recording_loop' is de loop die wordt re-runt voor elke enkele meting
    # return: dB np.array()
    def recording_loop(self):
        pass
        # TODO: - neem input
        # TODO: - doe opname
        # TODO: - verander in dB
        return dB_recording


# de 'microphone' class houdt alle functies die er voor nodig zijn om een opname met de microfoon te doen
class microphone:
    def __init__(self):
        self.frames = 44100             # (Hz): frequentie van opnamen (standaard waarde)
        self.sd.default.channels = 1    # hoeveel kanelen beschikbaar voor opname (laat 1)
        self.sd.default.device = 'Microphone (USB Audio Device)'    # selecteren de juiste microfoon


    # doet een (rauwe) opnamen van geluid voor een bepaald aantal aangegeven secondes ('duration')
    # return: np.array()
    def perform_raw_recodring(self, duration, frames):

        raw_recording = sd.rec(int(frames * duration), samplerate=frames)
        sd.wait()
        return raw_recording


    # veranderd de 'raw_recording' naar een gecorigeerde en gekalibreerde dB array
    # return np.array()
    def raw_recording_to_dB_recording(self, raw_recording):
        # neem de absolute waarde van de intensiteit
        intensiteit_ongekalibreerd = np.absolute(raw_recording)

        # correctie factor die experimenteel is bepaald
        correctiefactor_experimenteel = 0.99088
        correctiefactor_2 = 0.85000
        # TODO: Finetunen van correctie factors ↑

        # TODO: Testen of dit nodig is ↓
        # afgeleide_int = np.diff(intensiteit_ongekalibreerd)
        # intensiteit_toppen = []
        # # bereken de intensiteit op de toppen van de
        # for value in afgeleide_int:
        #     if value < 0.001:
        #         intensiteit_toppen.append(value)
        #
        # intensiteit_toppen = np.array(intensiteit_toppen)
        # TODO: Testen of dit nodig is ↑

        # verander de ongecalibreerde intensiteit waardes naar gecalibreerde gecorigeerde dB waardes
        dB_recording = (np.log((intensiteit_ongekalibreerd) / (1 * (10 ** -6))) / 0.1141) * correctiefactor_2
        return dB_recording


# de 'user_input' class houdt alle functies die er voor nodig zijn om een opname met de microfoon te doen
class user_input:
    def __init__(self):




