from pydub import AudioSegment
import os
from num2words import num2words


audio_path = "conference_audio"
audio_list = os.listdir(audio_path)
audio_count = 0

if not os.path.exists('wavs'):
    os.makedirs('wavs')

with open("metadata.csv", 'w') as metadata:
    for audio in audio_list:
        if ".wav" not in audio:
            continue
        with open("conference_audio_metadata/"+audio+".csv", 'r') as conference_metadata: 
            metadata_lines = conference_metadata.readlines()
            print("Croppping audio file:", audio, '\n')

            audio_src = "conference_audio/" + audio                    
            audio_segment = AudioSegment.from_wav(audio_src)
            audio_seconds = audio_segment.duration_seconds    

            print("Seconds in audio", audio_seconds)        

            for line in metadata_lines:
                data = line.split("|")
                text = data[0]
                numbers_in_string = [int(s) for s in data[0].split() if s.isdigit()]

                if len(numbers_in_string) > 0:                    
                    for number in numbers_in_string:
                        text = text.replace(str(number), num2words(number, lang='es'))                    


                
                print("Cropping sector and saving in file -->", str(audio_count)+".wav")
                extract = audio_segment[float(data[1])*1000:(float(data[2])+1)*1000] # Milliseconds
                extract.export('wavs/'+str(audio_count)+'.wav', format="wav")

                # Formatting file in LJSpeech format                
                metadata.write(str(audio_count)+'|'+text+'|'+text.lower()+'\n')
                print("Sector text saved in metadata.csv")                
        
                audio_count += 1

        print()