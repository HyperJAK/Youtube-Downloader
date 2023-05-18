import youtube_dl
import urllib.request
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import configparser
import YoutubeAPI
from YoutubeAPI import YoutubeAPI #From (filename) import (class name)

#Global variables:
download_path = ''
threads = ''
playlist_downloads = ''
audio_format = ''
server_loc = ''
api_key = ''
download_type = ''

     
     
def set_server_location(new_location):
   config_file = 'app_config.ini'

   # create ConfigParser object to read/write configuration file
   config_parser = configparser.ConfigParser()
   
   if os.path.exists(config_file):
      config_parser.read(config_file)
   
      # Modify the value
   config_parser.set('Settings', 'server_location', new_location)

   # Write the changes back to the file
   with open('app_config.ini', 'w') as config_file:
      config_parser.write(config_file)

def set_playlist_max_downloads(new_max):
   config_file = 'app_config.ini'

   # create ConfigParser object to read/write configuration file
   config_parser = configparser.ConfigParser()
   
   if os.path.exists(config_file):
      config_parser.read(config_file)
   
      # Modify the value
   config_parser.set('Settings', 'playlist', new_max)

   # Write the changes back to the file
   with open('app_config.ini', 'w') as config_file:
      config_parser.write(config_file)

def set_audio_format(new_format):
   config_file = 'app_config.ini'

   # create ConfigParser object to read/write configuration file
   config_parser = configparser.ConfigParser()
   
   if os.path.exists(config_file):
      config_parser.read(config_file)
   
      # Modify the value
   config_parser.set('Settings', 'audio_format', new_format)

   # Write the changes back to the file
   with open('app_config.ini', 'w') as config_file:
      config_parser.write(config_file)

def set_threads(new_threads):
   config_file = 'app_config.ini'

   # create ConfigParser object to read/write configuration file
   config_parser = configparser.ConfigParser()
   
   if os.path.exists(config_file):
      config_parser.read(config_file)
   
      # Modify the value
   config_parser.set('Settings', 'threads', new_threads)

   # Write the changes back to the file
   with open('app_config.ini', 'w') as config_file:
      config_parser.write(config_file)

def set_path(new_path):
   config_file = 'app_config.ini'

   # create ConfigParser object to read/write configuration file
   config_parser = configparser.ConfigParser()
   
   if os.path.exists(config_file):
      config_parser.read(config_file)
   
      # Modify the value
   config_parser.set('Settings', 'path', new_path)

   # Write the changes back to the file
   with open('app_config.ini', 'w') as config_file:
      config_parser.write(config_file)
   

def choose_local_path():
        local_path = filedialog.askdirectory()
        
        return local_path
         

def get_user_specified_path(config):
   # add the Settings section to the configuration file if it doesn't exist
   if 'Settings' not in config:
    config.add_section('Settings')

   # get the saved path from the configuration file, or prompt the user to choose a new path
   if 'path' in config['Settings'] and len(config['Settings']['path']) > 3:
      path = config['Settings']['path']
   else:
      path = choose_local_path()
      set_path(path)
   
   
   return path


def get_threads(config):

   return config['Settings']['threads']

def get_server_location(config):

   return config['Settings']['server_location']

def get_playlist_max_downloads(config):

   return config['Settings']['playlist']

def get_audio_format(config):

   return config['Settings']['audio_format']

def get_api_key():
   api_file = 'api_key.ini'

   # create ConfigParser object to read/write configuration file
   api_parser = configparser.ConfigParser()

   # check if the configuration file exists and read it if it does
   if os.path.exists(api_file):
      api_parser.read(api_file)

   return api_parser['api']['key']

def get_download_type(config):
   return config['Settings']['download_type']



def get_all_configs():
   config_file = 'app_config.ini'

   # create ConfigParser object to read/write configuration file
   config_parser = configparser.ConfigParser()

   # check if the configuration file exists and read it if it does
   if os.path.exists(config_file):
      config_parser.read(config_file)
   else:
      config_parser['Settings'] = {'path': '',
                              'threads': '5',
                              'audio_format': 'm4a',
                              'video_format': 'mp4',
                              'playlist': '10',
                              'server_location': 'FR',
                              'download_type': 'audio'}
      
      config_parser.write(open("app_config.ini","w"))
      
   global download_path, threads, playlist_downloads, audio_format, server_loc, api_key, download_type
      
   download_path = get_user_specified_path(config_parser)
   threads = get_threads(config_parser)
   playlist_downloads = get_playlist_max_downloads(config_parser)
   audio_format = get_audio_format(config_parser)
   server_loc = get_server_location(config_parser)
   api_key = get_api_key()
   download_type = get_download_type(config_parser)
   
   return True


def show_window():
   pass 



def scanpath_length(path):
   counter = 0
   
   
   for path in os.scandir(path): 
      if path.is_file():
         counter += 1
               
   return counter



def main():     
   #Get playlist name and name the new folder that the playlist will be put in as that name 
        #TO DOWNLOAD IMP 
       # https://www.youtube.com/watch?v=tnM2-fg1ujQ&list=RDtnM2-fg1ujQ&start_radio=1

   vid_url = 'https://youtu.be/hRok6zPZKMA'
   is_playlist = False
   
   try:
      #This gets all settings from config file and stores them in the global variables
      get_all_configs()
      quality = "320"
   except Exception:
      print("Error downloading")
      #download_path = os.path.join(os.path.expanduser('~'), 'Downloads') #Default is to Downloads folder
      
      
   #Creating an object of the YoutubeAPI class
   youtube_class = YoutubeAPI(api_key)
#Checks if the link is of a playlist or not
   try:
      playlist_id = youtube_class.get_playList_id(vid_url)
      
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
         'outtmpl': download_path + f'/{str(scanpath_length(download_path) + 1)}-%(title)s.%(ext)s', #Download path
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
         'outtmpl': download_path + '/' + str(scanpath_length(download_path) + 1) +'-%(title)s.%(ext)s', #Download path
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
         'outtmpl': download_path + '/' + str(scanpath_length(download_path) + 1) +'-%(title)s.%(ext)s', # Download path
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
         
         youtube_class.get_video_length(vid_url)

         #ydl.download([vid_url])
   

      
         
      

def clear_program_cache():
   ydl_opts = {
      'rm_cache_dir': True
   }

   ydl = youtube_dl.YoutubeDL(ydl_opts)
   ydl.cache.remove()
      





#if file name is called main or contails main i think
if __name__ == "__main__":
    main()