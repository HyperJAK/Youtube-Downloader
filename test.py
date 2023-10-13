#testing

title = "Hello there i"
title = title.split(' ')

new_title = ''
new_title += title[0]

if len(title) > 2:
   for i in range(len(title) - (int)(len(title) - 2)):
      new_title += (title[i + 1])
   
print(new_title)


download_thumbnail = "false"

if download_thumbnail == "false":
   download_thumbnail = False


print(download_thumbnail)