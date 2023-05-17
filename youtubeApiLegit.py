import os

import googleapiclient.discovery

    
def get_playList_id(playlist_url):
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
     
    

def get_playlist_thumbnails(playlist_url, max_results, api_key):

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    

    # Specify the playlist ID
    playlist_id = get_playList_id(playlist_url)

    # Retrieve the playlist items
    playlist_items = youtube.playlistItems().list(
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
        
        
        
        
        print(f'Title: {video_title}')
        print(f'Thumbnail URL: {thumbnail_url}')
