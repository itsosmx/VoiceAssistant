from youtube import YoutubeSearching
import webbrowser
import subprocess
import datetime
import asyncio
import wikipedia
import pygame.mixer
pygame.mixer.init()

# Matching user input with keys and return action
def Talking(App, respone, RecognizeVoice):
  userName = open('saved.txt')
  userName = userName.read()
  
# while True:
  if not userName:
    respone('Hello Sir , first Can you tell me your name ?')
    voiceText = RecognizeVoice()
    userName = open('saved.txt', 'r')
    userName.write(voiceText)
  # else: return Talking(App, respone, RecognizeVoice)

  respone(f"Hello, {userName} How can i help you ?")
  voiceText = RecognizeVoice()
  Date = datetime.datetime.now()
  
  # Mathing the voice text key that run the needed function
  def matching(key):
    if key in voiceText:
      return True;
    else: return False
        
  if matching('stop listening') or matching('go sleep'):
    return;
  
  elif matching('date'):
    Date = Date.strftime("%x")
    respone(f'Date is {Date}')
  
  elif matching('my name'):
    respone(f'What do you mean?, you are definitely the boss, Hello {userName}.')
  
  elif matching('day'):
    Date = Date.strftime("%A")
    respone(f'the day is {Date}')
  
  elif matching('time'):
    Date = Date.strftime("%I:%M %p")
    respone(f'the time is {Date}')
  
  elif matching('your name'):
    respone('I\'m the boss hahahahahahahahhhahahahahahah')
  
  elif matching('change name'):
    userName = voiceText.split(' ').pop()
    respone(f'Change username to {userName}')
  
  elif matching('created'):
    respone('you don\'t know, i don\'t know either, i heard someone called him Osama, what a name')
  
  elif matching('google'):
    respone('opening google chrome')
    subprocess.Popen(['C:\Program Files\Google\Chrome\Application\\chrome.exe', '-new-tab'])
  
  elif matching('play'):
    try:
      voiceText = voiceText.replace('play', '')
      respone(f'Playing your music')
      source = asyncio.run(YoutubeSearching(voiceText))
      pygame.mixer.music.stop()
      pygame.mixer.music.load(source)
      pygame.mixer.music.play()
      # os.startfile(source) #Playing in the windows player
    except: respone('Please check your internet connection.')
  elif matching('where is'):
    location = voiceText.replace('where is', '')
    respone(f'Here is the location for {location}')
    webbrowser.open(f'https://google.nl/maps/place/{location}')
  elif matching('stop'):
    respone('Stopping your music')
    pygame.mixer.music.stop()
  
  elif matching('project'):
    respone('It\'s a simple GUI app for Computer language 2 developed by Osama Hussein, Under the supervision of Dr. Ali , I\'m a voice assistant, or you can called me intelligent personal assistant, all my functionality  based on natural language speech recognition.')
    respone('For more information about me, take a look here')
    webbrowser.open_new_tab('https://en.wikipedia.org/wiki/Virtual_assistant')

  elif matching('search'):
    voiceText = voiceText.replace('search about', '')
    voiceText = voiceText.replace('search for', '')
    voiceText = voiceText.replace('search to', '')
    voiceText = voiceText.replace('search', '')
    webbrowser.open_new_tab(f'https://www.google.com/search?q={voiceText}')
  
  elif matching('say'):
    voiceText = voiceText.replace('say', '')
    respone(voiceText)

  elif matching('destroy'):
    respone('I will take a nap. bye')
    App.get_running_app().stop()

  elif matching('wiki'):
    try:
      name = voiceText.replace('wiki for', '')
      data = wikipedia.summary(name, sentences=1)
      if data: respone(data)
      else: respone('Sorry, No data found.')
    except: respone('Please check your internet connection.')
  
  else:
    respone('Sorry, i can\'t understand you.')
    Talking(App, respone, RecognizeVoice)
    # return 
  
  # except Exception as e:
  #   print(e)
  #   # Run if something gose wrong or the voice not detected
  #   return respone('Sorry, i can\'t understand you.')
  #   # Talking()