# Information Processor
This application allows us to process large quantities of diverse data and convert them into a uniform, easy to use, format.

---

## Collecting Youtube Videos
To download YouTube videos, I decided to use `pytube` which is a "genuine, lightweight, dependency-free Python library" according to the docs.

---

## 1. Convert Video to Audio
To convert video files into a native audio format, we are using a combination of the `moviepy` and `imageio` libraries.

We use `moviepy` for the conversions themselves and `imageio` to provide a simple and reliable ffmpeg wrapper for working with video files.

After the videos have been converted, we place the new audio files inside our audio file directory. Here, they wait to be transcribed.

---

## 2. Transcribe Audio to Text
Once we have our audio files prepared, we now need to convert the audio to text

Using AssemblyAI, we are able to use their generous API to transcribe large amounts of audio files.

For the purpose of this application, we want all of our data in a text format.

Once converted, the text files are placed in the text file directory to await analysis.

---

## 3. Convert HTML to Text (Optional)
To allow us to intake as much data as possible, we have set up conversion of HTML files into plain text. This allows us to use very simple webscraping techniques to gather large amounts of data from the web.

Using the linux command `html2text`, we are able to easily convert the inner HTML of these files to plain text.

Once converted, the text files are placed in the text file directory to await analysis.

---

## 4. Analyze and Format Data (Text Files)

---

## Installation

Ensure you have `python` installed on your machine.

Then install the following packages:
```sh
python -m pip install git+https://github.com/pytube/pytube
pip install moviepy
pip install imageio-ffmpeg
```


