import glob, os
from src.mfcc import MFCCParser
from src.wav_analyser import Sound

def extract_mfcc(parser, location, to):
    os.chdir(location)
    files = glob.glob("*.wav")
    index = 1

    commands = dict()

    for file in files:
        command = file.rsplit(" ", -1)[0]
        if commands.get(command) is None:
            commands[command] = []
            
        soundTest = Sound(filename=file)
        mfccData = parser.toMFCC(soundTest)

        commands[command].append(mfccData)
        print("%s/%s done." % (index, len(files)))
        index += 1

    return commands

# extractMFCC("", "")

# print("slowo".rsplit(" ", -1))