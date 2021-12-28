from pytube import YouTube
from youtube_search import YoutubeSearch
import moviepy.editor as mp
import os
from os import walk

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