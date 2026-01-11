"""
Module de configuration et initialisation du package
"""

__version__ = "1.0.0"
__author__ = "BOUKECHOUCH Mohamed"
__description__ = "Property Price Predictor - ML-based real estate price prediction"

from configs.config import *
from src.utils import get_logger

logger = get_logger(__name__)

logger.info(f"Property Price Predictor v{__version__}")
