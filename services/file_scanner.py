import os
from typing import List


class FileScanner:
    @staticmethod
    def scan_folder(folder_path: str, extensions: List[str], include_subfolders: bool = False) -> List[str]:
        if not folder_path or not extensions:
            return []

        # Normalise caller-supplied extensions (callers may pass upper/dotless).
        normalised = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in extensions}

        files = []

        if include_subfolders:
            # Scan all subfolders
            for root, _, filenames in os.walk(folder_path):
                for filename in filenames:
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in normalised:
                        files.append(os.path.join(root, filename))
        else:
            # Only scan the specified folder, not subfolders
            try:
                entries = os.listdir(folder_path)
            except (OSError, PermissionError):
                return []
            for filename in entries:
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in normalised:
                        files.append(full_path)
        
        return files
    
    @staticmethod
    def get_extension(filename: str) -> str:
        return os.path.splitext(filename)[1].lower()
    
    @staticmethod
    def get_category(extension: str, categories: dict) -> str:
        for category, extensions in categories.items():
            if extension in extensions:
                return category
        return "Other"
