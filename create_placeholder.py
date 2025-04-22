from PIL import Image, ImageDraw, ImageFont
import os

# Create a placeholder image for the preview
def create_placeholder_image(output_path, width=800, height=450):
    """
    Create a placeholder image with text indicating 'No Preview Available'
    """
    # Create a blank image with gray background
    image = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(image)
    
    # Draw a frame around the image
    draw.rectangle(
        [(0, 0), (width-1, height-1)],
        outline=(200, 200, 200),
        width=2
    )
    
    # Add text
    try:
        # Try to load a font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw the main message
    message = "No Preview Available"
    text_width = draw.textlength(message, font=font)
    position = ((width - text_width) // 2, height // 2 - 50)
    draw.text(
        position,
        message,
        font=font,
        fill=(100, 100, 100)
    )
    
    # Draw additional message
    sub_message = "Start streaming to see your screen"
    try:
        sub_font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        sub_font = ImageFont.load_default()
    
    sub_text_width = draw.textlength(sub_message, font=sub_font)
    sub_position = ((width - sub_text_width) // 2, height // 2 + 10)
    draw.text(
        sub_position,
        sub_message,
        font=sub_font,
        fill=(130, 130, 130)
    )
    
    # Draw NDI logo text
    ndi_text = "NDI Screen Capture"
    try:
        logo_font = ImageFont.truetype("arial.ttf", 18)
    except IOError:
        logo_font = ImageFont.load_default()
    
    logo_text_width = draw.textlength(ndi_text, font=logo_font)
    logo_position = ((width - logo_text_width) // 2, height - 40)
    draw.text(
        logo_position,
        ndi_text,
        font=logo_font,
        fill=(80, 80, 80)
    )
    
    # Save the image
    image.save(output_path)
    print(f"Placeholder image created at {output_path}")

if __name__ == "__main__":
    # Ensure the static directory exists
    os.makedirs("static", exist_ok=True)
    
    # Create the placeholder image
    create_placeholder_image("static/placeholder.png") 