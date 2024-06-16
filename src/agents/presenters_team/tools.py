from typing import Annotated, List, Optional
from langchain_core.tools import tool
from utilities.video_utils import create_voice_overed_slide, merge_videos
from utilities.slide_utils import render_image_inside_html, render_markdown_to_image
from utilities.audio_utils import text_to_audio
from utilities.utils import generate_unique_filename

@tool
def generate_video_slide(
    type: Annotated[str, "The type of slide to generate (image or text)"],
    content: Annotated[str, "Markdown document for text slide, and image URL for image slide"],
    notes: Annotated[Optional[str], "Notes for the slide to be voiced over"],
) -> Annotated[str, "The path of the generated video slide"]:
    """Generates a video slide based on the provided note, content and type"""
    try:
        # Step 1 - Generate audio
        audio_path = generate_unique_filename("audio", "mp3", "audio")
        text_to_audio(notes, audio_path)
        # Step 2 - Conditionally generate base image
        slide_image_path = generate_unique_filename("slide", "png", "slides")
        # image size
        size = (720, 480)
        if type == "image":
            render_image_inside_html(content, slide_image_path, size)
        else:
            render_markdown_to_image(content, slide_image_path, size)
        # Step 3 - Generate video slide
        video_path = generate_unique_filename("slide", "mp4", "videos")
        create_voice_overed_slide(
            slide_image_path, audio_path, video_path
        )
        # Step 4 - Return the path of the generated video slide
        return f"Generated video slide at \"{video_path}\""
    except Exception as e:
        print(f"Error generating video slide: {e}")
        return "Failed to generate video slide"


@tool
def merge_video_slides(
    video_slide_paths: Annotated[List[str], "List of paths of video slides to merge"]
) -> Annotated[str, "The path of the merged video slide"]:
    """Merges the provided video slides into a single video slide"""
    try:
        # Video Path
        output_path = generate_unique_filename("output_video", "mp4")
        # Merge the video slides
        merge_videos(video_slide_paths, output_path)
        # Return the path of the merged video slide
        return f"Generated merged video slide at \"{output_path}\""
    except Exception as e:
        print(f"Error merging video slides: {e}")
        return "Failed to merge video slides"