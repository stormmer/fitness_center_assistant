"""Export utilities for session summaries."""

from typing import List
from pathlib import Path


def export_text(path: str, lines: List[str]) -> None:
    """
    Export lines of text to a file.
    
    Args:
        path: File path to write to
        lines: List of strings to write (one per line)
        
    Raises:
        IOError: If file cannot be written
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

