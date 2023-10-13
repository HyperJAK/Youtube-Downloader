import sys
import youtube_dl
from tkinter import filedialog
import os
import configparser
import pyperclip

console_app = True

if console_app == False:
   sys.stdout = open(os.devnull, 'w')
   sys.stderr = open(os.devnull, 'w')

#Global variables:
vid_url = ''
download_path = ''
threads = ''
playlist_downloads = ''
audio_format = ''
server_loc = ''
api_key = ''
download_type = ''
download_thumbnail = ''


def set_download_thumbnail(bool_value):
   config_file = 'app_config.ini'

   # create ConfigParser object to read/write configuration file
   config_parser = configparser.ConfigParser()
   
   if os.path.exists(config_file):
      config_parser.read(config_file)
   
      # Modify the value
   config_parser.set('Settings', 'download_thumbnail', bool_value)

   # Write the changes back to the file
   with open('app_config.ini', 'w') as config_file:
      config_parser.write(config_file)
      
     
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

def get_thumbnail(config):
   return config['Settings']['download_thumbnail']


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
   if os.path.exists(os.getcwd() + '/' + config_file):
      config_parser.read(config_file)
   else:
      config_parser['Settings'] = {'path': '',
                              'threads': '4',
                              'audio_format': 'm4a',
                              'video_format': 'mp4',
                              'playlist': '10',
                              'server_location': 'FR',
                              'download_type': 'audio',
                              'download_thumbnail': 'false'}
      
      config_parser.write(open(os.getcwd() +"/app_config.ini","w"))
      
   global download_path, threads, playlist_downloads, audio_format, server_loc, api_key, download_type, download_thumbnail
      
   download_path = get_user_specified_path(config_parser)
   threads = get_threads(config_parser)
   playlist_downloads = get_playlist_max_downloads(config_parser)
   audio_format = get_audio_format(config_parser)
   server_loc = get_server_location(config_parser)
   #api_key = get_api_key()
   download_type = get_download_type(config_parser)
   download_thumbnail = get_thumbnail(config_parser)
   
   return True


def show_window():
   pass 



def scanpath_length(path):
   counter = 0
   
   
   for path in os.scandir(path): 
      if path.is_file():
         counter += 1
               
   return counter


def paste_url():
   global vid_url
   vid_url = pyperclip.paste()
   run_downloader()
   
   
   
   #Gets video / playlist information
   
def get_video_info(vid_url):
   with youtube_dl.YoutubeDL() as ydl:
      info = ydl.extract_info(vid_url, download=False) #Gets all video info in a dict() format
      
      temp_is_playlist = is_playlist(info)
      temp_playlist_title = ''
      
      if temp_is_playlist:
         temp_playlist_title = get_playlist_title(info)
   
   return temp_is_playlist, temp_playlist_title



def get_playlist_title(ydl_extracted_info):
   try:
      title = ydl_extracted_info['title']
      title = title.split(' ')

      new_title = ''
      new_title += title[0]

      if len(title) > 2:
         for i in range(len(title) - (int)(len(title) - 3)):
            new_title += (title[i + 1])
         
      return new_title
   
   except youtube_dl.DownloadError:
      if console_app:
         print("Couldnt find title")
         
         
   

def is_playlist(ydl_extracted_info):
      try:
         if 'entries' in ydl_extracted_info:
               # Playlist
               playlist_id = ydl_extracted_info['id']
               if console_app:
                  print(f"This is a playlist. Playlist ID: {playlist_id}")
               return True
         else:
               # Single video
               video_id = ydl_extracted_info['id']
               if console_app:
                  print(f"This is a single video. Video ID: {video_id}")
               return False
      except youtube_dl.DownloadError:
         if console_app:
            print("Invalid URL or unable to extract information.")




def progress_hook(hook):
   if console_app:
      if hook['status'] == 'downloading':
         percent = hook['_percent_str']
         speed = hook['_speed_str']
         eta = hook['_eta_str']
         progress_message = f"Downloading: {percent} complete | Speed: {speed} | ETA: {eta}"
         sys.stdout.write('\r' + progress_message)
         sys.stdout.flush()
      elif hook['status'] == 'finished':
         print("\nDownload finished! Starting to process...")
            


