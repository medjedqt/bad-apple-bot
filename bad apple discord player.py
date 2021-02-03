import discord
from discord.ext import commands, tasks
import time
from PIL import Image

CLIP_FRAMES = 6571

CLIP_LENGTH = 219.0666

ASCII_CHARS = ['⠀','⠄','⠆','⠖','⠶','⡶','⣩','⣪','⣫','⣾','⣿']
ASCII_CHARS.reverse()
ASCII_CHARS = ASCII_CHARS[::-1]

WIDTH = 60

TIMEOUT = 1/((int(CLIP_FRAMES/4)+1)/CLIP_LENGTH)*18

def resize(image, new_width=WIDTH):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int((aspect_ratio * new_width)/2)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image

def grayscalify(image):
    return image.convert('L')

def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)

def do(image, new_width=WIDTH):
    image = resize(image)
    image = grayscalify(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    new_image = [pixels[index:index+int(new_width)] for index in range(0, len_pixels, int(new_width))]

    return '\n'.join(new_image)

def runner(path):
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        return
    image = do(image)

    return image

frames = []

for i in range(0, int(CLIP_FRAMES/4)+1):
    path = "frames/frame"+str(i*4)+".jpg" #<--- path to folder containing every frame of the video
    frames.append(runner(path))

bot = commands.Bot(command_prefix="?", help_command=None)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@tasks.loop(count=1)
async def badloop():
    chan = bot.get_channel(806448950726754304)
    mes: discord.Message = await chan.send("initiating bad apple...")
    oldTimestamp = time.time()

    start = oldTimestamp

    i = 0
        
    while i < len(frames)-1:
        disp = False
        while not disp:
            newTimestamp = time.time()
            if (newTimestamp - oldTimestamp) >= TIMEOUT:

                await mes.edit(content=frames[int(i)])
                    
                newTimestamp = time.time()

                i += (newTimestamp - oldTimestamp)/TIMEOUT
                    
                oldTimestamp = newTimestamp

                disp = True
    await mes.edit(content="- The End -")

def medjed(ctx):
    return ctx.author.id == 550076298937237544

@bot.command()
@commands.check(medjed)
@commands.max_concurrency(1)
async def bad(ctx):
    if badloop.is_running():
        return await ctx.send("bad apple is already playing!")
    badloop.start()

bot.run('NTg3OTMxMjE4MTQ2ODg1NjQy.XqBISw._04H2XkhciT2n6yw8qzlQJWxHfM')#<--- Put bot token here
