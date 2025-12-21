from PIL import Image
import sys

def rgb888_to_rgb565(r, g, b):
    """Convert 8-bit RGB to 16-bit RGB565."""
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def convert_image(input_file, output_file):
    # Open image and convert to RGB
    img = Image.open(input_file).convert("RGB")
    width, height = img.size

    with open(output_file, "w") as f:
        f.write(f"{width},{height}\n")
        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                rgb565 = rgb888_to_rgb565(r, g, b)
                f.write(f"{rgb565}\n")
    print(f"Saved {output_file} ({width}x{height})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python png2txt.py input.png output.txt")
    else:
        convert_image(sys.argv[1], sys.argv[2])
