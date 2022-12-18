from PIL import Image
import collections

def get_dominant_colors(image, color_threshold):
    # Open the image and convert it to RGB
    image = Image.open(image).convert('RGB')

    # Get the width and height of the image
    width, height = image.size

    # Initialize a dictionary to store the count of each color
    color_count = {}

    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            r, g, b = image.getpixel((x, y))

            # Convert the RGB values to a hex string
            hex_color = '#%02x%02x%02x' % (r, g, b)

            # If the hex string is not in the dictionary, add it with a count of 1
            if hex_color not in color_count:
                color_count[hex_color] = 1
            # Otherwise, increment the count for that color
            else:
                color_count[hex_color] += 1

    # Sort the dictionary by value in descending order
    sorted_colors = sorted(color_count.items(), key=lambda item: item[1], reverse=True)

    # Calculate the total number of pixels in the image
    total_pixels = width * height

    # Convert the count of each color to a percentage
    dominant_colors = {}  # Change this to a dictionary
    for color, count in sorted_colors:
        percentage = count / total_pixels * 100
        # Check if the color is similar to any of the dominant colors
        is_similar = False
        for dominant_color in dominant_colors:
            if color_distance(color, dominant_color) < color_threshold:
                # If the color is similar, add its percentage to the dominant color
                dominant_colors[dominant_color] += percentage
                is_similar = True
                break
        if not is_similar:
            # If the color is not similar to any of the dominant colors, add it as a new dominant color
            dominant_colors[color] = percentage

    return dominant_colors

def color_distance(color1, color2):
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

    distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5

    return distance

# Example usage
image = 'image.jpg'
color_threshold = 20  # Change the value of the color threshold here
dominant_colors = get_dominant_colors(image, color_threshold)

# Sort the dominant colors by percentage in descending order
sorted_colors = sorted(dominant_colors.items(), key=lambda item: item[1], reverse=True)

# Ask the user if they want to calculate the area of each color
calculate_area = input('Do you want to calculate the area of each color? (y/n) ')
if calculate_area == 'y':
    # Ask the user for the total area of the painting
    total_area = float(input('Enter the total area of the painting in square meters: '))
    for color, percentage in sorted_colors:  # Use the items method to iterate over the dictionary
        area = percentage * total_area / 100
        sprays = area / 3  # Calculate the number of sprays needed
        liters = area / 10  # Calculate the number of liters needed
        print(f'{color}: {area:.2f} square meters ({percentage:.2f}%), {liters:.2f} liters of paint or {sprays:.2f} sprays')
else:
    for color, percentage in sorted_colors:  # Use the items method to iterate over the dictionary
        print(f'{color}: {percentage:.2f}%')