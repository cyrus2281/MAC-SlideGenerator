import base64
import os
import markdown
from html2image import Html2Image

from utilities.utils import generate_unique_id


def render_markdown_to_image(markdown_text, output_image_path, size=(720, 480)):
    # Parse Markdown text
    html_text = markdown.markdown(markdown_text).replace("\n", "<br>")
    html_text = f"<div>{html_text}</div>"
    watermark = os.getenv("SLIDES_WATERMARK")
    if (watermark):
        html_text = f"{html_text}<div id=\"watermark\">{watermark}</div>"
    # Convert HTML to image    
    hti = Html2Image()
    css = '''body {
        background: white; 
        height: 90%;
        padding: 5px; 
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-size: 1.4rem;
        font-family: Arial, sans-serif;
        }
        #watermark {
            position: absolute; 
            bottom: 0; 
            left: 0; 
            padding: 5px; 
            background: white; 
            color: black; 
            font-size: 1rem;
        }
        '''
    temp_loc = generate_unique_id() + ".png"
    hti.screenshot(html_str=html_text, save_as=temp_loc, css_str=css, size=size)
    # Move the file to the output location - force overwrite
    if os.path.exists(output_image_path):
        os.remove(output_image_path)
    os.rename(temp_loc, output_image_path)
    
def render_image_inside_html(image_path, output_path, size=(720, 480)):
    if not output_path:
        # Overwrite the initial image if not given an output path
        output_path = image_path
    # Read image as base64 encoded string
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        image_base64 = base64.b64encode(image_data).decode()
    # Formatting for source value
    image_base64 = f"data:image/png;base64,{image_base64}"
    # Create the HTML content with the image
    html_content = f'<img src="{image_base64}" alt="Image" />'
    watermark = os.getenv("SLIDES_WATERMARK")
    if (watermark):
        html_content = f"{html_content}<div id=\"watermark\">{watermark}</div>"
    css = """
    body {
        background: red;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0;
    }
    img {
        width: 100%;
        height: 100%;
    }
    #watermark {
        position: absolute; 
        bottom: 0; 
        left: 0; 
        padding: 5px; 
        background: white; 
        color: black; 
        font-size: 1rem;
    }
    """
    temp_loc = generate_unique_id() + ".png"
    hti = Html2Image()
    hti.screenshot(html_str=html_content, save_as=temp_loc, css_str=css, size=size)
    # Move the file to the output location - force overwrite
    if os.path.exists(output_path):
        os.remove(output_path)
    os.rename(temp_loc, output_path)