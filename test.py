# importing packages
from pytube import YouTube
from pytube import Search
import os

def download_vid_convert_to_mp3(vid):
    yt = YouTube(
	    vid)

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    # check for destination to save file
    print("Enter the destination (leave blank for current directory)")
    destination = str(input(">> ")) or '.'

    # download the file
    out_file = video.download(output_path=destination)

    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

with open('playlist_data.txt','r') as filename:
     song_list = filename.readlines()
for song in song_list:
    song = song.strip()
    s = Search(song)
    print(s.results)
    for v in s.results[:1]:
        print(f"{v.title}\n{v.watch_url}\n")
        download_vid_convert_to_mp3(v.watch_url)
        




