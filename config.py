TOKEN = 'ODg3NzY5OTYxMzk1ODEwMzQ0.YUI-NA.ogjVWmKeO55R5PvhDqtlET8IRrQ'

ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': 'True',
        'simulate': 'True',
        'source_address': '0.0.0.0',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

ffmpeg_opts = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}
