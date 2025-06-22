"""
Automobile Insurance Underwriting System

A comprehensive Python package for automobile insurance underwriting with AI-powered
decision making and A/B testing capabilities.

This package provides:
- Core underwriting engine with LLM integration
- A/B testing framework for rule and prompt optimization
- Statistical analysis and business impact assessment
- Sample data generation for testing

Example usage:
    from underwriting.core.engine import UnderwritingEngine
    from underwriting.core.models import Applicant
    
    engine = UnderwritingEngine()
    result = engine.evaluate_applicant(applicant)
"""

__version__ = "1.0.0"
__author__ = "Jeremiah Connelly"
__email__ = "contact@jeremiahconnelly.dev"

# Package-level imports for convenience
from underwriting.core.models import (
    Applicant,
    Driver, 
    Vehicle,
    Violation,
    Claim,
    UnderwritingResult,
    UnderwritingDecision
)

from underwriting.core.engine import UnderwritingEngine
from underwriting.core.exceptions import (
    UnderwritingError,
    RuleValidationError,
    LLMError,
    ConfigurationError
)

# Version information
VERSION_INFO = {
    "major": 1,
    "minor": 0,
    "patch": 0,
    "release": "stable"
}

__all__ = [
    # Core models
    "Applicant",
    "Driver", 
    "Vehicle",
    "Violation",
    "Claim",
    "UnderwritingResult",
    "UnderwritingDecision",
    
    # Core engine
    "UnderwritingEngine",
    
    # Exceptions
    "UnderwritingError",
    "RuleValidationError", 
    "LLMError",
    "ConfigurationError",
    
    # Version info
    "__version__",
    "VERSION_INFO"
]

