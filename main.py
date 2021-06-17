from PIL import Image
import requests
import time
import os

bearer = input("Bearer: ")

template_head_coords = [8, 8, 16, 16]

x_diff = int(template_head_coords[2] - template_head_coords[0])
y_diff = int(template_head_coords[3] - template_head_coords[1])

template = Image.open("template.png")
input_file = Image.open("input.jpg")

region = input_file.resize((9 * x_diff, 3 * y_diff), Image.ANTIALIAS)
region.save("region.png")

def write_head(inp, num):
    template.paste(inp, (template_head_coords[0], template_head_coords[1], template_head_coords[2],
        template_head_coords[3]))

    template.save(f"num{num}.png")

def changeskin(bearer, filename):
    headers = {"Authorization": "Bearer " + bearer}
    files = {
        'variant': (None, 'classic'),
        'file': (f'{filename}.png', open(f'{filename}.png', 'rb')),
    }
    response = requests.post('https://api.minecraftservices.com/minecraft/profile/skins', headers=headers, files=files)
    time.sleep(1)
    if response.status_code == 200 or response.status_code == 204:
        print(f"Successfully changed skin, Refresh NameMC Profile")
    else:
        print(response.text)

a = 0
b = 0
ee = []
for y in range(1, 4):

    a = 0
    for x in range(1, 10):
        region_ = region.crop((a, b, (x * int(x_diff)), y * int(y_diff)))

        write_head(region_, f"{x}{y}")

        a += int(x_diff)
        ee.append(f"{x}{y}")
        time.sleep(0.25)
    b += int(y_diff)

time.sleep(1)

ee.reverse()
for i in ee:
    _img_ = Image.open(f"num{i}.png")
    _img = _img_.resize((64, 64), Image.ANTIALIAS)
    _img.save(f"dum{i}.png")
    time.sleep(0.1)


for i in ee:
    changeskin(bearer, f"dum{i}")
    time.sleep(5) # Change this for more time to refresh NameMc Profile


for i in ee:
    os.system(f"del dum{i}.png")
    os.system(f"del num{i}.png")

input("Finished, Press enter to quit: ")