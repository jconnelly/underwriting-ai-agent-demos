underwriting-ai-agent-demos/
├── .env                                       # Environment variables template
├── .gitignore                                 # Git ignore patterns
├── pyproject.toml                             # Modern Python project configuration
├── requirements.txt                           # Production dependencies
├── README.md                                  # Project overview 
│
├── underwriting/                              # Main application package
│   ├── __init__.py                            # Package initialization with exports
│   │
│   ├── core/                                  # Core business logic
│   │   ├── __init__.py                        # Core package exports
│   │   ├── models.py                          # Pydantic data models
│   │   ├── engine.py                          # Main underwriting engine
│   │   └── exceptions.py                      # Custom exception classes
│   │
│   ├── ai/                                    # AI/LLM components
│   │   ├── __init__.py                        # AI package exports
│   │   └── prompts.py                         # Prompt templates
│   │
│   ├── testing/                               # A/B testing framework
│   │   ├── __init__.py                        # Testing package exports
│   │   ├── ab_engine.py                       # A/B test execution
│   │   └── statistical_analysis.py           # Statistical tests 
│   │
│   ├── data/                                  # Data handling
│   │   ├── __init__.py                        # Data package exports
│   │   └── sample_generator.py                # Test data generation
│   │
│   ├── cli/                                   # Command-line interfaces
│   │   ├── __init__.py                        # CLI package exports
│   │   ├── basic.py                           # Basic underwriting CLI
│   │   └── ab_testing.py                      # A/B testing CLI
│   │
│   └── utils/                                 # Utility functions
│       ├── __init__.py                        # Utils package exports
│       ├── config.py                          # Configuration management
│       └── logging.py                         # Logging setup
│
├── config/                                    # Configuration files
│   └── rules/                                 # Underwriting rules
│       ├── underwriting_rules.json            # Standard rules
│       ├── underwriting_rules_conservative.json # Conservative rules
│       └── underwriting_rules_liberal.json    # Liberal rules
│
├── tests/                                     # Test suite
│   ├── __init__.py                            # Test package marker
│   └── conftest.py                            # Pytest configuration
│
└── docs/                                      # Documentation
    ├── AB_TESTING_GUIDE.md                    # A/B testing guide
    ├── PROJECT_SUMMARY.md                     # Project summary
    ├── README.md                              # Detailed documentation
    └── ab_testing_framework.md                # Framework docs