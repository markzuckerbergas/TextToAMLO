from pydub import AudioSegment
import os

# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage

audio_path = "conference_audio"
audio_list = os.listdir(audio_path)
audio_count = 0

if not os.path.exists('wavs'):
    os.makedirs('wavs')

with open("metadata.csv", 'w') as metadata:
    for audio in audio_list:
        with open("conference_audio_metadata/"+audio+".csv", 'r') as conference_metadata: 
            metadata_lines = conference_metadata.readlines()
            print("Croppping audio file:", audio, '\n')

            audio_src = "conference_audio/" + audio                    
            audio_segment = AudioSegment.from_wav(audio_src)
            audio_seconds = audio_segment.duration_seconds    

            print("Seconds in audio", audio_seconds)        

            for line in metadata_lines:
                data = line.split("|")
                print("Cropping sector and saving in file -->", str(audio_count)+".wav")
                extract = audio_segment[float(data[1])*1000:(float(data[2])+1)*1000] # Milliseconds
                extract.export('wavs/'+str(audio_count)+'.wav', format="wav")

                # Formatting file in LJSpeech format                
                metadata.write(str(audio_count)+'|'+data[0]+'|'+data[0].lower()+'\n')
                print("Sector text saved in metadata.csv")                
        
                audio_count += 1

        print()