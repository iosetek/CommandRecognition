from recorder import Recorder
from wavAnalyser import Sound
from mfcc import MFCCParser
from plotDrawer import PlotDrawer
import extractor
import numpy as np

parser = MFCCParser(
    windowFunction=np.hamming,
    windowLength=0.03,
    distanceToNextWindow=0.01,
    cepstralAmount=13,
    filtersAmount=30,
    FFTsize=2048,
    appendEnergy=True,
    lowFreq=0,
    maxFreq=None,
    preemphFilter=0.97,
    cepLifter=22)

# soundTest = Sound(filename="Sound/trzy 2.wav")
# mfccData = parser.toMFCC(soundTest)
# PlotDrawer.draw(mfccData)

commands = extractor.extractMFCC(parser, "Sound/", "")

soundTest = Sound(filename="../real.wav")
mfccData = parser.toMFCC(soundTest)
realCommand = parser.convertToNFrames(mfccData, 150)

which = 1
lowestDiff = 99999999
commandWithLowestDiff = ""

for command in commands:
    for i in range(0, 3):
        x = parser.convertToNFrames(commands[command][i], 150)
        x = parser.normalizeTo(x, 300)
        PlotDrawer.save("../Plots/" + command + " " + str(i) + ".png", x)
        diff = parser.getDifference(x, realCommand)
        if diff < lowestDiff:
            lowestDiff = diff
            commandWithLowestDiff = command
        print("%s/261 converted. Command: %s. Difference: %s" % (which, command, diff))
        which += 1

print("Recognized as: %s." % commandWithLowestDiff)