# TextToAMLO

AMLO voice cloning (Dataset only). This repo has utility programs to help create a LJSpeech-like dataset for different Deep Learning Text-to-Speech programs. 

## Installation
- FFmpeg (easier to install in a Linux-based OS like Ubuntu) is necessary to convert audio files
- Use the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
apt-get install ffmpeg -y # Dependency needed to convert .mp3 files to .wav
pip install --upgrade pip
pip install -r requirements.tx
```

## Step 1: Web Crawler
- This program crawls https://lopezobrador.org.mx/secciones/comunicados/ and tries to find .mp3 audio where only AMLO voice is present (Excluding "mañaneras" where there are multiple speakers).
- Downloads audio into a local directory
- Converts .mp3 file to .wav
- Downsamples to 16kHz and saves it as mono-channel

### Note: Crawling 50 pages takes ~1 hour. File server may have security features that prevent you from downloading audio files or crawl pages
```bash
python spiderbot.py
```

### Before proceeding, some manual work is needed (you need to listen to each downloaded audio file). 
- Exclude audio files which contain multiple speakers (files larger than 70MB usually are conferences with multiple speakers. Get rid of those)
- Exclude files that have lots of noise
- Make sure you only have audio where AMLO speaks clearly
- Effective audio usually lasts no more than 30 minutes

## Step 2: Speech-to-text using GCP
This program attempts to use Google Cloud Speech-to-text API, to extract text transcripts and useful metadata (start_time, end_time) from previously downloaded audio
- To run this program, first you have to set GCP Speech-to-text API and storage bucket services. Download credentials
  - Login or create an account in GCP. Start here: console.cloud.google.com
  - Create a storage bucket and name it amlo_audio_bucket or whatever
  - Create a Speech-to-Text API service 
  - Download your GCP credentials JSON file
  - Save it in the current directory as speech_credentials.json or whatever
  - Specify bucket name as first argument for speech_recognition.py

- This program uploads local audio files to the specified GCP bucket
- Analyzes each audio using Speech-to-text API
- Retrieves transcripts and metadata and saves them in separate files

#### Specify bucket name as the first parameter for speech_recognition.py
### Note: Might take several HOURS to run

```bash
export GOOGLE_APPLICATION_CREDENTIALS=./speech_credentials.json
python speech_recognition.py amlo_audio_bucket
```

## Step 3: Audio Cropper
Using previously generated metadata, this program:

- Crops all .wav files to short length sentences and saves them in /wavs directory
- Saves its corresponding transcript in metadata.csv
```bash
python crop_audio.py
```

### After this step, you would have successfully created a LJSpeech-like dataset to train a Text-to-Speech model
## Training using Mozilla/TTS
I've created a notebook where you can initiate a training run using Mozilla/TTS: Text-to-Speech, more specifically Coqui-AI/TTS. See https://github.com/coqui-ai/TTS

### Notebook can be found here: https://gist.github.com/markzuckerbergas/d03c8cf58a4281ba22fee6ce06234795
#### You need a CUDA enabled Graphics Card with lots of memory (> 8GB)
- This repo has a config.json file with default parameters for a [Tacotron2](https://github.com/NVIDIA/tacotron2) training run
- It is necessary to update parameters accordingly to your dataset
