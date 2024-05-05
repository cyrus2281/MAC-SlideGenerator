from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips

def create_voice_overed_slide(input_image, input_audio, output_file, end_padding=1):
    # Load the image clip
    image_clip = ImageClip(input_image)
    # Load the audio clip
    audio_clip = AudioFileClip(input_audio)
    # Set the duration of the image clip to match the audio clip
    image_clip = image_clip.set_duration(audio_clip.duration + end_padding)
    # Set the audio of the image clip to the loaded audio clip
    image_clip = image_clip.set_audio(audio_clip)
    # Write the final video file
    image_clip.write_videofile(output_file, fps=12, logger=None, audio_codec='libvorbis')
    
    audio_clip.close()
    image_clip.close()

def merge_videos(videos_list, output_video):
    # Create an empty list to store the video clips
    video_clips = []
    # Iterate over each video path in the videos_list
    for video_path in videos_list:
        # Load the video clip
        video_clip = VideoFileClip(video_path)
        # Append the video clip to the list
        video_clips.append(video_clip)
    
    # Concatenate the video clips into a single video
    final_clip = concatenate_videoclips(video_clips)
    
    # Write the final video file
    final_clip.write_videofile(output_video, fps=12, logger=None, audio_codec='libvorbis')

    # Closing resources
    for video_path in videos_list:
        video_clip.close()
    final_clip.close()

    
