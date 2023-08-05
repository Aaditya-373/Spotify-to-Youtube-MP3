import pytube
from pytube import YouTube
from pytube import Search

import os
def download_vid_convert_to_mp3(vid):
    yt = Youtube(vid)
    video  = yt.streams.filter(only_audio=True).first()
    destination  = 'D:\downloadedsongs'
    output_file = video.download(output_path=destination)
    base, ext = os.path.splitext(output_file)
    new_file = base + '.mp3'
    os.rename(output_file, new_file)

vid  = 'https://youtu.be/EAYlckSaviI'
download_vid_convert_to_mp3(vid)





    




