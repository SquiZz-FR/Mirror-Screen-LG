#!/usr/bin/env python3
"""
Device Connector Module

Handles connection and communication with LG WebOS TV devices.
"""

import logging
import paramiko
from typing import Optional
import time

logger = logging.getLogger(__name__)


class DeviceConnector:
    """
    Manages connection to LG WebOS TV devices.
    
    Uses SSH (port 9922) to communicate with the TV in developer mode.
    
    Attributes:
        tv_ip (str): IP address of the TV.
        passphrase (str): Developer mode passphrase.
        port (int): SSH port (default: 9922).
        ssh_client (paramiko.SSHClient): SSH client instance.
    """
    
    def __init__(self, tv_ip: str, passphrase: str, port: int = 9922):
        """
        Initialize the device connector.
        
        Args:
            tv_ip: IP address of the LG WebOS TV.
            passphrase: Developer mode passphrase (6 characters).
            port: SSH port (default: 9922).
        """
        self.tv_ip = tv_ip
        self.passphrase = passphrase
        self.port = port
        self.ssh_client: Optional[paramiko.SSHClient] = None
        self.connected = False
        logger.info(f"DeviceConnector initialized (TV: {tv_ip}, Port: {port})")
    
    def connect(self, retries: int = 3, timeout: int = 10) -> bool:
        """
        Connect to the LG WebOS TV via SSH.
        
        Args:
            retries: Number of connection attempts (default: 3).
            timeout: Connection timeout in seconds (default: 10).
            
        Returns:
            bool: True if connection succeeded, False otherwise.
        """
        if self.connected:
            logger.warning("Already connected to TV")
            return True
        
        for attempt in range(retries):
            try:
                logger.info(f"Connecting to TV {self.tv_ip} (Attempt {attempt + 1}/{retries})...")
                
                # Create SSH client
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                # Connect with passphrase as password
                self.ssh_client.connect(
                    hostname=self.tv_ip,
                    port=self.port,
                    username='root',
                    password=self.passphrase,
                    timeout=timeout,
                    banner_timeout=5
                )
                
                self.connected = True
                logger.info(f"Successfully connected to TV {self.tv_ip}")
                
                # Test connection with a simple command
                if self._test_connection():
                    return True
                else:
                    self.disconnect()
                    
            except paramiko.AuthenticationException:
                logger.error(f"Authentication failed. Check passphrase for TV {self.tv_ip}")
                return False
            except paramiko.SSHException as e:
                logger.error(f"SSH connection error: {e}")
                if attempt < retries - 1:
                    time.sleep(2)
            except Exception as e:
                logger.error(f"Connection error: {e}", exc_info=True)
                if attempt < retries - 1:
                    time.sleep(2)
        
        logger.error(f"Failed to connect to TV {self.tv_ip} after {retries} attempts")
        return False
    
    def _test_connection(self) -> bool:
        """
        Test the SSH connection with a simple command.
        
        Returns:
            bool: True if test command succeeded.
        """
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command('ls /tmp', timeout=5)
            # Just check if command executed without error
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the TV."""
        if not self.connected:
            return
        
        try:
            if self.ssh_client:
                self.ssh_client.close()
            self.connected = False
            logger.info("Disconnected from TV")
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")
    
    def execute_command(self, command: str, timeout: int = 5) -> Optional[str]:
        """
        Execute a command on the TV via SSH.
        
        Args:
            command: Command to execute.
            timeout: Command timeout in seconds.
            
        Returns:
            str: Command output, or None if failed.
        """
        if not self.connected:
            logger.error("Not connected to TV")
            return None
        
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=timeout)
            return stdout.read().decode('utf-8').strip()
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return None
    
    def launch_app(self, app_id: str, params: dict = None) -> bool:
        """
        Launch an application on the TV using Luna API.
        
        Args:
            app_id: Application ID (e.g., 'com.webos.app.browser').
            params: Optional parameters for the app.
            
        Returns:
            bool: True if app launched successfully.
        """
        if not self.connected:
            return False
        
        try:
            # Use luna-send to launch app
            params_str = ''
            if params:
                import json
                params_str = ' ' + json.dumps(params)
            
            command = f"luna-send -n 1 -f luna://com.webos.applicationmanager/launch '{{\"id\": \"{app_id}\"{params_str}}}'"
            logger.debug(f"Launching app: {command}")
            
            output = self.execute_command(command)
            return output is not None
        except Exception as e:
            logger.error(f"Failed to launch app: {e}")
            return False
    
    def send_to_tv(self, command: str) -> bool:
        """
        Send a command to the TV (wrapper for execute_command).
        
        Args:
            command: Command to send.
            
        Returns:
            bool: True if command succeeded.
        """
        return self.execute_command(command) is not None
    
    def is_connected(self) -> bool:
        """Check if connected to TV."""
        return self.connected
    
    def get_tv_info(self) -> dict:
        """
        Get information about the connected TV.
        
        Returns:
            dict: TV information (model, webOS version, etc.).
        """
        info = {
            'ip': self.tv_ip,
            'port': self.port,
            'connected': self.connected
        }
        
        if self.connected:
            try:
                # Get model info
                model_cmd = "cat /etc/model_info"
                model_output = self.execute_command(model_cmd)
                if model_output:
                    info['model'] = model_output
                
                # Get webOS version
                version_cmd = "cat /etc/webos_version"
                version_output = self.execute_command(version_cmd)
                if version_output:
                    info['webos_version'] = version_output
                    
            except Exception as e:
                logger.error(f"Failed to get TV info: {e}")
        
        return info
