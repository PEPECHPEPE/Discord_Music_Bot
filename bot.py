import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from config import TOKEN, ydl_opts, ffmpeg_opts
from requests import get
import asyncio

client = commands.Bot(command_prefix=["~", "=", "1", "`", "+", "ё", "Ё"])

music_list = []
first_play = True
check = False
check_playing = 0
skip_check = False
check_dis = False


@client.event
async def on_ready():
    print('Ready!')
    print('-----------------------------------------------------------')


@client.command()
async def p(ctx, *, arg: str):

    if arg.startswith('https://www.youtube'):
        url = arg

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        video = info
        URL = info['formats'][0]['url']
        title = video['title']
        duration = video['duration']

    else:
        with YoutubeDL(ydl_opts) as ydl:
            try:
                get(arg)
            except:
                video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else:
                video = ydl.extract_info(arg, download=False)
            URL = video['url']
            title = video['title']
            duration = video['duration']


    user_channel = str(ctx.message.author.voice.channel)

    print('-----------------------------------------------------------')
    print(user_channel)
    print(ctx.message.author)
    print(URL)
    print(title)
    print(f'Длинна: {duration}сек')
    print('-----------------------------------------------------------')

    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=user_channel)
    invoking_voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if invoking_voice and invoking_voice != voice_channel:
        print('Уже подключен')
    else:
        await voice_channel.connect()

    #voice_play = discord.utils.get(client.voice_clients, guild=ctx.guild)
    #voice_play.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=p_s_url, **ffmpeg_opts))

    await ctx.send(f"**Поставлено в очередь:** \n>>> ```{title}``` ")

    trek = {
        'title': title,
        'url': URL,
        'duration': duration,
    }

    music_list.append(trek)
    if first_play:
        await play(ctx)


async def play(ctx):
    global voice, trek_now, first_play, check, check_playing, skip_check, check_dis, music_list
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    while True:
        if not check or first_play:
            first_play = False
            check = True
            trek_now = music_list.pop(0)

            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=trek_now['url'], **ffmpeg_opts))

            await ctx.send(f"**Сейчас играет:** \n>>> ```{trek_now['title']}``` ")

            print(trek_now['duration'])
        elif check:
            check_playing += 1
            await asyncio.sleep(1)
            if check_playing >= trek_now['duration']:
                check = False
                check_playing = 0
                if not music_list:
                    first_play = True
                    print('офаю поток')
                    break
            elif skip_check:
                voice.stop()
                check = False
                check_playing = 0
                skip_check = False
                if not music_list:
                    first_play = True
                    print('офаю поток')
                    break
            elif check_dis:
                check_dis = False
                music_list = []
                first_play = True
                check = False
                check_playing = 0
                skip_check = False
                check_dis = False
                break

@client.command()
async def dis(ctx):
    global check_dis
    check_dis = True
    voice_dis = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_dis.is_connected():
        await voice_dis.disconnect()
    else:
        print("Бот не находится в войсе")


@client.command()
async def skip(ctx):
    global skip_check
    skip_check = True


@client.command()
async def vol(ctx, volume):
    voice_vol = discord.utils.get(client.voice_clients, guild=ctx.guild)
    vol_new = int(volume)
    if voice_vol and voice_vol.is_connected():
        voice_vol.source = discord.PCMVolumeTransformer(voice_vol.source, vol_new / 100)


client.run(TOKEN)
