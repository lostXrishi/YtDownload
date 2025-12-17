import yt_dlp
from tqdm import tqdm

# banner
from rich.console import Console
from rich.text import Text
console = Console()
art = r"""
                                                     ___
                                     ____          /   /                                                        
                                     \   \        /   /________________________________                                                 
                                      \   \      /                                     |         
                                       \   \    /   _________     _____________________|                                                     
                                        \   \  /   /         |   |                              
                                         \   \/   /          |   |
                                          \      /           |   |                                     __         
                                           \    /            |   |                                    |  |
 ________                                  /   /___      __  |   |     _______                        |  |   
|         \                               /   /|    \   |  | |   |   /   ___   \      ___             |  |                                          
|    __     \     _______                /   / |  \  \  |  | |   |  |   |   |   |    /    \           |  |                                                              
|   |   \    |  /   ___   \   _         /   /  |  |\  \ |  | |   |  |   |   |   |   /  /\  \          |  |                                                                                
|   |    |   | |   |   |   | \  \      /   /   |  | \  \|  | |   |  |   |___|   |  /  /__\  \      ___|  |                                                                           
|   |___/   /  |   |   |   |  \  \ /\ /   /    |  |  \_____| |   |   \_________/  /  _____   \    /  _   |                                                                                  
|          /   |   |___|   |   \   ..    /     |  |          |    \____________  /  /     \   \  |  (_|  |                                                                                
|________/      \_________/     \_/  \__/     /__/           |_________________|/__/       \___\  \______|                                                                                   
""".strip("\n").splitlines()

colors = [
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0062",
    "#ff0077",
    "#ff006a",
    "#ff009d",
    "#ff00ff",
    "#ff00ff",
    "#cc33ff",
    "#9966ff",
    "#6699ff",
    "#33ccff",
    "#00ffff",
    "#00ffcc",
    "#00ff99",
]
for i, line in enumerate(art):
    t = Text(line, style=colors[i % len(colors)])
    console.print(t)

console.print("[bold green]         Welcome to YT DOWNLOAD, here you can download Youtube Videos and Audios[/]")
# console.print("[bold yellow]     Welcome to YT DOWNLOAD, here you can download Youtube Videos and Audios[/]")
# console.print("[bold red]     Welcome to YT DOWNLOAD, here you can download Youtube Videos and Audios[/]")

url = console.input("[bold blue]\n\n  Enter Youtube Video Link:  ")
# url = "https://youtu.be/8of5w7RgcTc?si=WZoSTrX8PQijPMEH"

pbar = None
# p-bar config
def progress_hook(d):
        global pbar
        if d['status'] == 'downloading':
            if pbar is None:
                # total = d.get('total_bytes') or d.get('total_bytes_estimate')
                total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
                pbar = tqdm(
                total=total,
                unit='B',
                unit_scale=True,
                dynamic_ncols=True
            )
            pbar.update(d.get('downloaded_bytes', 0) - pbar.n)
        
        elif d['status'] == 'finished':
            if pbar:
                pbar.close()

# Common options (used for both video & audio)
common_options = {
    'quiet': True,
    'no_warnings': True,
}

# 2️⃣ Get video information (title only)
with yt_dlp.YoutubeDL(common_options) as ydl:
    info = ydl.extract_info(url, download=False)
    title = info['title']

console.print("[bold blue]\n  Title:[/]", title)

# 3️⃣ Ask user what to download
console.print("[bold yellow]\n  What do you want to Download?[/]")
console.print("[bold blue]    1. Video[/]")
console.print("[bold blue]    2. Audio[/]")

choice = console.input("[bold yellow]  Enter 1 or 2: ")

# 4️⃣ Set options based on user choice
if choice == "1":
    console.print("[bold red]\nDownloading video...[/]")
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
    }

elif choice == "2":
    console.print("[bold red]\nDownloading audio...[/]")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

else:
    console.print("[bold red]Invalid choice!![/]")
    console.print("[bold #ff69b4]\nThank You <3[/]")
    exit()


# 5️⃣ Download
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])


console.print("[bold blue]\nDownload successful ✅[/]")
console.print("[bold #ff69b4]\nThank You <3[/]")
input()