def run_downloader():     
   #Get playlist name and name the new folder that the playlist will be put in as that name 
        #TO DOWNLOAD IMP 
       # https://www.youtube.com/watch?v=tnM2-fg1ujQ&list=RDtnM2-fg1ujQ&start_radio=1
       # https://youtu.be/oi6sOSTFrxc
   quality = "320"
  
#Checks if the link is of a playlist or not

   is_playlist, playlist_title = get_video_info(vid_url)
   
   if is_playlist:
      global download_path
      
      if not os.path.exists(download_path + "/" + playlist_title):
         os.chdir(download_path)
         os.mkdir(playlist_title)
         
         
      download_path = download_path + "/" + playlist_title
      
      #using the global value of download_thumbnail
   global download_thumbnail
   #sets the thumbnail download boolean value based on the text read from the config
   if download_thumbnail == "false":
      download_thumbnail = False
      
   else:
      download_thumbnail = True
   

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
         'outtmpl': download_path + '/%(playlist_index)s-%(title)s.%(ext)s', #Download path
         'quiet': True,
         'no_mtime': True,
         'forcetitle': False,
         'verbose': False,
         'forcethumbnail': False,
         'keepvideo': False,
         #'restrictfilenames': True,  # only use safe characters in output filename
         'noplaylist': False,  # Download playlists
         'playlist_items':'1-'+playlist_downloads,
         'n_threads': threads,
         'geo_bypass_country': server_loc,
         'ignoreerrors': True,
         'progress_hooks': [progress_hook]

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
         'quiet': True,
         'no_mtime': True,
         'forcetitle': False,
         'verbose': False,
         'forcethumbnail': download_thumbnail,
         'keepvideo': False,
         #'restrictfilenames': True,  # only use safe characters in output filename
         'noplaylist': True,  # Download playlists
         'n_threads': threads,
         'ignoreerrors': True,
         'geo_bypass_country': server_loc,
         'progress_hooks': [progress_hook],
         'writethumbnail': True

      }
   
    #In this case thumbnails are downloaded using youtubeapi
   elif download_type == 'video' and is_playlist == True:
      ydl_opts = {
         'format': 'bestvideo[height<=1080]+bestaudio/best[abr>128]',
         'outtmpl': download_path + '/%(playlist_index)s-%(title)s.%(ext)s', # Download path
         'quiet': True,
         'no_mtime': True,
         'forcetitle': False,
         'verbose': False,
         'forcethumbnail': False,
         'keepvideo': True,  # Set to True to keep the video file
         'noplaylist': False,  # Download playlists
         'playlist_items': '1-' + playlist_downloads,
         'n_threads': threads,
         'ignoreerrors': True,
         'geo_bypass_country': server_loc,
         'progress_hooks': [progress_hook]
      }
      
      #In this case thumbnails are downlaoded from youtube-dl
   elif download_type == 'video' and is_playlist == False:
      ydl_opts = {
         'format': 'bestvideo[height<=1080]+bestaudio/best[abr>128]',
         'outtmpl': download_path + '/' + str(scanpath_length(download_path) + 1) +'-%(title)s.%(ext)s', # Download path
         'quiet': True,
         'no_mtime': True,
         'forcetitle': False,
         'verbose': False,
         'forcethumbnail': download_thumbnail,
         'keepvideo': True,  # Set to True to keep the video file
         'noplaylist': True,  # Download playlists
         'playlist_items': '1-' + playlist_downloads,
         'n_threads': threads,
         'ignoreerrors': True,
         'geo_bypass_country': server_loc,
         'progress_hooks': [progress_hook],
         'writethumbnail': True
      }
      

   info = dict()
   # Initialize youtube-dl
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      # Download audio-only
      
      #if is_playlist == False:
         #pass
         # specify the URL of the image
         #url = info.get('thumbnail')
         
         
         # download the image and save it to a file
         #urllib.request.urlretrieve(url, 'image2.jpg')
         
      #getting title and shorttening it
      #info = ydl.extract_info(vid_url,download=False)
      #title = info.get('title')
      

      ydl.download([vid_url])
      if console_app:
         print('Finished processing')
         
      

def clear_program_cache():
   ydl_opts = {
      'rm_cache_dir': True
   }

   ydl = youtube_dl.YoutubeDL(ydl_opts)
   ydl.cache.remove()
      





#if file name is called main or contails main i think
if __name__ == "__main__":
    run_downloader()