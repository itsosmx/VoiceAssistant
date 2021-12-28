import speech_recognition as speechRec
import pyttsx3
import datetime
import subprocess
import pygame.mixer
import asyncio
import webbrowser
import os
import wikipedia
import moviepy.editor as mp

from pytube import YouTube
from youtube_search import YoutubeSearch
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from os import walk
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"


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

# Download Music from youtube and convert it to mp3
async def YoutubeSearching(query):
  try:
    result = YoutubeSearch(query, max_results=1).to_dict()
    videoId = result[0]['id']
    url = f'https://youtu.be/{videoId}'
    video = YouTube(url)
    directory  = 'player'
    filePath = f'{directory}/{videoId}.mp3'
    
    files = []
    for (dirpath, dirnames, filenames) in walk(directory):
      files.extend(filenames)
      break
    if f'{videoId}.mp3' in files:
      return filePath
    
    audio = video.streams.filter(only_audio=True).first()
    source = audio.download(directory)
    clip = mp.AudioFileClip(source).subclip(10,)
    clip.write_audiofile(filePath)
    
    
    # Delete all mp4 files
    if len(os.listdir(directory )) != 0:
      for file in os.listdir(directory):
        if file.endswith('.mp4'):
          os.remove(os.path.join(directory , file))
          
    return filePath
  except: pass

# Open the mic and start recognize the user voice
def RecognizeVoice():
  try:
    with speechRec.Microphone() as sound:
      voice = recognizer.listen(sound)
      voiceText = recognizer.recognize_google(voice)
      voiceText = voiceText.lower()
      print(f'Me : {voiceText}')
      return voiceText
  except speechRec.UnknownValueError:
    # respone('Sorry, I didn\'t recognize your voice.')
    # respone('listening.....')
    pass
  except speechRec.RequestError:
    respone('Sorry, something went wrong.')
userName = None
# Matching user input with keys and return action
def Talking(widget):
  try:
    # if not Starting():
    #   return
    # else:
    global userName 
    if not userName:
      respone('Hello, first Can you tell me your name?')
      voiceText = RecognizeVoice()
      userName = voiceText
      
    respone(f"Hello, {userName} How can i help you")
    voiceText = RecognizeVoice()
    Date = datetime.datetime.now()
    
    # Mathing the voice text key that run the needed function
    def matching(key):
      if key in voiceText:
        return True;
      else: return False
    widget.ids.text_id.text = voiceText
    # print(self.ids)
    if matching('date'):
      Date = Date.strftime("%x")
      return respone(f'Date is {Date}')
    elif matching('my name'):
      respone('If you know this key, you are definitely the boss, Hello Osama.')
    elif matching('time'):
      Date = Date.strftime("%I:%M %p")
      return respone(f'the time is {Date}')
    elif matching('your name'):
      return respone('I\'m the boss hahahahahahahahhhahahahahahah')
    elif matching('rename'):
      userName = voiceText.split(' ').pop()
      return respone('I\'m the boss hahahahahahahahhhahahahahahah')
    elif matching('created'):
      return respone('I don\'t know, someome called Osama. do you know him?!')
    elif matching('google'):
      respone('opening google chrome')
      return subprocess.Popen(['C:\Program Files\Google\Chrome\Application\\chrome.exe', '-new-tab'])
    elif matching('play'):
      try:
        voiceText = voiceText.replace('play', '')
        source = asyncio.run(YoutubeSearching(voiceText))
        respone(f'Playing, your music')
        pygame.mixer.stop()
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
    return Talking(widget)

def Starting(self):
  try:
    print("listening.....")
    voiceText = RecognizeVoice()

    if 'hello' not in voiceText:
      Starting(self)
      return False
    else: 
      x = Talking(self)
      while not x:
        Starting(self)
      return 
  except: pass
  

class PyWidget(Widget):
  def release(self):
    self.ids.mic.source = 'assets/normal2.png'
  def callback(self):
    self.ids.mic.source = 'assets/open2.png'
    self.ids.mic.reload()
    Clock.schedule_once(lambda dt: Starting(self))
    
class AwesomeAssistant(App):
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