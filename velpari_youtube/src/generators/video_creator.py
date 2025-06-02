"""Video creation module using MoviePy.

This module handles the creation of video clips by combining generated
images and audio files, and merging them into a final video.
"""

from pathlib import Path
from tqdm import tqdm
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from src.utils.config import Config


class VideoCreator:
    """Handles video creation using MoviePy.
    
    This class manages the creation of video clips from image and audio
    files, and combines them into a final video with proper encoding.
    """
    
    def __init__(self):
        self.config = Config()
        self.output_dir = Path(self.config.directories['output'])
        self.output_dir.mkdir(exist_ok=True)
    
    def create_clip(self, image_path: Path, audio_path: Path) -> ImageClip:
        """Create a video clip from image and audio files.
        
        Args:
            image_path (Path): Path to the image file
            audio_path (Path): Path to the audio file
        
        Returns:
            ImageClip: Video clip with synchronized audio
        """
        audio = AudioFileClip(str(audio_path))
        image = ImageClip(str(image_path))
        video = image.set_duration(audio.duration)
        return video.set_audio(audio)
    
    def create_video(
        self,
        image_paths: list[Path],
        audio_paths: list[Path],
        output_name: str
    ) -> Path:
        """Create video from images and audio files.
        
        Args:
            image_paths (list[Path]): List of image file paths
            audio_paths (list[Path]): List of audio file paths
            output_name (str): Output video filename
        
        Returns:
            Path: Path to the generated video file
        """
        print("\n🎬 Creating video...")
        
        # Create clips for each image-audio pair
        clips = []
        for img_path, audio_path in tqdm(
            zip(image_paths, audio_paths),
            desc="Creating clips",
            total=len(image_paths)
        ):
            # Load audio to get duration
            audio = AudioFileClip(str(audio_path))
            
            # Create image clip with same duration as audio
            image = ImageClip(str(img_path))
            image = image.set_duration(audio.duration)
            
            # Combine image and audio
            clip = image.set_audio(audio)
            clips.append(clip)
        
        # Concatenate all clips
        final = concatenate_videoclips(clips)
        
        # Get output path
        output_path = Path(self.config.directories['output']) / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write video with high quality settings
        print("\n💾 Writing final video...")
        final.write_videofile(
            str(output_path),
            fps=self.config.video['fps'],
            codec=self.config.video['video_codec'],
            preset=self.config.video['video_preset'],
            audio_codec=self.config.video['audio_codec'],
            audio_bitrate=self.config.video['audio_bitrate'],
            ffmpeg_params=[
                "-crf", str(self.config.video['video_quality']),
                "-pix_fmt", self.config.video['pixel_format']
            ]
        )
        
        return output_path 