from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from data.dataloader import TIME_24h


def make_gif(gif_name) -> None:
    """
    Erstelle ein Gif aus allen 24 Bildern
    :return:
    """

    images: list = []  # to display all 24 images in a gif

    for tidx, t in enumerate(TIME_24h):
        fname = f'arrows_map_{tidx}.png'
        # Open each PNG file and append it to a list
        image_png = Image.open(fname)

        # Create a drawing context for the image
        draw = ImageDraw.Draw(image_png)

        # Define the text label to add
        text = f'Werktagverkehr in Altdorf für t = {t.strftime("%H:%M")} ' \
               f'© André Eggli'

        # Define the font to use for the text label
        font = ImageFont.truetype('arial.ttf', 22)

        # Add the text label to the image
        draw.text((10, image_png.height - 30), text, fill=(0, 0, 0), font=font)

        images.append(image_png)

    # Save the list of images as a GIF animation
    images[0].save(gif_name, save_all=True,
                   append_images=images[1:], duration=400, loop=0)


if __name__ == "__main__":
    make_gif('Altdorf_Verkehr.gif')
