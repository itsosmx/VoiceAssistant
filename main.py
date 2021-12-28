from asyncio.windows_events import NULL
import speech_recognition as speechRec
import pyttsx3
import datetime
import subprocess
import pygame.mixer
import asyncio
import webbrowser
import time
import threading
import os
import wikipedia
# import moviepy.editor as mp
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock, mainthread
from os import walk
from youtube import YoutubeSearching
# os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"


recognizer = speechRec.Recognizer();

pygame.mixer.init()
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
      voice = recognizer.listen(sound, phrase_time_limit=5)
      voiceText = recognizer.recognize_google(voice) #online 
      # voiceText = recognizer.recognize_sphinx(voice, language="en-US") #offline
      # voiceText = recognizer.recognize_houndify() #offline
      voiceText = voiceText.lower()
      print(f'Input : {voiceText}')
      return voiceText
  except speechRec.UnknownValueError:
    respone('Sorry, I didn\'t recognize your voice.')
    # pass
    # respone('listening.....')
  except speechRec.RequestError:
    respone('Sorry, something went wrong.')

userName = NULL

# Matching user input with keys and return action
def Talking(self):
  try:
    global userName 
    if not userName:
      respone('Hello, first Can you tell me your name?')
      voiceText = RecognizeVoice()
      userName = voiceText
    else: return Talking(self)
      
    respone(f"Hello, {userName} How can i help you")
    voiceText = RecognizeVoice()
    Date = datetime.datetime.now()
    
    # Mathing the voice text key that run the needed function
    def matching(key):
      if key in voiceText:
        return True;
      else: return False
    
    self.ids.text_id.test = voiceText
    if matching('date'):
      Date = Date.strftime("%x")
      return respone(f'Date is {Date}')
    
    elif matching('my name'):
      respone(f'If you know this key, you are definitely the boss, Hello {userName}.')
    
    elif matching('time'):
      Date = Date.strftime("%I:%M %p")
      return respone(f'the time is {Date}')
    
    elif matching('your name'):
      return respone('I\'m the boss hahahahahahahahhhahahahahahah')
    
    elif matching('rename'):
      userName = voiceText.split(' ').pop()
      return respone(f'Change username to {userName}')
    
    elif matching('created'):
      return respone('I don\'t know, someome called Osama. do you know him?!')
    
    elif matching('google'):
      respone('opening google chrome')
      return subprocess.Popen(['C:\Program Files\Google\Chrome\Application\\chrome.exe', '-new-tab'])
    
    elif matching('play'):
      try:
        voiceText = voiceText.replace('play', '')
        respone(f'Playing your music')
        source = asyncio.run(YoutubeSearching(voiceText))
        pygame.mixer.music.stop()
        pygame.mixer.music.load(source)
        return pygame.mixer.music.play()
        # os.startfile(source) #Playing in the windows player
      except: respone('Please check your internet connection.')
      
    elif matching('stop'):
      respone('Stopping your music')
      return pygame.mixer.music.stop()
    
    elif matching('project'):
      return respone('It\'s a simple GUI app for Computer language 2, I\'m AI that can do what ever you want, but iam waiting my lazy Boss to develop me more than this.')
    
    elif matching('search'):
      voiceText = voiceText.replace('search', '')
      return webbrowser.open_new_tab(f'https://www.google.com/search?q={voiceText}')
    
    elif matching('say'):
      voiceText = voiceText.replace('say', '')
      return respone(voiceText)
    
    # elif matching('+'):
    #   result = 0
    #   for num in voiceText.split(' '):
    #     if num.isdigit():
    #       result += num
    #   respone(f'The result is {result}')
      
    elif matching('destroy'):
      respone('I will take a nap. bye')
      App.get_running_app().stop()
      return True
  
    elif matching('wiki'):
      try:
        name = voiceText.replace('wiki', '')
        data = wikipedia.summary(name, sentences=1)
        if data: return respone(data)
        else: return respone('Sorry, No data found.')
      except: respone('Please check your internet connection.')
    
    else: return respone('Sorry, i can\'t understand you.') # Run if the above function not match
  
  except:
    # Run if something gose wrong or the voice not detected
    respone('Sorry, i can\'t understand you.')
    return Talking(self)

def Starting(self):
  while True:
    try:
      print('listening.......')
      voiceText = RecognizeVoice()
      if 'hello' in voiceText and Talking(self):
        return
    except:
      print('something wrong in the Strating Func.')
    
class PyWidget(Widget):
  stop = threading.Event()
  
  def start_second_thread(self):
    threading.Thread(target=self.second_thread,  args=[self]).start()

  def second_thread(self):
    threading.Thread(target=Starting, args=[self]).start()
    self.ids.mic.source = 'assets/open2.png'
    time.sleep(2)
    self.ids.mic.reload()
    time.sleep(2)
    
    
  # def second_thread(self, lable_text):
  #   self.ids.mic.source = 'assets/open2.png'
  #   Clock.schedule_once(self.Starting(self), 0)
  #   time.sleep(5)
  #   l_text = str(int(lable_text) * 3000)
    
  # def release(self):
  #   self.ids.mic.source = 'assets/normal2.png'
  # def callback(self):
  #   self.ids.mic.source = 'assets/open2.png'
  #   self.ids.mic.reload()
  #   Clock.schedule_once(lambda dt: Starting(self))


class AwesomeAssistant(App):
  def on_stop(self):
    self.root.stop.set()
  def build(self):
    return PyWidget()
    # setup window 
    # Window.clearcolor = (1, 1, 1, 1)
    # Config.set('graphics', 'resizable', True)
    # self.icon = "windowIcon.png"
    # self.window = GridLayout(cols = 1, row_force_default=True, row_default_height=100)
    # self.window.cols = 1
    # self.window.size_hint = (0.6, 0.2)
    # self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
    # self.Title = Label(text="BOSS ASSISTANT", font_size=50)
    # self.window.add_widget(self.Title)
    
    # self.button = ToggleButton(text="Talk with me", background_color='#ffd43b', background_normal="",
    #                          bold=True, size_hint=(1, 1), color="#00000")
    # self.button.bind(on_press=self.callback)
    # self.window.add_widget(self.button)
    # self.button = Button(text="Click", background_normal='mic.png', width = 100 , size_hint_x= None, pos_hint = {"x":0.5, "y":0.5})
    # self.window.add_widget(self.button)
    # self.mic = Image(source='mic.png', size=(5, 5))
    # self.mic.bind(on_press=self.callback)
    # self.window.add_widget(self.mic)

    # self.description = Label(text="")
    # return self.window
    
if __name__ == "__main__":
  AwesomeAssistant().run()