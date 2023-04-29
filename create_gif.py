from PIL import Image

def sparkle_gif_create_frames(image_filepath_to_add_sparkle, random_image_picker):

        if random_image_picker == 1:
                still_frames = 50
                motion_frames_plus_one = 10
                resize_multiplier = 9
                paste_adjustment = 5
                paste_x_position = 284
                paste_y_position = 407

        if random_image_picker == 2:
                still_frames = 50
                motion_frames_plus_one = 9
                resize_multiplier = 9
                paste_adjustment = 5
                paste_x_position = 306
                paste_y_position = 419

        if random_image_picker == 3:
                still_frames = 50
                motion_frames_plus_one = 10
                resize_multiplier = 9
                paste_adjustment = 5
                paste_x_position = 293
                paste_y_position = 412

        if random_image_picker == 4:
                still_frames = 50
                motion_frames_plus_one = 10
                resize_multiplier = 9
                paste_adjustment = 5
                paste_x_position = 303
                paste_y_position = 512

        if random_image_picker == 5:
                still_frames = 50
                motion_frames_plus_one = 10
                resize_multiplier = 9
                paste_adjustment = 5
                paste_x_position = 318
                paste_y_position = 517

        if random_image_picker == 6:
                still_frames = 50
                motion_frames_plus_one = 10
                resize_multiplier = 9
                paste_adjustment = 5
                paste_x_position = 268
                paste_y_position = 407


        for x in range(1,still_frames+1):
                image_to_sparkle = Image.open(image_filepath_to_add_sparkle)
                image_to_sparkle = image_to_sparkle.resize((int(image_to_sparkle.size[0]/2.7),int(image_to_sparkle.size[1]/2.7)))
                image_to_sparkle.save(f"assets/sparkled_mascot_images/{x}.jpg")
                x += 1

        # sparkle growing from 0 to max size
        for x in range(1,motion_frames_plus_one):
                image_to_sparkle = Image.open(image_filepath_to_add_sparkle)
                sparkle = Image.open("assets/sparkle.png")
                image_to_sparkle = image_to_sparkle.resize((int(image_to_sparkle.size[0]/2.7),int(image_to_sparkle.size[1]/2.7)))
                sparkle = sparkle.resize(((100-((motion_frames_plus_one-1-x)*resize_multiplier)),(100-(motion_frames_plus_one-1-x)*resize_multiplier)))
                image_to_sparkle.paste( sparkle ,(paste_x_position+((motion_frames_plus_one-x)*paste_adjustment), paste_y_position+((motion_frames_plus_one-x)*paste_adjustment)), sparkle)
                image_to_sparkle.save(f"assets/sparkled_mascot_images/{x+still_frames}.jpg")
                x += 1

        # sparkle shrinking from max size to 0
        for x in range(1,motion_frames_plus_one):
                image_to_sparkle = Image.open(image_filepath_to_add_sparkle)
                sparkle = Image.open("assets/sparkle.png")
                image_to_sparkle = image_to_sparkle.resize((int(image_to_sparkle.size[0]/2.7),int(image_to_sparkle.size[1]/2.7)))
                sparkle = sparkle.resize(((100-((x-1)*resize_multiplier)),(100-((x-1)*resize_multiplier))))
                image_to_sparkle.paste( sparkle ,(paste_x_position+(x*paste_adjustment), paste_y_position+(x*paste_adjustment)), sparkle)
                image_to_sparkle.save(f"assets/sparkled_mascot_images/{x+motion_frames_plus_one+still_frames-1}.jpg")
                x += 1

        create_gif(still_frames, motion_frames_plus_one)


def create_gif(still_frames, motion_frames_plus_one):
        imgs=[]
        for i in range(1,still_frames+(motion_frames_plus_one*2-1)): 
                imgs.append(f"assets/sparkled_mascot_images/{i}.jpg")

        frames = []
        for i in imgs:
                new_frame = Image.open(i)
                frames.append(new_frame)

        frames[0].save('assets/tweet_image_sparkled.gif', format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=35, loop=0)


# if __name__ == "__main__":
#     sparkle_gif_create_frames("assets/blank_belly_dark_mode/1.jpg",1)
#     sparkle_gif_create_frames("assets/tweet_image.jpg",2)