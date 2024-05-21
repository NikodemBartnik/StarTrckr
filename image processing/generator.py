import numpy as np
from PIL import Image


def generate_fake_night_sky(width, height, num_stars):
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    stars_x = np.random.randint(0, width, size=num_stars)
    stars_y = np.random.randint(0, height, size=num_stars)

    for x, y in zip(stars_x, stars_y):
        canvas[y, x] = [255, 255, 255]
    return canvas


def save_image(image_data, filename):
    image = Image.fromarray(image_data)
    image.save(filename)


if __name__ == "__main__":
    width = 30000
    height = 30000
    num_stars = int(input("Enter the number of stars: "))

    fake_night_sky = generate_fake_night_sky(width, height, num_stars)

    save_image(fake_night_sky, "fake_night_sky2.png")
    print("Fake night sky image saved successfully.")
