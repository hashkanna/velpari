"""Configuration management for the video generator.

This module provides a singleton Config class that manages all configuration
settings for the video generator, including directories, API settings, and
video parameters.
"""

from pathlib import Path
import yaml


class Config:
    """Singleton configuration manager.
    
    This class loads and provides access to all configuration settings from
    the YAML config file. It follows the singleton pattern to ensure only
    one instance exists.
    
    Attributes:
        config (dict): The loaded configuration settings
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'config'):
            config_path = Path('config/default.yml')
            with open(config_path) as f:
                self.config = yaml.safe_load(f)
    
    @property
    def directories(self) -> dict:
        """Get directory configurations.
        
        Returns:
            dict: Directory paths configuration
        """
        return self.config['directories']
    
    @property
    def elevenlabs(self) -> dict:
        """Get ElevenLabs API configurations.
        
        Returns:
            dict: ElevenLabs settings
        """
        return self.config['elevenlabs']
    
    @property
    def openai(self) -> dict:
        """Get OpenAI API configurations.
        
        Returns:
            dict: OpenAI settings
        """
        return self.config['openai']
    
    @property
    def video(self) -> dict:
        """Get video generation configurations.
        
        Returns:
            dict: Video encoding settings
        """
        return self.config['video']
    
    @property
    def story(self) -> dict:
        """Get story processing configurations.
        
        Returns:
            dict: Story settings including chapter patterns
        """
        return self.config['story']
    
    def ensure_directories(self):
        """Create all necessary directories if they don't exist."""
        for dir_path in self.directories.values():
            Path(dir_path).mkdir(parents=True, exist_ok=True) 