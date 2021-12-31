from asyncio.windows_events import NULL
import speech_recognition as speechRec
import time
import pyttsx3
import threading
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import mainthread
from matching import Talking
recognizer = speechRec.Recognizer();
AI = pyttsx3.init()

# Change AI Voice
AIvoices = AI.getProperty('voices')
voices = {
  'male':  AIvoices[0].id,
  'female': AIvoices[1].id
}

AI.setProperty('voice', voices.get('female'))


# Text to speech
def respone(message):
  AI.say(message)
  AI.runAndWait()
  


# Open the mic and start recognize the user voice
def RecognizeVoice():
  try:
    with speechRec.Microphone() as sound:
      # clientId = "Rpg6hOM-Uk86JyKeXwOAeA=="
      # clientKey = "Trt3vwMESEmDFkfwP6uConk_2fNYKnWvywxsvosPl8-xM-WuNDy2Q2XQcGAMhW0obPM0Hw9GDdLPMefaMLSsbQ=="
      voice = recognizer.listen(sound)
      voiceText = recognizer.recognize_google(voice, language="en-US") #online 
      # voiceText = recognizer.recognize_sphinx(voice, language="en-US") #offline
      # voiceText = recognizer.recognize_houndify(voice,
      # client_id=clientId, client_key=clientKey) #offline
      
      voiceText = voiceText.lower()
      print(f'Input : {voiceText}')
      return voiceText
  except speechRec.UnknownValueError as e:
    print(f'RecognizeVoice: {e}')
    # respone('Sorry, I didn\'t recognize your voice.')
    # pass
    # respone('listening.....')
  except speechRec.RequestError as e:
    print(f'RecognizeVoice: {e}')
    respone('Sorry, something went wrong.')




class PyWidget(Widget):
  stop = threading.Event()
  
  def second_thread(self): 
    self.ids.mic.source = 'assets/open2.png'
    self.ids.mic.reload()
    # time.sleep(2)
    threading.Thread(target=self.start_listening).start()

    
  @mainthread
  def start_listening(self):
    while True:
      try:
        time.sleep(1)
        print('Listening.......')
        voiceText = RecognizeVoice()
        time.sleep(1)
        if 'hello' in voiceText and Talking(App, respone, RecognizeVoice):
          return
        time.sleep(1)
      except Exception as e:
        print(f'start_listening: {e}')
    




class AwesomeAssistant(App):
  def on_stop(self):
    self.root.stop.set()
    
  def build(self):
    return PyWidget()

if __name__ == "__main__":
  AwesomeAssistant().run()