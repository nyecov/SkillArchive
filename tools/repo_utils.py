"""
Repository Utilities (repo_utils.py)
----------------------------------
Standardized utility functions for high-integrity repository maintenance.
This module provides shared logic for logging, frontmatter parsing, and atomic file I/O.
"""

import os
import sys
import logging
import yaml
import re
import uuid
from pathlib import Path
from typing import Dict, Any, Optional

def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """Sets up a standardized logger for the toolset."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        # Professional format: Timestamp | Level | Message
        formatter = logging.Formatter('%(asctime)s | %(levelname)-7s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger

def get_frontmatter(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Safely extracts and parses YAML frontmatter from a markdown file.
    
    Args:
        file_path: The Path to the markdown file.
        
    Returns:
        A dictionary of the frontmatter content, or None if no valid frontmatter is found.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match frontmatter between --- and ---
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not fm_match:
            return None
            
        data = yaml.safe_load(fm_match.group(1))
        return data if isinstance(data, dict) else None
    except Exception as e:
        logging.error(f"Failed to parse frontmatter in {file_path}: {e}")
        return None

def atomic_write(file_path: Path, content: str):
    """
    Writes content to a file using an atomic write-and-rename pattern.
    
    Args:
        file_path: The target Path to write to.
        content: The string content to write.
    """
    temp_path = file_path.with_suffix(file_path.suffix + ".tmp")
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
            # Ensure data hits disk BEFORE closing
            f.flush()
            os.fsync(f.fileno())
        
        # Atomic swap
        if os.path.exists(file_path):
            os.remove(file_path)
        os.rename(temp_path, file_path)
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise e

def is_valid_uuid4(val: str) -> bool:
    """Verifies if a string is a valid UUIDv4."""
    try:
        uuid_obj = uuid.UUID(str(val), version=4)
        return str(uuid_obj) == str(val)
    except ValueError:
        return False
