#!/usr/bin/env python3
"""
Screen Capture Module

Handles screen capture, processing, and frame encoding for mirroring.
"""

import logging
import time
import io
from typing import Optional, Tuple
from PIL import ImageGrab, Image

logger = logging.getLogger(__name__)


class ScreenCapture:
    """
    Captures the screen and provides frames for streaming.
    
    Attributes:
        fps (int): Frames per second for capture.
        quality (int): JPEG quality (0-100).
        running (bool): Whether capture is running.
    """
    
    def __init__(self, fps: int = 15, quality: int = 80):
        """
        Initialize the screen capture.
        
        Args:
            fps: Frames per second for capture (default: 15).
            quality: JPEG quality for encoded frames (default: 80).
        """
        self.fps = fps
        self.quality = quality
        self.running = False
        self._last_frame_time = 0
        self._frame_interval = 1.0 / fps if fps > 0 else 0
        logger.info(f"ScreenCapture initialized (FPS: {fps}, Quality: {quality})")
    
    def start(self):
        """Start the screen capture."""
        self.running = True
        logger.info("Screen capture started")
    
    def stop(self):
        """Stop the screen capture."""
        self.running = False
        logger.info("Screen capture stopped")
    
    def get_frame(self) -> Optional[bytes]:
        """
        Capture a frame from the screen and return it as JPEG bytes.
        
        Returns:
            bytes: JPEG-encoded frame, or None if capture failed or not running.
        """
        if not self.running:
            return None
        
        # Rate limiting based on FPS
        current_time = time.time()
        elapsed = current_time - self._last_frame_time
        if elapsed < self._frame_interval:
            time.sleep(self._frame_interval - elapsed)
        
        try:
            # Capture screen using PIL (works on Windows)
            screen = ImageGrab.grab()
            
            # Save to bytes buffer as JPEG
            buffer = io.BytesIO()
            screen.save(buffer, format='JPEG', quality=self.quality, optimize=True)
            
            self._last_frame_time = time.time()
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Failed to capture frame: {e}", exc_info=True)
            return None
    
    def get_frame_as_pil(self):
        """
        Capture a frame from the screen and return it as PIL Image.
        
        Returns:
            PIL.Image: Screen capture, or None if failed.
        """
        if not self.running:
            return None
        
        try:
            return ImageGrab.grab()
        except Exception as e:
            logger.error(f"Failed to capture frame: {e}", exc_info=True)
            return None
    
    def get_screen_resolution(self) -> Tuple[int, int]:
        """
        Get the current screen resolution.
        
        Returns:
            Tuple[int, int]: (width, height) of the screen.
        """
        try:
            screen = ImageGrab.grab()
            return screen.size
        except Exception as e:
            logger.error(f"Failed to get screen resolution: {e}")
            return (1920, 1080)  # Default fallback
    
    def resize_frame(self, pil_image, width: int, height: int):
        """
        Resize a PIL image to the specified dimensions.
        
        Args:
            pil_image: PIL Image to resize.
            width: Target width.
            height: Target height.
            
        Returns:
            PIL.Image: Resized image.
        """
        return pil_image.resize((width, height), resample=Image.Resampling.LANCZOS)
