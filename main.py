import os
import shutil
import assemblyai as aai
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
aai.settings.api_key = os.getenv('ASSEMBLY_AI_API_KEY')


# transcribe audio using AssemblyAI
def transcribe_audio(file, dir_path):
  print("processing: " + dir_path)
  # Transcribe the audio
  config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
  transcript = aai.Transcriber(config=config).transcribe(dir_path)
  if transcript.status == "error":
    raise RuntimeError(f"Transcription failed: {transcript.error}")
  
  # Move the file
  shutil.move(dir_path, "./audio-complete/")
  print("moved old file to ./audio-complete directory")

  # Create new path
  new_path = "./text/" + file + ".txt"

  # Write to file
  text_file = open(new_path, "x")
  text_file.write(transcript.text)
  text_file.close()
  return new_path

# parse text using Gemini
def parse_text(file, dir_path):
  print("processing: " + dir_path)
  # Open the file in read mode
  with open(dir_path, 'r') as raw_text:
      # Read the entire content of the file
      data = raw_text.read()
  slug = os.path.basename(file).split('.')[0]
  prompt = f"""Summarize the entry episode into one sentence explanation and the 5 most important bullet points.
    Using the text provided, list names of people, names of companies, fraud avoidance tips, scam avoidance tips, safety tips, tactics that scammers use, and the some important topics in the text

    I have already provided the title (this remains unchanged). I just need 'important_topics', 'names', 'companies', 'acronyms', 'fraud_tips', and 'tactics',, to be populated
 
    Use this JSON schema:
    {{
      'title': '{slug}',
      'important_topics': list[str],
      'names': list[str],
      'companies': list[str],
      'acronyms': list[str],
      'fraud_tips': list[str]
      'tactics': list[str],

    }}

    Provided text:
    {data}
    """
  response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompt,
    config={
      'response_mime_type': 'application/json',
    }
  )

  # Move the file
  shutil.move(dir_path, "./text-complete/")
  print("moved old file to ./text-complete directory")

  # Create new path
  new_path = "./parsedText/" + file + ".json"
  
  # Write to new file
  complete_file = open(new_path, "x")
  complete_file.write(response.text)
  complete_file.close()
  return new_path

# def process_audio_files(folder_path):
#   try:
#     for filename in os.listdir(folder_path):
#       file_path = os.path.join(folder_path, filename)
#       if os.path.isfile(file_path):  # Check if it's a file
#         new_path = transcribe_audio(filename, file_path)
#         print("new transcription found at " + new_path)
#   except FileNotFoundError:
#     print(f"Error: Folder not found: {folder_path}")
#   except Exception as e:
#     print(f"An error occurred: {e}")

def process_text_files(folder_path):
  try:
    for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      if os.path.isfile(file_path):  # Check if it's a file
        new_path = parse_text(filename, file_path)
        print("new JSON object found at " + new_path)
  except FileNotFoundError:
    print(f"Error: Folder not found: {folder_path}")
  except Exception as e:
    print(f"An error occurred: {e}")

def build_dataset(folder_path):
  try:
    for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      if os.path.isfile(file_path):
        file = os.path.basename(filename).split('.')[0]
        new_path = transcribe_audio(file, file_path)
        print("new text @ " + new_path)
        if os.path.isfile(new_path):
          new_path = parse_text(file, new_path)
          print("new JSON @ " + new_path)
  except FileNotFoundError:
    print(f"Error: Folder not found: {folder_path}")
  except Exception as e:
    print(f"An error occurred: {e}")

def build():
  # Parse Text
  build_dataset("./audio")
  # process_text_files("./text")

build()