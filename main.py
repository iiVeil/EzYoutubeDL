import youtube_dl
import subprocess
import os
import ctypes
import random



title = "EzYoutubeDL"
ctypes.windll.kernel32.SetConsoleTitleW(title)
playlists = input("Are you downloading playlists? (y/n): ")
if playlists.lower() == "yes" or playlists.lower() == "y":
	playlists = True
	title += " (Playlist Mode)"
else:
	playlists = False
ctypes.windll.kernel32.SetConsoleTitleW(title)


while True:
	seed = random.randint(1, 9999)
	audio = youtube_dl.YoutubeDL(
		{
			'outtmpl': f'../a{seed}.%(ext)s',
			'format': 'bestaudio/best',
			'noplaylist' : True if playlists else False
		})
	video = youtube_dl.YoutubeDL(
		{
			'outtmpl': f'../v{seed}.%(ext)s',
				'format': 'bestvideo/best',
				'noplaylist': True if playlists else False
		})

	url = input(f"Enter Link{' (Playlist Mode)' if playlists else ''}: ")
	
	print("---------------  DOWNLOADING AUDIO ---------------")
	with audio:
		audio.cache.remove()
		meta = audio.extract_info(url, download=False)
		audio.download([url])
		audioname_ = f"a{seed}.{meta['ext']}"
	print("---------------  DOWNLOADING VIDEO ---------------")
	with video:
		video.cache.remove()
		meta = video.extract_info(url, download=False)
		video.download([url])
		videoname_ = f"v{seed}.{meta['ext']}"

	print("[finishing] Combining audio and video for best quality.")
	cmd = f'ffmpeg -y -i "../{audioname_}"  -r 30 -i "../{videoname_}" -filter:a aresample=async=1 -c:a flac -strict -2 -c:v copy "../{meta["title"]}.mp4"'
	subprocess.call(cmd, shell=True)
	print("[done] Combined.")
	os.remove(f"../{audioname_}")
	os.remove(f"../{videoname_}")

	print(f"\n\n\n\n\n\n\n\n\n\nFinished {meta['title']}.mp4\n\n")

