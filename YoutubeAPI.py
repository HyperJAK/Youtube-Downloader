import googleapiclient.discovery

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
   
   
   
   
   def get_playList_id(self, playlist_url):
      string_length = len(playlist_url)
      concat_string = ''
      
      for i in range(0, string_length):  
         concat_string = playlist_url[i:i+5]

         if concat_string == 'list=':
               concat_string = playlist_url[i+5:string_length]
               break
         else:
               concat_string = ''
               if i+5 == string_length:
                  return False
      
      return concat_string  
      
   
   
   
   def get_video_length(self, vid_id):
      video_info = self.youtube.videos().list(
         part='snippet',
         id=vid_id,
      ).execute()
      
      vid_length = (video_info['contentDetails']['duration'])
         
      print(f"This video length is {vid_length}")
    
    
   
   
      
      
   
   def get_playlist_thumbnails(self, playlist_url, max_results):

      # Specify the playlist ID
      playlist_id = self.get_playList_id(playlist_url)

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
         