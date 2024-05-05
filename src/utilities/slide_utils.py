import os
import markdown
from html2image import Html2Image

from utilities.utils import generate_unique_id


def render_markdown_to_image(markdown_text, output_image_path, size=(720, 480)):
    # Parse Markdown text
    html_text = markdown.markdown(markdown_text).replace("\n", "<br>")
    # Convert HTML to image    
    hti = Html2Image()
    css = '''body {
        background: white; 
        padding: 10px 5px; 
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-size: 1.4rem;
        font-family: Arial, sans-serif;
        }'''
    temp_loc = generate_unique_id() + ".png"
    hti.screenshot(html_str=html_text, save_as=temp_loc, css_str=css, size=size)
    # Move the file to the output location - force overwrite
    if os.path.exists(output_image_path):
        os.remove(output_image_path)
    os.rename(temp_loc, output_image_path)
