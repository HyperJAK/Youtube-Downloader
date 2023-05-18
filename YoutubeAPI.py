import googleapiclient.discovery
from pytube import YouTube

class YoutubeAPI:
   
   def __init__(self, api_key):
      self.api_key = api_key
      api_service_name = "youtube"
      api_version = "v3"
      DEVELOPER_KEY = api_key

      self.youtube = googleapiclient.discovery.build(
         api_service_name, api_version, developerKey = DEVELOPER_KEY)
      
      
      
      
   
   def get_video_id(self, video_url):
      pass
   
   
   
   
   def is_playlist(self, playlist_url):
      string_length = len(playlist_url)
      concat_string = ''
      
      for i in range(0, string_length):  
         concat_string = playlist_url[i:i+5]

         if concat_string == 'list=':
              # concat_string = playlist_url[i+5:string_length]
              return True
               
         else:
               concat_string = ''
               if i+5 == string_length:
                  return False
      
      
  
      
      
      

   def convert_to_readable(self, secounds):
      pass
   
   
   
   def get_video_length(self, video_url):
      # Create a YouTube object
      yt = YouTube(video_url)

      # Get the duration of the video in seconds
      duration_seconds = yt.length

      # Convert the duration to a more readable format (e.g., HH:MM:SS)
      formatted_duration = str(self.convert_to_readable(duration_seconds))

      print(f"This video duration is {duration_seconds}")
    
    
    
   def get_playlist_info(self, playlist_url):
      # Specify the playlist ID
      playlist_id = self.get_playList_id(playlist_url)

   
    
   def get_playlist_id(self, playlist_url):
   
      # Retrieve the playlist items
      playlist_id = self.youtube.playlistItems().list(
         part='id',
         playlist_url=playlist_url,
      ).execute()
      
      return playlist_id
   
   
   
   
   
   def get_playlist_title(self, playlist_url):
      pass
      
   
   def get_playlist_thumbnails(self, playlist_id, max_results):

      # Retrieve the playlist items
      playlist_items = self.youtube.playlistItems().list(
         part='snippet',
         playlistId=playlist_id,
         maxResults=max_results,  # Maximum number of results per page
         order='position'
      ).execute()

      # Extract thumbnails from each video
      for item in playlist_items['items']:
         video_title = item['snippet']['title']
         
         if 'maxres' in item['snippet']['thumbnails']:
               thumbnail_url = item['snippet']['thumbnails']['maxres']['url']
         elif 'high' in item['snippet']['thumbnails']:
               thumbnail_url = item['snippet']['thumbnails']['high']['url']
         
         
         
         vid_length = int(item['contentDetails']['duration'])
         
         print(f"This video length is {vid_length}")
         print(f'Title: {video_title}')
         print(f'Thumbnail URL: {thumbnail_url}')
         