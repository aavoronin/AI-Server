import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages model information from CSV file"""

    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self.df: Optional[pd.DataFrame] = None
        self._load_models()

    def _load_models(self):
        """Load models from CSV file"""
        try:
            if not self.csv_path.exists():
                logger.error(f"CSV file not found: {self.csv_path}")
                raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

            self.df = pd.read_csv(self.csv_path, on_bad_lines='skip')
            logger.info(f"Loaded {len(self.df)} models from {self.csv_path}")

            # Convert numeric columns, handling errors gracefully
            numeric_columns = [
                'downloads', 'likes', 'SizeB', 'model_size',
                'input_tokens', 'output_tokens'
            ]

            for col in numeric_columns:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise

    def get_all_models(self) -> List[Dict[str, Any]]:
        """Get all models as list of dictionaries"""
        if self.df is None:
            return []

        # Select and rename columns for API response
        columns_to_select = [
            'model_url', 'model_id', 'has_code',
            'input_modalities', 'output_modalities',
            'model_size', 'input_tokens', 'output_tokens',
            'downloads', 'likes', 'SizeB'
        ]

        # Filter to only existing columns
        available_columns = [col for col in columns_to_select if col in self.df.columns]
        result_df = self.df[available_columns].copy()

        records = result_df.to_dict(orient='records')
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                else:
                    try:
                        if float(value) in (float('inf'), float('-inf')):
                            record[key] = None
                    except (ValueError, TypeError):
                        pass

        return records

    def filter_models(
            self,
            input_modalities: Optional[str] = None,
            output_modalities: Optional[str] = None,
            model_size_from: Optional[int] = None,
            model_size_to: Optional[int] = None,
            input_tokens_from: Optional[int] = None,
            input_tokens_to: Optional[int] = None,
            output_tokens_from: Optional[int] = None,
            output_tokens_to: Optional[int] = None,
            downloads_from: Optional[int] = None,
            downloads_to: Optional[int] = None,
            likes_from: Optional[int] = None,
            likes_to: Optional[int] = None,
            size_b_from: Optional[int] = None,
            size_b_to: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Filter models based on modalities and numeric ranges

        Args:
            input_modalities: Comma-separated list of input modalities (e.g., "Text,Image")
            output_modalities: Comma-separated list of output modalities (e.g., "Image,Audio")
            model_size_from/to: Range for model_size
            input_tokens_from/to: Range for input_tokens
            output_tokens_from/to: Range for output_tokens
            downloads_from/to: Range for downloads
            likes_from/to: Range for likes
            size_b_from/to: Range for SizeB

        Returns:
            List of filtered models
        """
        if self.df is None:
            return []

        # Start with a copy of the dataframe
        filtered_df = self.df.copy()

        # Filter by input modalities (must contain ALL specified modalities)
        if input_modalities:
            required_inputs = [m.strip().lower() for m in input_modalities.split(',')]
            mask = filtered_df['input_modalities'].apply(
                lambda x: self._check_modalities(x, required_inputs) if pd.notna(x) else False
            )
            filtered_df = filtered_df[mask]

        # Filter by output modalities (must contain ALL specified modalities)
        if output_modalities:
            required_outputs = [m.strip().lower() for m in output_modalities.split(',')]
            mask = filtered_df['output_modalities'].apply(
                lambda x: self._check_modalities(x, required_outputs) if pd.notna(x) else False
            )
            filtered_df = filtered_df[mask]

        # Apply numeric range filters
        numeric_filters = [
            ('model_size', model_size_from, model_size_to),
            ('input_tokens', input_tokens_from, input_tokens_to),
            ('output_tokens', output_tokens_from, output_tokens_to),
            ('downloads', downloads_from, downloads_to),
            ('likes', likes_from, likes_to),
            ('SizeB', size_b_from, size_b_to),
        ]

        for col_name, from_val, to_val in numeric_filters:
            if col_name in filtered_df.columns:
                if from_val is not None:
                    filtered_df = filtered_df[filtered_df[col_name] >= from_val]
                if to_val is not None:
                    filtered_df = filtered_df[filtered_df[col_name] <= to_val]

        # Select columns for response
        columns_to_select = [
            'model_url', 'model_id', 'has_code',
            'input_modalities', 'output_modalities',
            'model_size', 'input_tokens', 'output_tokens',
            'downloads', 'likes', 'SizeB'
        ]

        available_columns = [col for col in columns_to_select if col in filtered_df.columns]
        result_df = filtered_df[available_columns].copy()

        records = result_df.to_dict(orient='records')
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                else:
                    try:
                        if float(value) in (float('inf'), float('-inf')):
                            record[key] = None
                    except (ValueError, TypeError):
                        pass

        logger.info(f"Filtered to {len(records)} models")

        return records

    def _check_modalities(self, modalities_str: str, required: List[str]) -> bool:
        """
        Check if modalities string contains all required modalities

        Args:
            modalities_str: String like "Text,Image,Audio"
            required: List of required modalities like ["text", "image"]

        Returns:
            True if all required modalities are present
        """
        if not modalities_str:
            return False

        available = [m.strip().lower() for m in modalities_str.split(',')]
        return all(req in available for req in required)