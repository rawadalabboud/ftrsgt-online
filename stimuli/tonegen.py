#!/usr/bin/env python3

import numpy as np
from scipy.io import wavfile

sampleRate = 44100
frequency = 440
duration = 0.075

t = np.linspace(0, duration, int(sampleRate * duration))  #  Produces a 5 second Audio-File
y = np.sin(frequency * 2 * np.pi * t)  #  Has frequency of 440Hz

wavfile.write('beep.wav', sampleRate, y)