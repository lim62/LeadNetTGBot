from PIL import Image, ImageDraw

def change_photo(user_photo_path: str, user_id: int) -> None:
    template_path = "bot/media/avatars/draft.jpg"  

    template = Image.open(template_path).convert("RGBA")
    user_photo = Image.open(user_photo_path).convert("RGBA")

    paste_x = 310
    paste_y = 240

    circle_size = 235

    mask = Image.new("L", (circle_size, circle_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, circle_size, circle_size), fill=255)

    user_photo = user_photo.resize((circle_size, circle_size))
    circle_avatar = Image.new("RGBA", (circle_size, circle_size))
    circle_avatar.paste(user_photo, (0, 0), mask)

    template.paste(circle_avatar, (paste_x, paste_y), circle_avatar)

    template.save(f'bot/media/avatars/pusk_prepare{user_id}.png')