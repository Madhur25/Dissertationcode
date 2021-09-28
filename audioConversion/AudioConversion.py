import os
from pydub import AudioSegment

path = "C:/Users/madhu/cv-valid-dev/cv-valid-dev"
dst = "C:/Users/madhu/converted2"
#Change working directory
os.chdir(path)

audio_files = os.listdir()

# You dont need the number of files in the folder, just iterate over them directly using:
for file in audio_files:
    #spliting the file into the name and the extension
    name, ext = os.path.splitext(file)
    print(name)
    if ext == ".mp3":
        mp3_sound = AudioSegment.from_mp3(file)
       #rename them using the old name + ".wav"
        mp3_sound.export(dst+"/{0}.wav".format(name), format="wav")
        print(dst+"/{0}.wav".format(name))