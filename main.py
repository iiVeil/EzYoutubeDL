import youtube_dl
import subprocess
import os
import ctypes
import random
import validators

ctypes.windll.kernel32.SetConsoleTitleW("EzYoutubeDL")


while True:
	seed = random.randint(1, 9999)
	audio = youtube_dl.YoutubeDL(
		{
			'outtmpl': f'a{seed}.%(ext)s',
			'format': 'bestaudio/best',
			'noplaylist' : True
		})
	video = youtube_dl.YoutubeDL(
		{
			'outtmpl': f'v{seed}.%(ext)s',
				'format': 'bestvideo/best',
				'noplaylist': True
		})

	url = input(f"[SEED: {seed}] Enter Link: ")
	if not validators.url(url):
		print("\nInvalid URL\n")
		continue

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
	cmd = f'ffmpeg -y -i "{audioname_}"  -r 30 -i "{videoname_}" -filter:a aresample=async=1 -c:a flac -strict -2 -c:v copy "{meta["id"]}.mp4"'
	subprocess.call(cmd, shell=True)
	os.remove(f"{audioname_}")
	os.remove(f"{videoname_}")

	print(f"\n\nFinished {meta['title']} and saved as {meta['id']}.mp4\n\n")

