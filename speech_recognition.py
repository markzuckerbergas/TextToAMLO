import os
import sys

# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage

audio_path = "conference_audio"
audio_list = os.listdir(audio_path)
storage_client = storage.Client()
bucket = storage_client.get_bucket(sys.argv[1])

print("Uploading files to GCloud")
for audio in audio_list:
    if ".wav" not in audio:
        continue
    blob = bucket.blob(audio)
    blob.upload_from_filename(audio_path+'/'+audio)
    print("Uploaded to GCloud", audio)

# Speech to text
# Instantiates a speech client
client = speech.SpeechClient()

config = speech.RecognitionConfig(    
    sample_rate_hertz=16000,
    language_code="es-MX",    
    enable_word_time_offsets=True         
)

if not os.path.exists('conference_audio_metadata'):
    os.makedirs('conference_audio_metadata')


for audio in audio_list:
    if ".wav" not in audio:
        continue
    with open("conference_audio_metadata/"+audio+".csv", 'w') as metadata:
        print("Analyzing audio file:", audio, '\n')                
        gcs_uri = "gs://"+sys.argv[1]+"/" + audio
        recognition_audio = speech.RecognitionAudio(uri=gcs_uri)
        operation = client.long_running_recognize(config=config, audio=recognition_audio)

        print("Waiting for operation to complete...")
        result = operation.result()        

        for result in result.results:
            alternative = result.alternatives[0]
            print("Transcript: {}".format(alternative.transcript))
            print("Confidence: {}".format(alternative.confidence))

            sector_limit = 10 # Seconds            
            sector_transcript = ""
            start_time = alternative.words[0].start_time.total_seconds()

            for index, word_info in enumerate(alternative.words):
                if index == len(alternative.words)-1:
                    sector_transcript += word_info.word
                    metadata.write(sector_transcript + "|"+str(start_time)+"|"+str(word_info.end_time.total_seconds())+"\n")
                    break

                if (word_info.start_time.total_seconds() > start_time+sector_limit):
                    sector_transcript += word_info.word
                    metadata.write(sector_transcript + "|"+str(start_time)+"|"+str(word_info.end_time.total_seconds())+"\n")
                    sector_transcript = ""
                    start_time = word_info.end_time.total_seconds()
                    sector_limit += 10
                    continue
                    
                sector_transcript += word_info.word + " "                                

