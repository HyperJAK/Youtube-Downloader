import youtube_dl
import urllib.request
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import configparser
import youtubeApiLegit as yt_lg

def choose_local_path():
        local_path = filedialog.askdirectory()
        
        return local_path
     
     
def set_server_location(new_location):
   pass

def set_playlist_max_downloads(new_max):
   pass

def set_audio_format(new_format):
   pass

def set_threads(new_threads):
   pass


def get_user_specified_path(config):
   # add the Settings section to the configuration file if it doesn't exist
   if 'settings' not in config:
    config.add_section('settings')

   # get the saved path from the configuration file, or prompt the user to choose a new path
   if 'path' in config['settings'] and len(config['settings']['path']) > 3:
      path = config['settings']['path']
   else:
      path = choose_local_path()
      config['settings']['path'] = path
      with open(config, 'w') as f:
         config.write(f)
   

   
   return path


def get_threads(config):

   return config['settings']['threads']

def get_server_location(config):

   return config['settings']['server_location']

def get_playlist_max_downloads(config):

   return config['settings']['playlist']

def get_audio_format(config):

   return config['settings']['audio_format']

def get_api_key():
   api_file = 'api_key.ini'

   # create ConfigParser object to read/write configuration file
   api_parser = configparser.ConfigParser()

   # check if the configuration file exists and read it if it does
   if os.path.exists(api_file):
      api_parser.read(api_file)

   return api_parser['api']['key']

def get_download_type(config):
   return config['settings']['download_type']



def get_all_configs():
   config_file = 'config.ini'

   # create ConfigParser object to read/write configuration file
   config_parser = configparser.ConfigParser()

   # check if the configuration file exists and read it if it does
   if os.path.exists(config_file):
      config_parser.read(config_file)
      
      
   path = get_user_specified_path(config_parser)
   threads = get_threads(config_parser)
   playlist_downloads = get_playlist_max_downloads(config_parser)
   audio_format = get_audio_format(config_parser)
   server_loc = get_server_location(config_parser)
   api_key = get_api_key()
   download_type = get_download_type(config_parser)
   
   return path, threads, server_loc, playlist_downloads, audio_format, api_key, download_type



def main():      
        

   vid_url = "https://youtu.be/HLEMQgCzxd4"
   is_playlist = False
   
   try:
      #This gets all settings from config file
      download_path, threads, server_loc, playlist_downloads, audio_format, api_key, download_type = get_all_configs()
      quality = "320"
   except Exception:
      print("Error downloading")
      #download_path = os.path.join(os.path.expanduser('~'), 'Downloads') #Default is to Downloads folder
   

#Checks if the link is of a playlist or not
   try:
      playlist_id = yt_lg.get_playList_id(vid_url)
      
      if playlist_id == False:
         is_playlist = False
      else:
         is_playlist = True
      
   except Exception:
      pass
   
   #In this case thumbnails are downloaded using youtubeapi
   if download_type == 'audio' and is_playlist == True:
      # Set options for audio-only download
      ydl_opts = {
         'format': 'bestaudio/best',
         'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': quality
         }],
         'outtmpl': download_path + '/%(title)s.%(ext)s', #Download path
         'quiet': False,
         'forcetitle': True,
         'verbose': False,
         'forcethumbnail': False,
         'keepvideo': False,
         #'restrictfilenames': True,  # only use safe characters in output filename
         'noplaylist': False,  # Download playlists
         'playlist_items':'1-'+playlist_downloads,
         'n_threads': threads,
         'geo_bypass_country': server_loc

      }
   
   #In this case thumbnails are downlaoded from youtube-dl
   elif download_type == 'audio' and is_playlist == False:
      ydl_opts = {
         'format': 'bestaudio/best',
         'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': quality
         }],
         'outtmpl': download_path + '/%(title)s.%(ext)s', #Download path
         'quiet': False,
         'forcetitle': True,
         'verbose': False,
         'forcethumbnail': True,
         'keepvideo': False,
         #'restrictfilenames': True,  # only use safe characters in output filename
         'noplaylist': True,  # Download playlists
         'n_threads': threads,
         'geo_bypass_country': server_loc

      }
   
    #In this case thumbnails are downloaded using youtubeapi
   elif download_type == 'video' and is_playlist == True:
      ydl_opts = {
         'format': 'bestvideo[height<=1080]+bestaudio/best[abr>128]',
         'outtmpl': download_path + '/%(title)s.%(ext)s', # Download path
         'quiet': False,
         'forcetitle': True,
         'verbose': False,
         'forcethumbnail': False,
         'keepvideo': True,  # Set to True to keep the video file
         'noplaylist': False,  # Download playlists
         'playlist_items': '1-' + playlist_downloads,
         'n_threads': threads,
         'geo_bypass_country': server_loc
      }
      
      #In this case thumbnails are downlaoded from youtube-dl
   elif download_type == 'video' and is_playlist == False:
      ydl_opts = {
         'format': 'bestvideo[height<=1080]+bestaudio/best[abr>128]',
         'outtmpl': download_path + '/%(title)s.%(ext)s', # Download path
         'quiet': False,
         'forcetitle': True,
         'verbose': False,
         'forcethumbnail': True,
         'keepvideo': True,  # Set to True to keep the video file
         'noplaylist': True,  # Download playlists
         'playlist_items': '1-' + playlist_downloads,
         'n_threads': threads,
         'geo_bypass_country': server_loc
      }
      

   info = dict()
   # Initialize youtube-dl
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      # Download audio-only
      
      if is_playlist == False:
         info = ydl.extract_info(vid_url,download=False)
      
         # specify the URL of the image
         url = info.get('thumbnail')
         title = info.get('title')
         
         # download the image and save it to a file
         urllib.request.urlretrieve(url, 'image2.jpg')
         
         
      
      ydl.download([vid_url])
   

      
     
      
      

def clear_program_cache():
   ydl_opts = {
      'rm_cache_dir': True
   }

   ydl = youtube_dl.YoutubeDL(ydl_opts)
   ydl.cache.remove()
      





#if file name is called main or contails main i think
if __name__ == "__main__":
    main()