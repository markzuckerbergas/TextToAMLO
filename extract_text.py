from pydub import AudioSegment
import speech_recognition as sr
import os

r = sr.Recognizer()

audio_path = "conference_audio"
audio_list = os.listdir("conference_audio")
audio_count = 0

if not os.path.exists('wavs'):
    os.makedirs('wavs')

with open("metadata.csv", 'w') as metadata:
    for audio in audio_list:
        print("Analyzing audio file:", audio)        
        audio_src = audio_path + '/' + audio

        audio_file = sr.AudioFile(audio_src)

        audio_segment = AudioSegment.from_wav(audio_src)
        audio_seconds = audio_segment.duration_seconds    
        print("Seconds in audio", audio_seconds)
        
        sector = 10

        with audio_file as source:
            

            while sector < audio_seconds:            
                
                try:
                    audio = r.record(source, duration=10)
                    recognized_audio = r.recognize_google(audio, language="es-MX")
                    print("Recognized audio:", recognized_audio)

                    print("Cropping sector and saving in file -->", str(audio_count)+".wav")
                    extract = audio_segment[(sector-10)*1000:sector*1000] # Milliseconds
                    extract.export('wavs/'+str(audio_count)+'.wav', format="wav")

                    # Formatting file in LJSpeech format                
                    metadata.write(str(audio_count)+'|'+recognized_audio+'|'+recognized_audio.lower()+'\n')
                    print("Sector text saved in metadata.csv")                

                    sector += 10
                    audio_count += 1                

                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))                



