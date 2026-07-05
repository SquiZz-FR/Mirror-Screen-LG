#!/usr/bin/env python3
"""
Mirror Screen LG - Main Application Entry Point

This script is the main entry point for the Mirror Screen LG application.
It initializes the screen capture and streaming server to mirror the PC screen to an LG WebOS TV.
"""

import argparse
import logging
import sys
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Mirror Screen LG - Mirror your PC screen to an LG WebOS TV'
    )
    parser.add_argument(
        '--tv-ip',
        type=str,
        default=None,
        help='IP address of the LG WebOS TV (e.g., 192.168.0.32)'
    )
    parser.add_argument(
        '--passphrase',
        type=str,
        default=None,
        help='Developer mode passphrase (6 characters)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=15,
        help='Frames per second for screen capture (default: 15)'
    )
    parser.add_argument(
        '--quality',
        type=int,
        default=80,
        help='JPEG quality for screen capture (0-100, default: 80)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=9922,
        help='Port for WebOS TV connection (default: 9922)'
    )
    parser.add_argument(
        '--websocket-port',
        type=int,
        default=8080,
        help='Port for WebSocket server (default: 8080)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run in test mode (no TV connection)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    return parser.parse_args()


def setup_logging(debug: bool = False):
    """Configure logging level based on debug flag."""
    level = logging.DEBUG if debug else logging.INFO
    logging.getLogger().setLevel(level)
    logger.debug(f"Logging level set to {level}")


def validate_args(args) -> bool:
    """Validate command line arguments."""
    if not args.test:
        if not args.tv_ip:
            logger.error("TV IP address is required when not in test mode. Use --tv-ip or --test.")
            return False
        if not args.passphrase:
            logger.error("Passphrase is required when not in test mode. Use --passphrase or --test.")
            return False
    
    if args.fps < 1 or args.fps > 60:
        logger.error("FPS must be between 1 and 60.")
        return False
    
    if args.quality < 1 or args.quality > 100:
        logger.error("Quality must be between 1 and 100.")
        return False
    
    return True


def run_screen_mirroring(args):
    """Run the screen mirroring application."""
    from src.screen_capture.capture import ScreenCapture
    from src.network.stream_server import StreamServer
    from src.network.device_connector import DeviceConnector
    
    try:
        # Initialize screen capture
        capture = ScreenCapture(
            fps=args.fps,
            quality=args.quality
        )
        logger.info(f"Screen capture initialized (FPS: {args.fps}, Quality: {args.quality})")
        
        # Initialize WebSocket server
        stream_server = StreamServer(
            host='0.0.0.0',
            port=args.websocket_port
        )
        logger.info(f"WebSocket server initialized on port {args.websocket_port}")
        
        # If not in test mode, connect to TV
        if not args.test:
            connector = DeviceConnector(
                tv_ip=args.tv_ip,
                passphrase=args.passphrase,
                port=args.port
            )
            
            if not connector.connect():
                logger.error("Failed to connect to TV. Exiting.")
                return False
            
            logger.info(f"Connected to TV at {args.tv_ip}")
            
            # Start streaming to TV
            stream_server.set_device_connector(connector)
        
        # Start capture and streaming
        capture.start()
        stream_server.start()
        
        logger.info("Screen mirroring started. Press Ctrl+C to stop.")
        
        # Keep running until interrupted
        try:
            while True:
                frame = capture.get_frame()
                if frame is not None:
                    stream_server.send_frame(frame)
        except KeyboardInterrupt:
            logger.info("Stopping screen mirroring...")
        
        # Cleanup
        capture.stop()
        stream_server.stop()
        if not args.test:
            connector.disconnect()
        
        logger.info("Screen mirroring stopped.")
        return True
        
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return False


def main():
    """Main entry point."""
    args = parse_args()
    setup_logging(args.debug)
    
    logger.debug(f"Starting Mirror Screen LG with args: {args}")
    
    if not validate_args(args):
        sys.exit(1)
    
    success = run_screen_mirroring(args)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
