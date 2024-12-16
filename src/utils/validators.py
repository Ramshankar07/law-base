from typing import Dict, Any, Optional
from datetime import datetime


class DataValidator:
    @staticmethod
    def validate_case_data(case_data: Dict) -> Optional[str]:
        """Validate case data structure"""
        required_fields = ["metadata", "content", "citations"]
        for field in required_fields:
            if field not in case_data:
                return f"Missing required field: {field}"

        if not isinstance(case_data["metadata"], dict):
            return "Invalid metadata format"

        return None

    @staticmethod
    def validate_argument(argument: Dict) -> Optional[str]:
        """Validate argument structure"""
        required_fields = ["text", "type", "evidence"]
        for field in required_fields:
            if field not in argument:
                return f"Missing required field: {field}"
        return None
