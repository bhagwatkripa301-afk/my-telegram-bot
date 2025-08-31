"""
Configuration module for the Enhanced Course Bot
Handles environment variables and bot settings
"""

import os
import base64
import logging
from typing import List

class Config:
    """Configuration class for bot settings"""
    
    def __init__(self):
        # Bot credentials
        self.BOT_TOKEN = os.getenv(
            "BOT_TOKEN", 
            "7850621902:AAGJ1e59fXcIz4Vcix8dz3aQVJepTvoBS08"
        )
        
        # Search API credentials
        self.SERPAPI_KEY = os.getenv(
            "SERPAPI_KEY", 
            "abcdb784fb8ee0b773d4ff2d3da0597c52571a1a43b96850a0d3551d43b4c5fb"
        )
        
        # Developer info (encoded)
        self.DEVELOPER_TELEGRAM = base64.b64decode("QE5HWVQ3NzdHRw==").decode('utf-8')
        
        # --- ZAROORI CHANNELS ---
        # Bot istemal karne ke liye users ko in channels ko join karna zaroori hai.
        self.REQUIRED_CHANNELS = [
            "@winclashplaykar0",
            "@winclashplay",
            -1002712519615  # Yeh aapka private channel ID hai
        ]

        # Search settings
        self.MAX_RESULTS_PER_PAGE = 5
        self.MAX_SEARCH_HISTORY = 20
        self.MAX_FAVORITES = 50
        
        # Supported platforms
        self.SUPPORTED_PLATFORMS = [
            "drive.google.com",
            "mediafire.com", 
            "mega.nz",
            "dropbox.com",
            "onedrive.live.com"
        ]
        
        # Search engines
        self.SEARCH_ENGINES = ["google", "bing", "duckduckgo"]
        
        # Rate limiting
        self.RATE_LIMIT_SEARCHES = 10  # per minute
        self.RATE_LIMIT_WINDOW = 60    # seconds
        
        # Database settings
        self.DATABASE_FILE = "course_bot.db"
        
        # Progress animation settings
        self.PROGRESS_FRAMES = ["⏳", "⌛", "🔍", "📚", "🎯"]
        self.PROGRESS_DELAY = 0.5  # seconds

        # Logging setup
        self.setup_logging()

    def setup_logging(self):
        """Initializes the logger for the bot."""
        logger = logging.getLogger('CourseBotLogger')
        logger.setLevel(logging.INFO)
        
        # Handler ko baar baar add hone se rokne ke liye check
        if not logger.handlers:
            file_handler = logging.FileHandler('course_bot.log', encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        self.logger = logger

    def get_search_query_template(self, platform: str = None) -> str:
        """Get search query template for specific platform"""
        if platform:
            return f"{{query}} site:{platform}"
        else:
            platforms = " OR ".join([f"site:{p}" for p in self.SUPPORTED_PLATFORMS])
            return f"{{query}} ({platforms})"
    
    def is_valid_platform(self, url: str) -> bool:
        """Check if URL belongs to supported platform"""
        return any(platform in url.lower() for platform in self.SUPPORTED_PLATFORMS)

