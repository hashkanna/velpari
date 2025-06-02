"""Story processing module.

This module handles reading and processing story text files, including
splitting them into paragraphs for processing.
"""

from pathlib import Path
from src.utils.config import Config


class StoryProcessor:
    """Handles story file reading and text processing.
    
    This class manages reading story files from the input directory and
    processing them into paragraphs for audio and image generation.
    """
    
    def __init__(self):
        self.config = Config()
    
    def split_into_paragraphs(self, text: str) -> list[str]:
        """Split text into paragraphs based on double newlines.
        
        Args:
            text (str): The full story text
        
        Returns:
            list[str]: List of paragraphs
        """
        return [p.strip() for p in text.split("\n\n") if p.strip()]
    
    def get_chapter_path(self, chapter_number: int) -> Path:
        """Get path to chapter file.
        
        Args:
            chapter_number (int): Chapter number
        
        Returns:
            Path: Path to chapter file
        """
        return Path(self.config.directories['input']) / f"chapter{chapter_number}.txt"
    
    def get_base_prompt_path(self, chapter_number: int) -> Path:
        """Get path to base prompt file for a chapter.
        
        Args:
            chapter_number (int): Chapter number
        
        Returns:
            Path: Path to base prompt file
        """
        return Path(self.config.directories['input']) / f"chapter{chapter_number}_base_prompt.txt"
    
    def read_base_prompt(self, chapter_number: int) -> str:
        """Read base prompt for a chapter.
        
        Args:
            chapter_number (int): Chapter number
            
        Returns:
            str: Base prompt text, or None if file doesn't exist
        """
        prompt_path = self.get_base_prompt_path(chapter_number)
        if prompt_path.exists():
            return prompt_path.read_text().strip()
        return None
    
    def read_chapter(self, chapter_number: int) -> str:
        """Read a specific chapter from file.
        
        Args:
            chapter_number (int): The chapter number to read
        
        Returns:
            str: Chapter text content
        
        Raises:
            FileNotFoundError: If chapter file doesn't exist
        """
        file_path = self.get_chapter_path(chapter_number)
        if not file_path.exists():
            raise FileNotFoundError(
                f"Chapter {chapter_number} not found at {file_path}"
            )
        
        with open(file_path, "r") as f:
            return f.read()
    
    def get_output_filename(self, chapter_number: int) -> str:
        """Get the output filename for a chapter's video.
        
        Args:
            chapter_number (int): The chapter number
        
        Returns:
            str: Output filename for the video
        """
        return self.config.story['output_filename_pattern'].format(chapter_number) 