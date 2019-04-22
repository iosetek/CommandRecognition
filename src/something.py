import numpy as np

from src.recorder import Recorder
from src.wav_analyser import Sound
from src.mfcc import MFCCParser
from src.plot_drawer import PlotDrawer
import src.extractor as extractor

parser = MFCCParser(
    window_function=np.hamming,
    window_length=0.03,
    distance_to_next_window=0.01,
    cepstral_amount=13,
    filters_amount=30,
    fft_size=2048,
    append_energy=True,
    low_freq=0,
    max_freq=None,
    preemph_filter=0.97,
    cep_lifter=22)

# soundTest = Sound(filename="Sound/trzy 2.wav")
# mfccData = parser.toMFCC(soundTest)
# PlotDrawer.draw(mfccData)

commands = extractor.extract_mfcc(parser, "Sound/", "")

soundTest = Sound(filename="../real.wav")
mfccData = parser.to_mfcc(soundTest)
realCommand = parser.convert_to_n_frames(mfccData, 150)

which = 1
lowestDiff = 99999999
commandWithLowestDiff = ""

for command in commands:
    for i in range(3):
        x = parser.convert_to_n_frames(commands[command][i], 150)
        x = parser.normalize_to(x, 300)
        PlotDrawer.save("../Plots/" + command + " " + str(i) + ".png", x)
        diff = parser.get_difference(x, realCommand)
        if diff < lowestDiff:
            lowestDiff = diff
            commandWithLowestDiff = command
        print("%s/261 converted. Command: %s. Difference: %s" % (which, command, diff))
        which += 1

print("Recognized as: %s." % commandWithLowestDiff)