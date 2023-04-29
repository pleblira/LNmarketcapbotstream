from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

def image_draw_angled(LN_capacity_in_BTC, tweet_image):

        if tweet_image == "assets/blank_belly_dark_mode/1.jpg":
                font_size = 85
                rotate_angle = -7.5
                paste_x_position = 639
                paste_y_position = 1265

        if tweet_image == "assets/blank_belly_dark_mode/2.jpg":
                font_size = 95
                rotate_angle = -2.5
                paste_x_position = 712
                paste_y_position = 1315
                
        if tweet_image == "assets/blank_belly_dark_mode/3.jpg":
                font_size = 88
                rotate_angle = 3
                paste_x_position = 926
                paste_y_position = 1285

        if tweet_image == "assets/blank_belly_dark_mode/4.jpg":
                font_size = 86
                rotate_angle = -2.5
                paste_x_position = 747
                paste_y_position = 1303

        if tweet_image == "assets/blank_belly_dark_mode/5.jpg":
                font_size = 86
                rotate_angle = -4
                paste_x_position = 622
                paste_y_position = 1268
                
        if tweet_image == "assets/blank_belly_dark_mode/6.jpg":
                font_size = 90
                rotate_angle = -23.2
                paste_x_position = 455
                paste_y_position = 1190

        tweet_image = Image.open(tweet_image)
        font = ImageFont.truetype("assets/Silom.ttf",font_size)
        
        # Creating a temporary canvas, drawing the text on it, and rotating
        temporary_canvas = Image.new(mode='L', size=(500,500))
        text_on_temporary_canvas = ImageDraw.Draw(temporary_canvas)
        text_on_temporary_canvas.text((0, 0), str(LN_capacity_in_BTC) + "\nBTC", font=font, fill=255, align="center")
        rotated_text_on_temporary_canvas=temporary_canvas.rotate(rotate_angle, resample=3, expand=1)

        # pasting temporary canvas on main image
        tweet_image.paste( ImageOps.colorize(rotated_text_on_temporary_canvas, (0,0,0), (242,169,0)), (paste_x_position,paste_y_position), rotated_text_on_temporary_canvas)

        # tweet_image.show()
        tweet_image.save("assets/tweet_image.jpg")
        return None

# if __name__ == "__main__":
#     image_draw_angled(5002, "assets/blank_belly_dark_mode/6.jpg")