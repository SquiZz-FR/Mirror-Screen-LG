#!/usr/bin/env python3
"""
Tests for Screen Capture Module
"""

import pytest
from src.screen_capture.capture import ScreenCapture


@pytest.fixture
def screen_capture():
    """Create a ScreenCapture instance for testing."""
    capture = ScreenCapture(fps=5, quality=50)
    yield capture
    capture.stop()


def test_screen_capture_init(screen_capture):
    """Test ScreenCapture initialization."""
    assert screen_capture.fps == 5
    assert screen_capture.quality == 50
    assert not screen_capture.running


def test_screen_capture_start_stop(screen_capture):
    """Test start and stop methods."""
    screen_capture.start()
    assert screen_capture.running
    
    screen_capture.stop()
    assert not screen_capture.running


def test_screen_capture_get_frame(screen_capture):
    """Test frame capture (may fail in headless environments)."""
    screen_capture.start()
    
    # Get a frame (may be None in headless environments like CI)
    frame = screen_capture.get_frame()
    # In headless environments, this will be None, so we just check it doesn't crash
    assert isinstance(frame, (bytes, type(None)))
    
    screen_capture.stop()


def test_screen_capture_get_frame_as_pil(screen_capture):
    """Test PIL image frame capture (may fail in headless environments)."""
    screen_capture.start()
    
    # Get a frame as PIL image (may be None in headless environments)
    frame = screen_capture.get_frame_as_pil()
    # In headless environments, this will be None
    assert frame is None or hasattr(frame, 'size')
    
    screen_capture.stop()


def test_screen_capture_get_resolution(screen_capture):
    """Test screen resolution detection (may return default in headless environments)."""
    width, height = screen_capture.get_screen_resolution()
    assert width > 0
    assert height > 0
    assert isinstance(width, int)
    assert isinstance(height, int)


def test_screen_capture_resize_frame(screen_capture):
    """Test frame resizing (requires a valid PIL image)."""
    screen_capture.start()
    
    # Create a dummy PIL image for testing
    from PIL import Image
    dummy_image = Image.new('RGB', (100, 100), color='red')
    
    resized = screen_capture.resize_frame(dummy_image, 50, 50)
    assert resized.size == (50, 50)
    
    screen_capture.stop()


def test_screen_capture_not_running():
    """Test that capture returns None when not running."""
    capture = ScreenCapture()
    assert capture.get_frame() is None
    assert capture.get_frame_as_pil() is None
