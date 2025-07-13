"""
Data loader module for ReactRadar brand analysis system.
Handles loading and saving of JSON data files.
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


class DataLoader:
    """Handles loading and saving of data files for the brand analysis system."""
    
    def __init__(self, data_dir: str = "experiment"):
        """
        Initialize the data loader.
        
        Args:
            data_dir: Directory containing the data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def load_json(self, filename: str) -> Any:
        """
        Load data from a JSON file.
        
        Args:
            filename: Name of the JSON file to load
            
        Returns:
            Loaded data from the JSON file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        file_path = self.data_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_json(self, data: Any, filename: str) -> None:
        """
        Save data to a JSON file.
        
        Args:
            data: Data to save
            filename: Name of the JSON file to save to
        """
        file_path = self.data_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_transcript(self) -> str:
        """
        Load the full transcript from the JSON file.
        
        Returns:
            The transcript text
        """
        data = self.load_json("full_transcript.json")
        return data.get("transcript", "")
    
    def load_extracted_brands(self) -> List[str]:
        """
        Load the list of extracted brands.
        
        Returns:
            List of brand names
        """
        return self.load_json("extracted_brands.json")
    
    def load_brand_ratings(self) -> List[Dict[str, Any]]:
        """
        Load brand ratings data.
        
        Returns:
            List of brand rating dictionaries
        """
        return self.load_json("brand_ratings.json")
    
    def load_brand_sentiment(self) -> List[Dict[str, Any]]:
        """
        Load brand sentiment analysis data.
        
        Returns:
            List of brand sentiment dictionaries
        """
        return self.load_json("brand_sentiment_analysis.json")
    
    def load_brand_segmented(self) -> List[Dict[str, Any]]:
        """
        Load segmented brand data.
        
        Returns:
            List of segmented brand dictionaries
        """
        return self.load_json("brand_segmented.json")
    
    def load_brand_insights(self) -> List[Dict[str, Any]]:
        """
        Load brand insight summaries.
        
        Returns:
            List of brand insight dictionaries
        """
        return self.load_json("brand_insight_summaries.json")
    
    def list_available_files(self) -> List[str]:
        """
        List all available JSON files in the data directory.
        
        Returns:
            List of available JSON filenames
        """
        json_files = list(self.data_dir.glob("*.json"))
        return [f.name for f in json_files] 