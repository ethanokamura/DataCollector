# Data Collector
The aim of this program is to parse data from a wide range of data sets.

In the current implementation, we have the following workflow:
1. MP3 -> Text
2. Text -> JSON

## Audio to Text
To convert the audio to text, we are using AssemblyAI due to its generous free tier as well as its fast and effective ability to transcribe audio files.

## Text to JSON
To retrieve the specific data we want from the given text files, we are feeding the text files with a prompt into Google's Gemini API.

## Getting Started
To run this on your own, you will need to install the following packages:
```sh
pip install assemblyai
pip install -q -U google-genai
```
