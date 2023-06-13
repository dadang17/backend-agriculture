import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from matplotlib import pyplot as plt
import requests
import json
import os
from dotenv import load_dotenv
import datetime


def fuzzy_logic(last_data) :
  # Memuat variabel lingkungan dari file .env
    load_dotenv()

   #  last_data = 65
    # Variable input and Ouput

    api_url = os.getenv('WEATHER_API_URL')
    api_key = os.getenv('WEATHER_API_KEY')
    latitude = os.getenv('LATITUDE')
    longitude = os.getenv('LONGITUDE')
    
    # Input
    soilMoisture = ctrl.Antecedent(np.arange(0, 101, 1),'soilMoisture')
    temperature = ctrl.Antecedent(np.arange(0, 50.1, 0.1), 'temperature')
    curahHujan = ctrl.Antecedent(np.arange(0, 10, 0.01),'curahHujan')
    prediksiHujan = ctrl.Antecedent(np.arange(0, 10, 0.01),'prediksiHujan')

    # Output
    volumeIrrigation = ctrl.Consequent(np.arange(0, 1101, 1), 'volumeIrrigation')
    prediksiIrrigation = ctrl.Consequent(np.arange(0, 5, 1), 'prediksiIrrigation')
    fertilization = ctrl.Consequent(np.arange(0, 5, 1), 'fertilization')

    # Custom membership function
    soilMoisture['kering'] = fuzz.trapmf(soilMoisture.universe, [0, 0, 15, 30])
    soilMoisture['normal'] = fuzz.trimf(soilMoisture.universe, [25, 45, 60])
    soilMoisture['lembab'] = fuzz.trimf(soilMoisture.universe, [50, 70, 85])
    soilMoisture['basah'] = fuzz.trapmf(soilMoisture.universe, [84, 90, 100, 100])

    temperature['sangat dingin'] = fuzz.trapmf(temperature.universe, [0, 0, 10, 20])
    temperature['dingin'] = fuzz.trimf(temperature.universe, [18, 22, 26])
    temperature['normal'] = fuzz.trimf(temperature.universe, [25, 28, 31])
    temperature['panas'] = fuzz.trimf(temperature.universe, [30, 32, 35])
    temperature['sangat panas'] = fuzz.trapmf(temperature.universe, [34, 38, 50, 50])

    curahHujan['tidak hujan'] = fuzz.trapmf(curahHujan.universe, [0, 0, 0, 0])
    curahHujan['ringan'] = fuzz.trimf(curahHujan.universe, [0.01, 0.5, 0.83]) 
    curahHujan['sedang'] = fuzz.trimf(curahHujan.universe, [0.83, 1.5, 2.08])
    curahHujan['lebat'] = fuzz.trimf(curahHujan.universe, [2.08, 3.2, 4.16])
    curahHujan['sangat lebat'] = fuzz.trapmf(curahHujan.universe, [4.16, 5.3, 10, 10])

    prediksiHujan['tidak hujan'] = fuzz.trapmf(prediksiHujan.universe, [0, 0, 0, 0]) 
    prediksiHujan['ringan'] = fuzz.trimf(prediksiHujan.universe, [0.01, 0.5, 0.83]) 
    prediksiHujan['sedang'] = fuzz.trimf(prediksiHujan.universe, [0.83, 1.5, 2.08])
    prediksiHujan['lebat'] = fuzz.trimf(prediksiHujan.universe, [2.08, 3.2, 4.16])
    prediksiHujan['sangat lebat'] = fuzz.trapmf(prediksiHujan.universe, [4.16, 5.3, 10, 10])

    volumeIrrigation['sangat sedikit'] = fuzz.trapmf(volumeIrrigation.universe, [0, 0, 100, 200])
    volumeIrrigation['sedikit'] = fuzz.trimf(volumeIrrigation.universe, [180, 230, 320])
    volumeIrrigation['agak sedikit'] = fuzz.trimf(volumeIrrigation.universe, [300, 390, 480])
    volumeIrrigation['sedang'] = fuzz.trimf(volumeIrrigation.universe, [450, 520, 600])
    volumeIrrigation['agak banyak'] = fuzz.trimf(volumeIrrigation.universe, [590, 650, 750])
    volumeIrrigation['banyak'] = fuzz.trimf(volumeIrrigation.universe, [720, 810, 900])
    volumeIrrigation['sangat banyak'] = fuzz.trimf(volumeIrrigation.universe, [890, 950, 1000])
    volumeIrrigation['tidak perlu'] = fuzz.trapmf(volumeIrrigation.universe, [1000, 1000, 2000, 2000])

    prediksiIrrigation['disarankan'] = fuzz.trimf(prediksiIrrigation.universe, [0, 1, 2])
    prediksiIrrigation['tidak disarankan'] = fuzz.trimf(prediksiIrrigation.universe, [2, 3, 4])

    fertilization['disarankan'] = fuzz.trimf(fertilization.universe, [0, 1, 2])
    fertilization['tidak disarankan'] = fuzz.trimf(prediksiIrrigation.universe, [2, 3, 4])

    # prediksiHujan.view()
    # curahHujan.view()
    # soilMoisture.view()
    # temperature.view()
    # fertilization.view()
    # prediksiIrrigation.view()
    # volumeIrrigation.view()

    # Rule Menentukan volume air
    # Input : Kelembaban tanah, Suhu, 
    # Output : Jumlah Air yang dibutuhkan

    rule1 = ctrl.Rule(soilMoisture['kering'] & temperature['sangat dingin'] & curahHujan['tidak hujan'], volumeIrrigation['agak sedikit'])
    rule2 = ctrl.Rule(soilMoisture['kering'] & temperature['sangat dingin'] & curahHujan['ringan'], volumeIrrigation['agak sedikit'])
    rule3 = ctrl.Rule(soilMoisture['kering'] & temperature['sangat dingin'] & curahHujan['sedang'], volumeIrrigation['sedikit'])
    rule4 = ctrl.Rule(soilMoisture['kering'] & temperature['sangat dingin'] & curahHujan['lebat'], volumeIrrigation['sangat sedikit'])
    rule5 = ctrl.Rule(soilMoisture['kering'] & temperature['sangat dingin'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule6 = ctrl.Rule(soilMoisture['kering'] & temperature['dingin'] & curahHujan['tidak hujan'], volumeIrrigation['sedang'])
    rule7 = ctrl.Rule(soilMoisture['kering'] & temperature['dingin'] & curahHujan['ringan'], volumeIrrigation['agak sedikit'])
    rule8 = ctrl.Rule(soilMoisture['kering'] & temperature['dingin'] & curahHujan['sedang'], volumeIrrigation['sedikit'])
    rule9 = ctrl.Rule(soilMoisture['kering'] & temperature['dingin'] & curahHujan['lebat'], volumeIrrigation['sangat sedikit'])
    rule10 = ctrl.Rule(soilMoisture['kering'] & temperature['dingin'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule11 = ctrl.Rule(soilMoisture['kering'] & temperature['normal'] & curahHujan['tidak hujan'], volumeIrrigation['agak banyak'])
    rule12 = ctrl.Rule(soilMoisture['kering'] & temperature['normal'] & curahHujan['ringan'], volumeIrrigation['sedang'])
    rule13 = ctrl.Rule(soilMoisture['kering'] & temperature['normal'] & curahHujan['sedang'], volumeIrrigation['sedikit'])
    rule14 = ctrl.Rule(soilMoisture['kering'] & temperature['normal'] & curahHujan['lebat'], volumeIrrigation['sangat sedikit'])
    rule15 = ctrl.Rule(soilMoisture['kering'] & temperature['normal'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule16 = ctrl.Rule(soilMoisture['kering'] & temperature['panas'] & curahHujan['tidak hujan'], volumeIrrigation['banyak'])
    rule17 = ctrl.Rule(soilMoisture['kering'] & temperature['panas'] & curahHujan['ringan'], volumeIrrigation['agak banyak'])
    rule18 = ctrl.Rule(soilMoisture['kering'] & temperature['panas'] & curahHujan['sedang'], volumeIrrigation['sedang'])
    rule19 = ctrl.Rule(soilMoisture['kering'] & temperature['panas'] & curahHujan['lebat'], volumeIrrigation['agak sedikit'])
    rule20 = ctrl.Rule(soilMoisture['kering'] & temperature['panas'] & curahHujan['sangat lebat'], volumeIrrigation['sangat sedikit'])

    rule21 = ctrl.Rule(soilMoisture['kering'] & temperature['sangat panas'] & curahHujan['tidak hujan'], volumeIrrigation['sangat banyak'])
    rule22 = ctrl.Rule(soilMoisture['kering'] & temperature['sangat panas'] & curahHujan['ringan'], volumeIrrigation['banyak'])
    rule23 = ctrl.Rule(soilMoisture['kering'] & temperature['sangat panas'] & curahHujan['sedang'], volumeIrrigation['agak banyak'])
    rule24 = ctrl.Rule(soilMoisture['kering'] & temperature['sangat panas'] & curahHujan['lebat'], volumeIrrigation['sedang'])
    rule25 = ctrl.Rule(soilMoisture['kering'] & temperature['sangat panas'] & curahHujan['sangat lebat'], volumeIrrigation['sangat sedikit'])

    rule26 = ctrl.Rule(soilMoisture['normal'] & temperature['sangat dingin'] & curahHujan['tidak hujan'], volumeIrrigation['sedikit'])
    rule27 = ctrl.Rule(soilMoisture['normal'] & temperature['sangat dingin'] & curahHujan['ringan'], volumeIrrigation['sedikit'])
    rule28 = ctrl.Rule(soilMoisture['normal'] & temperature['sangat dingin'] & curahHujan['sedang'], volumeIrrigation['sangat sedikit'])
    rule29 = ctrl.Rule(soilMoisture['normal'] & temperature['sangat dingin'] & curahHujan['lebat'], volumeIrrigation['tidak perlu'])
    rule30 = ctrl.Rule(soilMoisture['normal'] & temperature['sangat dingin'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule31 = ctrl.Rule(soilMoisture['normal'] & temperature['dingin'] & curahHujan['tidak hujan'], volumeIrrigation['agak sedikit'])
    rule32 = ctrl.Rule(soilMoisture['normal'] & temperature['dingin'] & curahHujan['ringan'], volumeIrrigation['sedikit'])
    rule33 = ctrl.Rule(soilMoisture['normal'] & temperature['dingin'] & curahHujan['sedang'], volumeIrrigation['sangat sedikit'])
    rule34 = ctrl.Rule(soilMoisture['normal'] & temperature['dingin'] & curahHujan['lebat'], volumeIrrigation['tidak perlu'])
    rule35 = ctrl.Rule(soilMoisture['normal'] & temperature['dingin'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule36 = ctrl.Rule(soilMoisture['normal'] & temperature['normal'] & curahHujan['tidak hujan'], volumeIrrigation['sedang'])
    rule37 = ctrl.Rule(soilMoisture['normal'] & temperature['normal'] & curahHujan['ringan'], volumeIrrigation['agak sedikit'])
    rule38 = ctrl.Rule(soilMoisture['normal'] & temperature['normal'] & curahHujan['sedang'], volumeIrrigation['sedikit'])
    rule39 = ctrl.Rule(soilMoisture['normal'] & temperature['normal'] & curahHujan['lebat'], volumeIrrigation['sangat sedikit'])
    rule40 = ctrl.Rule(soilMoisture['normal'] & temperature['normal'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule41 = ctrl.Rule(soilMoisture['normal'] & temperature['panas'] & curahHujan['tidak hujan'], volumeIrrigation['agak banyak'])
    rule42 = ctrl.Rule(soilMoisture['normal'] & temperature['panas'] & curahHujan['ringan'], volumeIrrigation['sedang'])
    rule43 = ctrl.Rule(soilMoisture['normal'] & temperature['panas'] & curahHujan['sedang'], volumeIrrigation['agak sedikit'])
    rule44 = ctrl.Rule(soilMoisture['normal'] & temperature['panas'] & curahHujan['lebat'], volumeIrrigation['sedikit'])
    rule45 = ctrl.Rule(soilMoisture['normal'] & temperature['panas'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule46 = ctrl.Rule(soilMoisture['normal'] & temperature['sangat panas'] & curahHujan['tidak hujan'], volumeIrrigation['banyak'])
    rule47 = ctrl.Rule(soilMoisture['normal'] & temperature['sangat panas'] & curahHujan['ringan'], volumeIrrigation['sedang'])
    rule48 = ctrl.Rule(soilMoisture['normal'] & temperature['sangat panas'] & curahHujan['sedang'], volumeIrrigation['agak sedikit'])
    rule49 = ctrl.Rule(soilMoisture['normal'] & temperature['sangat panas'] & curahHujan['lebat'], volumeIrrigation['sedikit'])
    rule50 = ctrl.Rule(soilMoisture['normal'] & temperature['sangat panas'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule51 = ctrl.Rule(soilMoisture['lembab'] & temperature['sangat dingin'] & curahHujan['tidak hujan'], volumeIrrigation['sedikit'])
    rule52 = ctrl.Rule(soilMoisture['lembab'] & temperature['sangat dingin'] & curahHujan['ringan'], volumeIrrigation['sedikit'])
    rule53 = ctrl.Rule(soilMoisture['lembab'] & temperature['sangat dingin'] & curahHujan['sedang'], volumeIrrigation['sangat sedikit'])
    rule54 = ctrl.Rule(soilMoisture['lembab'] & temperature['sangat dingin'] & curahHujan['lebat'], volumeIrrigation['tidak perlu'])
    rule55 = ctrl.Rule(soilMoisture['lembab'] & temperature['sangat dingin'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule56 = ctrl.Rule(soilMoisture['lembab'] & temperature['dingin'] & curahHujan['tidak hujan'], volumeIrrigation['sedikit'])
    rule57 = ctrl.Rule(soilMoisture['lembab'] & temperature['dingin'] & curahHujan['ringan'], volumeIrrigation['sedikit'])
    rule58 = ctrl.Rule(soilMoisture['lembab'] & temperature['dingin'] & curahHujan['sedang'], volumeIrrigation['sangat sedikit'])
    rule59 = ctrl.Rule(soilMoisture['lembab'] & temperature['dingin'] & curahHujan['lebat'], volumeIrrigation['tidak perlu'])
    rule60 = ctrl.Rule(soilMoisture['lembab'] & temperature['dingin'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule61 = ctrl.Rule(soilMoisture['lembab'] & temperature['normal'] & curahHujan['tidak hujan'], volumeIrrigation['agak sedikit'])
    rule62 = ctrl.Rule(soilMoisture['lembab'] & temperature['normal'] & curahHujan['ringan'], volumeIrrigation['agak sedikit'])
    rule63 = ctrl.Rule(soilMoisture['lembab'] & temperature['normal'] & curahHujan['sedang'], volumeIrrigation['sedikit'])
    rule64 = ctrl.Rule(soilMoisture['lembab'] & temperature['normal'] & curahHujan['lebat'], volumeIrrigation['sangat sedikit'])
    rule65 = ctrl.Rule(soilMoisture['lembab'] & temperature['normal'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule66 = ctrl.Rule(soilMoisture['lembab'] & temperature['panas'] & curahHujan['tidak hujan'], volumeIrrigation['sedang'])
    rule67 = ctrl.Rule(soilMoisture['lembab'] & temperature['panas'] & curahHujan['ringan'], volumeIrrigation['agak sedikit'])
    rule68 = ctrl.Rule(soilMoisture['lembab'] & temperature['panas'] & curahHujan['sedang'], volumeIrrigation['sedikit'])
    rule69 = ctrl.Rule(soilMoisture['lembab'] & temperature['panas'] & curahHujan['lebat'], volumeIrrigation['sangat sedikit'])
    rule70 = ctrl.Rule(soilMoisture['lembab'] & temperature['panas'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule71 = ctrl.Rule(soilMoisture['lembab'] & temperature['sangat panas'] & curahHujan['tidak hujan'], volumeIrrigation['agak banyak'])
    rule72 = ctrl.Rule(soilMoisture['lembab'] & temperature['sangat panas'] & curahHujan['ringan'], volumeIrrigation['agak sedikit'])
    rule73 = ctrl.Rule(soilMoisture['lembab'] & temperature['sangat panas'] & curahHujan['sedang'], volumeIrrigation['sedikit'])
    rule74 = ctrl.Rule(soilMoisture['lembab'] & temperature['sangat panas'] & curahHujan['lebat'], volumeIrrigation['sangat sedikit'])
    rule75 = ctrl.Rule(soilMoisture['lembab'] & temperature['sangat panas'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule76 = ctrl.Rule(soilMoisture['basah'] & temperature['sangat dingin'] & curahHujan['tidak hujan'], volumeIrrigation['sangat sedikit'])
    rule77 = ctrl.Rule(soilMoisture['basah'] & temperature['sangat dingin'] & curahHujan['ringan'], volumeIrrigation['sangat sedikit'])
    rule78 = ctrl.Rule(soilMoisture['basah'] & temperature['sangat dingin'] & curahHujan['sedang'], volumeIrrigation['tidak perlu'])
    rule79 = ctrl.Rule(soilMoisture['basah'] & temperature['sangat dingin'] & curahHujan['lebat'], volumeIrrigation['tidak perlu'])
    rule80 = ctrl.Rule(soilMoisture['basah'] & temperature['sangat dingin'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule81 = ctrl.Rule(soilMoisture['basah'] & temperature['dingin'] & curahHujan['tidak hujan'], volumeIrrigation['sedikit'])
    rule82 = ctrl.Rule(soilMoisture['basah'] & temperature['dingin'] & curahHujan['ringan'], volumeIrrigation['sangat sedikit'])
    rule83 = ctrl.Rule(soilMoisture['basah'] & temperature['dingin'] & curahHujan['sedang'], volumeIrrigation['tidak perlu'])
    rule84 = ctrl.Rule(soilMoisture['basah'] & temperature['dingin'] & curahHujan['lebat'], volumeIrrigation['tidak perlu'])
    rule85 = ctrl.Rule(soilMoisture['basah'] & temperature['dingin'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule86 = ctrl.Rule(soilMoisture['basah'] & temperature['normal'] & curahHujan['tidak hujan'], volumeIrrigation['agak sedikit'])
    rule87 = ctrl.Rule(soilMoisture['basah'] & temperature['normal'] & curahHujan['ringan'], volumeIrrigation['sedikit'])
    rule88 = ctrl.Rule(soilMoisture['basah'] & temperature['normal'] & curahHujan['sedang'], volumeIrrigation['sangat sedikit'])
    rule89 = ctrl.Rule(soilMoisture['basah'] & temperature['normal'] & curahHujan['lebat'], volumeIrrigation['tidak perlu'])
    rule90 = ctrl.Rule(soilMoisture['basah'] & temperature['normal'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule91 = ctrl.Rule(soilMoisture['basah'] & temperature['panas'] & curahHujan['tidak hujan'], volumeIrrigation['sedang'])
    rule92 = ctrl.Rule(soilMoisture['basah'] & temperature['panas'] & curahHujan['ringan'], volumeIrrigation['sedikit'])
    rule93 = ctrl.Rule(soilMoisture['basah'] & temperature['panas'] & curahHujan['sedang'], volumeIrrigation['sangat sedikit'])
    rule94 = ctrl.Rule(soilMoisture['basah'] & temperature['panas'] & curahHujan['lebat'], volumeIrrigation['tidak perlu'])
    rule95 = ctrl.Rule(soilMoisture['basah'] & temperature['panas'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])

    rule96 = ctrl.Rule(soilMoisture['basah'] & temperature['sangat panas'] & curahHujan['tidak hujan'], volumeIrrigation['agak banyak'])
    rule97 = ctrl.Rule(soilMoisture['basah'] & temperature['sangat panas'] & curahHujan['ringan'], volumeIrrigation['agak sedikit'])
    rule98 = ctrl.Rule(soilMoisture['basah'] & temperature['sangat panas'] & curahHujan['sedang'], volumeIrrigation['sedikit'])
    rule99 = ctrl.Rule(soilMoisture['basah'] & temperature['sangat panas'] & curahHujan['lebat'], volumeIrrigation['sangat sedikit'])
    rule100 = ctrl.Rule(soilMoisture['basah'] & temperature['sangat panas'] & curahHujan['sangat lebat'], volumeIrrigation['tidak perlu'])


    # Rules Menentukan Perlakuan Penyiraman dengan prediksi cuaca

    rule101 = ctrl.Rule(soilMoisture['kering'] & prediksiHujan['tidak hujan'], prediksiIrrigation['disarankan'])
    rule102 = ctrl.Rule(soilMoisture['kering'] & prediksiHujan['ringan'], prediksiIrrigation['disarankan'])
    rule103 = ctrl.Rule(soilMoisture['kering'] & prediksiHujan['sedang'], prediksiIrrigation['disarankan'])
    rule104 = ctrl.Rule(soilMoisture['kering'] & prediksiHujan['lebat'], prediksiIrrigation['tidak disarankan'])
    rule105 = ctrl.Rule(soilMoisture['kering'] & prediksiHujan['sangat lebat'], prediksiIrrigation['tidak disarankan'])

    rule106 = ctrl.Rule(soilMoisture['normal'] & prediksiHujan['tidak hujan'], prediksiIrrigation['disarankan'])
    rule107 = ctrl.Rule(soilMoisture['normal'] & prediksiHujan['ringan'], prediksiIrrigation['disarankan'])
    rule108 = ctrl.Rule(soilMoisture['normal'] & prediksiHujan['sedang'], prediksiIrrigation['disarankan'])
    rule109 = ctrl.Rule(soilMoisture['normal'] & prediksiHujan['lebat'], prediksiIrrigation['tidak disarankan'])
    rule110 = ctrl.Rule(soilMoisture['normal'] & prediksiHujan['sangat lebat'], prediksiIrrigation['tidak disarankan'])

    rule111 = ctrl.Rule(soilMoisture['lembab'] & prediksiHujan['tidak hujan'], prediksiIrrigation['disarankan'])
    rule112 = ctrl.Rule(soilMoisture['lembab'] & prediksiHujan['ringan'], prediksiIrrigation['disarankan'])
    rule113 = ctrl.Rule(soilMoisture['lembab'] & prediksiHujan['sedang'], prediksiIrrigation['tidak disarankan'])
    rule114 = ctrl.Rule(soilMoisture['lembab'] & prediksiHujan['lebat'], prediksiIrrigation['tidak disarankan'])
    rule115 = ctrl.Rule(soilMoisture['lembab'] & prediksiHujan['sangat lebat'], prediksiIrrigation['tidak disarankan'])

    rule116 = ctrl.Rule(soilMoisture['basah'] & prediksiHujan['tidak hujan'], prediksiIrrigation['tidak disarankan'])
    rule117 = ctrl.Rule(soilMoisture['basah'] & prediksiHujan['ringan'], prediksiIrrigation['tidak disarankan'])
    rule118 = ctrl.Rule(soilMoisture['basah'] & prediksiHujan['sedang'], prediksiIrrigation['tidak disarankan'])
    rule119 = ctrl.Rule(soilMoisture['basah'] & prediksiHujan['lebat'], prediksiIrrigation['tidak disarankan'])
    rule120 = ctrl.Rule(soilMoisture['basah'] & prediksiHujan['sangat lebat'], prediksiIrrigation['tidak disarankan'])


    # Rules Menentukan Perlakuan Pemupukan
    # 

    # cuaca realtime
    rule121 = ctrl.Rule(soilMoisture['basah'] & curahHujan['tidak hujan'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule122 = ctrl.Rule(soilMoisture['basah'] & curahHujan['tidak hujan'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule123 = ctrl.Rule(soilMoisture['basah'] & curahHujan['tidak hujan'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule124 = ctrl.Rule(soilMoisture['basah'] & curahHujan['tidak hujan'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule125 = ctrl.Rule(soilMoisture['basah'] & curahHujan['tidak hujan'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule126 = ctrl.Rule(soilMoisture['basah'] & curahHujan['ringan'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule127 = ctrl.Rule(soilMoisture['basah'] & curahHujan['ringan'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule128 = ctrl.Rule(soilMoisture['basah'] & curahHujan['ringan'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule129 = ctrl.Rule(soilMoisture['basah'] & curahHujan['ringan'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule130 = ctrl.Rule(soilMoisture['basah'] & curahHujan['ringan'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule131 = ctrl.Rule(soilMoisture['basah'] & curahHujan['sedang'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule132 = ctrl.Rule(soilMoisture['basah'] & curahHujan['sedang'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule133 = ctrl.Rule(soilMoisture['basah'] & curahHujan['sedang'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule134 = ctrl.Rule(soilMoisture['basah'] & curahHujan['sedang'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule135 = ctrl.Rule(soilMoisture['basah'] & curahHujan['sedang'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule136 = ctrl.Rule(soilMoisture['basah'] & curahHujan['lebat'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule137 = ctrl.Rule(soilMoisture['basah'] & curahHujan['lebat'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule138 = ctrl.Rule(soilMoisture['basah'] & curahHujan['lebat'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule139 = ctrl.Rule(soilMoisture['basah'] & curahHujan['lebat'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule140 = ctrl.Rule(soilMoisture['basah'] & curahHujan['lebat'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule141 = ctrl.Rule(soilMoisture['basah'] & curahHujan['sangat lebat'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule142 = ctrl.Rule(soilMoisture['basah'] & curahHujan['sangat lebat'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule143 = ctrl.Rule(soilMoisture['basah'] & curahHujan['sangat lebat'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule144 = ctrl.Rule(soilMoisture['basah'] & curahHujan['sangat lebat'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule145 = ctrl.Rule(soilMoisture['basah'] & curahHujan['sangat lebat'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule146 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['tidak hujan'] & prediksiHujan['tidak hujan'], fertilization['disarankan'])
    rule147 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['tidak hujan'] & prediksiHujan['ringan'], fertilization['disarankan'])
    rule148 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['tidak hujan'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule149 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['tidak hujan'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule150 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['tidak hujan'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule151 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['ringan'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule152 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['ringan'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule153 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['ringan'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule154 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['ringan'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule155 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['ringan'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule156 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['sedang'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule157 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['sedang'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule158 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['sedang'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule159 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['sedang'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule160 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['sedang'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule161 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['lebat'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule162 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['lebat'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule163 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['lebat'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule164 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['lebat'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule165 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['lebat'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule166 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['sangat lebat'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule167 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['sangat lebat'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule168 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['sangat lebat'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule169 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['sangat lebat'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule170 = ctrl.Rule(soilMoisture['lembab'] & curahHujan['sangat lebat'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule171 = ctrl.Rule(soilMoisture['normal'] & curahHujan['tidak hujan'] & prediksiHujan['tidak hujan'], fertilization['disarankan'])
    rule172 = ctrl.Rule(soilMoisture['normal'] & curahHujan['tidak hujan'] & prediksiHujan['ringan'], fertilization['disarankan'])
    rule173 = ctrl.Rule(soilMoisture['normal'] & curahHujan['tidak hujan'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule174 = ctrl.Rule(soilMoisture['normal'] & curahHujan['tidak hujan'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule175 = ctrl.Rule(soilMoisture['normal'] & curahHujan['tidak hujan'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule176 = ctrl.Rule(soilMoisture['normal'] & curahHujan['ringan'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule177 = ctrl.Rule(soilMoisture['normal'] & curahHujan['ringan'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule178 = ctrl.Rule(soilMoisture['normal'] & curahHujan['ringan'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule179 = ctrl.Rule(soilMoisture['normal'] & curahHujan['ringan'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule180 = ctrl.Rule(soilMoisture['normal'] & curahHujan['ringan'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule181 = ctrl.Rule(soilMoisture['normal'] & curahHujan['sedang'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule182 = ctrl.Rule(soilMoisture['normal'] & curahHujan['sedang'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule183 = ctrl.Rule(soilMoisture['normal'] & curahHujan['sedang'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule184 = ctrl.Rule(soilMoisture['normal'] & curahHujan['sedang'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule185 = ctrl.Rule(soilMoisture['normal'] & curahHujan['sedang'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule186 = ctrl.Rule(soilMoisture['normal'] & curahHujan['lebat'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule187 = ctrl.Rule(soilMoisture['normal'] & curahHujan['lebat'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule188 = ctrl.Rule(soilMoisture['normal'] & curahHujan['lebat'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule189 = ctrl.Rule(soilMoisture['normal'] & curahHujan['lebat'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule190 = ctrl.Rule(soilMoisture['normal'] & curahHujan['lebat'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule191 = ctrl.Rule(soilMoisture['normal'] & curahHujan['sangat lebat'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule192 = ctrl.Rule(soilMoisture['normal'] & curahHujan['sangat lebat'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule193 = ctrl.Rule(soilMoisture['normal'] & curahHujan['sangat lebat'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule194 = ctrl.Rule(soilMoisture['normal'] & curahHujan['sangat lebat'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule195 = ctrl.Rule(soilMoisture['normal'] & curahHujan['sangat lebat'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule196 = ctrl.Rule(soilMoisture['kering'] & curahHujan['tidak hujan'] & prediksiHujan['tidak hujan'], fertilization['disarankan'])
    rule197 = ctrl.Rule(soilMoisture['kering'] & curahHujan['tidak hujan'] & prediksiHujan['ringan'], fertilization['disarankan'])
    rule198 = ctrl.Rule(soilMoisture['kering'] & curahHujan['tidak hujan'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule199 = ctrl.Rule(soilMoisture['kering'] & curahHujan['tidak hujan'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule200 = ctrl.Rule(soilMoisture['kering'] & curahHujan['tidak hujan'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule201 = ctrl.Rule(soilMoisture['kering'] & curahHujan['ringan'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule202 = ctrl.Rule(soilMoisture['kering'] & curahHujan['ringan'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule203 = ctrl.Rule(soilMoisture['kering'] & curahHujan['ringan'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule204 = ctrl.Rule(soilMoisture['kering'] & curahHujan['ringan'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule205 = ctrl.Rule(soilMoisture['kering'] & curahHujan['ringan'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule206 = ctrl.Rule(soilMoisture['kering'] & curahHujan['sedang'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule207 = ctrl.Rule(soilMoisture['kering'] & curahHujan['sedang'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule208 = ctrl.Rule(soilMoisture['kering'] & curahHujan['sedang'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule209 = ctrl.Rule(soilMoisture['kering'] & curahHujan['sedang'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule210 = ctrl.Rule(soilMoisture['kering'] & curahHujan['sedang'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule211 = ctrl.Rule(soilMoisture['kering'] & curahHujan['lebat'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule212 = ctrl.Rule(soilMoisture['kering'] & curahHujan['lebat'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule213 = ctrl.Rule(soilMoisture['kering'] & curahHujan['lebat'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule214 = ctrl.Rule(soilMoisture['kering'] & curahHujan['lebat'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule215 = ctrl.Rule(soilMoisture['kering'] & curahHujan['lebat'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])

    rule216 = ctrl.Rule(soilMoisture['kering'] & curahHujan['sangat lebat'] & prediksiHujan['tidak hujan'], fertilization['tidak disarankan'])
    rule217 = ctrl.Rule(soilMoisture['kering'] & curahHujan['sangat lebat'] & prediksiHujan['ringan'], fertilization['tidak disarankan'])
    rule218 = ctrl.Rule(soilMoisture['kering'] & curahHujan['sangat lebat'] & prediksiHujan['sedang'], fertilization['tidak disarankan'])
    rule219 = ctrl.Rule(soilMoisture['kering'] & curahHujan['sangat lebat'] & prediksiHujan['lebat'], fertilization['tidak disarankan'])
    rule220 = ctrl.Rule(soilMoisture['kering'] & curahHujan['sangat lebat'] & prediksiHujan['sangat lebat'], fertilization['tidak disarankan'])


    irrigation_ctrl = ctrl.ControlSystem([
        rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, 
        rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
        rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30, 
        rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40, 
        rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50, 
        rule51, rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60, 
        rule61, rule62, rule63, rule64, rule65, rule66, rule67, rule68, rule69, rule70, 
        rule71, rule72, rule73, rule74, rule75, rule76, rule77, rule78, rule79, rule80, 
        rule81, rule82, rule83, rule84, rule85, rule86, rule87, rule88, rule89, rule90, 
        rule91, rule92, rule93, rule94, rule95, rule96, rule97, rule98, rule99, rule100])

    prediksiIrrigation_ctrl = ctrl.ControlSystem([
        rule101, rule102, rule103, rule104, 
        rule105, rule106, rule107, rule108, 
        rule109, rule110, rule111, rule112, 
        rule113, rule114, rule115, rule116, 
        rule117, rule118, rule119, rule120]) 

    fertilization_ctrl = ctrl.ControlSystem([
        rule121, rule122, rule123, rule124, rule125, rule126, rule127, rule128, rule129, rule130,
        rule131, rule132, rule133, rule134, rule135, rule136, rule137, rule138, rule139, rule140,
        rule141, rule142, rule143, rule144, rule145, rule146, rule147, rule148, rule149, rule150,
        rule151, rule152, rule153, rule154, rule155, rule156, rule157, rule158, rule159, rule160,
        rule161, rule162, rule163, rule164, rule165, rule166, rule167, rule168, rule169, rule170,
        rule171, rule172, rule173, rule174, rule175, rule176, rule177, rule178, rule179, rule180,
        rule181, rule182, rule183, rule184, rule185, rule186, rule187, rule188, rule189, rule190,
        rule191, rule192, rule193, rule194, rule195, rule196, rule197, rule198, rule199, rule200,
        rule201, rule202, rule203, rule204, rule205, rule206, rule207, rule208, rule209, rule210,
        rule211, rule212, rule213, rule214, rule215, rule216, rule217, rule218, rule219, rule220
    ])


    volume_irrigation = ctrl.ControlSystemSimulation(irrigation_ctrl)
    fertilization_logic = ctrl.ControlSystemSimulation(fertilization_ctrl)
    prediksi_irrigation = ctrl.ControlSystemSimulation(prediksiIrrigation_ctrl)


    # Fetch data current weather
    url_current = f"{api_url}/weather"
    url_forecast = f"{api_url}/forecast"

    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': api_key,
        'units': 'metric'
    }
    response_current = requests.get(url_current, params=params)

    if response_current.status_code == 200:
        current_weather = response_current.json()
        temp = round(current_weather['main']['temp'])
        # print("Hasil data current: ", json.dumps(current_weather, indent=4))
        print("Get data current berhasil")
      #   print(temp)

    else:
        print('Error dalam mengambil data:', response_current.status_code)

    response_forecast = requests.get(url_forecast, params=params)

    if response_forecast.status_code == 200:
        forecast_weather = response_forecast.json()
        # print("Hasil data prediksi : ",json.dumps(forecast_weather, indent=4))
        print("Get data forecast berhasil")
        

    else:
        print('Error dalam mengambil data:', response_forecast.status_code)


    # fungsi mengubah curah hujan
    def toHour(rain_3h):
        # Blok kode fungsi
        # Tindakan yang akan dilakukan oleh fungsi
        # Pengembalian nilai (opsional)
        rain_1h = rain_3h / 3
        return rain_1h

    def getDataForecastTerdekat() :
       # Waktu saat ini
       waktu_sekarang = datetime.datetime.now()
       
       # Memilih data dari daftar berdasarkan tanggal dan jam
       data_terpilih = None
      #  print("ini forecast", forecast_weather)
      #  print("waktu sekarang : ", waktu_sekarang)
       for data in forecast_weather['list']:
          dt_txt = datetime.datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
          if dt_txt > waktu_sekarang:
            data_terpilih = data
            break
       
      #  print("ini data txt",data_terpilih)
       return data_terpilih
    
    def irrigation() :
       print("------------Ini Hasil Output Current---------")
       # check ada data hujan di json
       if rain_dataCurrent :
         print("Hujan sedang terjadi")
         rain_3h = rain_dataCurrent.get("3h") 
         # check jenis rain 3h atau 1h
         if rain_3h:
            rainCurrent = toHour(rain_3h)
         else :
            print("tidak ada 3h")
            rainCurrent = rain_dataCurrent.get("1h")
       else :
         rainCurrent = 0
         print("tidak hujan")
       volume_irrigation.input['curahHujan'] = rainCurrent
       volume_irrigation.input['soilMoisture'] = last_data
       volume_irrigation.input['temperature'] = temp
       volume_irrigation.compute()
       print("curah hujan = ", rainCurrent)
       print("Kelembaban tanah = ", last_data)
       print("suhu = ", temp)
       print(volume_irrigation.output['volumeIrrigation'])
      #  volumeIrrigation.view(sim=volume_irrigation)
       
       print("------------Ini Hasil Output Forecast---------")
       # check ada data hujan di json
       if rain_dataForecast :
          print("Hujan sedang terjadi")
          rain_3h = rain_dataForecast.get("3h") 
          # check jenis rain 3h atau 1h
          if rain_3h:
             rainForecast = toHour(rain_3h)
          else :
             print("tidak ada 3h")
             rainForecast = rain_dataCurrent.get("1h")
       else :
          rainForecast = 0
          print("tidak terjadi hujan")
       prediksi_irrigation.input['prediksiHujan'] = rainForecast
       prediksi_irrigation.input['soilMoisture'] = last_data
       prediksi_irrigation.compute()
       print("curah hujan = ", rainForecast)
       print("Kelembaban tanah = ", last_data)
       print(prediksi_irrigation.output['prediksiIrrigation'])
      #  prediksiIrrigation.view(sim=prediksi_irrigation)
       
       if(rainForecast == 0):
          kForecast = "Tidak Hujan"
       else :
          kForecast = "Hujan"
       
       
       if (prediksi_irrigation.output['prediksiIrrigation'] >=0 and prediksi_irrigation.output['prediksiIrrigation'] < 2 ) :
          print(f"Prediksi cuaca {kForecast}, kelembaban tanah bernilai {last_data} dan hasil logika fuzzy bernilai {prediksi_irrigation.output['prediksiIrrigation']} maka penyiraman disarankan")
       else :
          print(f"Prediksi cuaca {kForecast}, kelembaban tanah bernilai {last_data} dan hasil logika fuzzy bernilai {prediksi_irrigation.output['prediksiIrrigation']} maka penyiraman tidak disarankan")

    def fertilizationFunction() :
       # check ada hujan atau tidak untuk cuaca realtime
       if rain_dataCurrent :
          print("Hujan sedang terjadi")
          # check rain 3h 
          rain_3h = rain_dataCurrent.get("3h") 
          if rain_3h:
             rainCurrent = toHour(rain_3h)
          else :
             print("tidak ada 3h")
             rainCurrent = rain_dataCurrent.get("1h")
       else :
          rainCurrent = 0
          print("tidak hujan")


       # check ada hujan atau tidak untuk cuaca prediksi
       if rain_dataForecast :
          print("Hujan sedang terjadi")
          # check rain 3h 
          rain_3h = rain_dataForecast.get("3h") 
          if rain_3h:
             rainForecast = toHour(rain_3h)
          else :
             print("tidak ada 3h")
             rainForecast = rain_dataForecast("1h")
       else :
          rainForecast = 0
          print("tidak hujan")
       
       fertilization_logic.input['curahHujan'] = rainCurrent
       fertilization_logic.input['prediksiHujan'] = rainForecast
       fertilization_logic.input['soilMoisture'] = last_data
       fertilization_logic.compute()
       print(fertilization_logic.output['fertilization'])
      #  fertilization.view(sim=fertilization_logic)
       
       if(rainCurrent == 0):
          kCurrent = "Tidak Hujan"
       else :
          kCurrent = "Hujan"
       
       if(rainForecast == 0):
          kForecast = "Tidak Hujan"
       else :
          kForecast = "Hujan"
       
       print("kelembaban tanah : ",last_data)
       
       if (fertilization_logic.output['fertilization'] >=0 and fertilization_logic.output['fertilization'] < 2 ) :
          print(f"cuaca hari ini {kCurrent} dengan curah hujan {rainCurrent}, prediksi cuaca {kForecast} dengan curah hujan {rainForecast} dan hasil logika fuzzy bernilai {fertilization_logic.output['fertilization']} maka pemupukan disarankan")
       else :
          print(f"cuaca hari ini {kCurrent} dengan curah hujan {rainCurrent}, prediksi cuaca {kForecast} dengan curah hujan {rainForecast} dan hasil logika fuzzy bernilai {fertilization_logic.output['fertilization']} maka pemupukan tidak disarankan")


    data_prediksi = getDataForecastTerdekat()
    print(data_prediksi)
    rain_dataCurrent = current_weather.get("rain")
    rain_dataForecast = data_prediksi.get("rain")

    irrigation()
    fertilizationFunction()

# fuzzy_logic()