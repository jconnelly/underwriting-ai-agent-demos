automobile-underwriting-system/
├── .env.example                               # Environment variables template
├── .gitignore                                 # Git ignore patterns
├── pyproject.toml                             # Modern Python project configuration
├── requirements.txt                           # Production dependencies
├── README.md                                  # Project overview (moved to root)
│
├── underwriting/                              # Main application package
│   ├── __init__.py                            # Package initialization with exports
│   │
│   ├── core/                                  # Core business logic
│   │   ├── __init__.py                        # Core package exports
│   │   ├── models.py                          # Pydantic data models (existing)
│   │   ├── engine.py                          # Main underwriting engine (existing)
│   │   └── exceptions.py                      # Custom exception classes (new)
│   │
│   ├── ai/                                    # AI/LLM components
│   │   ├── __init__.py                        # AI package exports
│   │   └── prompts.py                         # Prompt templates (existing)
│   │
│   ├── testing/                               # A/B testing framework
│   │   ├── __init__.py                        # Testing package exports
│   │   ├── ab_engine.py                       # A/B test execution (existing)
│   │   └── statistical_analysis.py           # Statistical tests (existing)
│   │
│   ├── data/                                  # Data handling
│   │   ├── __init__.py                        # Data package exports
│   │   └── sample_generator.py                # Test data generation (existing)
│   │
│   ├── cli/                                   # Command-line interfaces
│   │   ├── __init__.py                        # CLI package exports
│   │   ├── basic.py                           # Basic underwriting CLI (existing)
│   │   └── ab_testing.py                      # A/B testing CLI (existing)
│   │
│   └── utils/                                 # Utility functions
│       ├── __init__.py                        # Utils package exports
│       ├── config.py                          # Configuration management (new)
│       └── logging.py                         # Logging setup (new)
│
├── config/                                    # Configuration files
│   └── rules/                                 # Underwriting rules
│       ├── underwriting_rules.json            # Standard rules (existing)
│       ├── underwriting_rules_conservative.json # Conservative rules (existing)
│       └── underwriting_rules_liberal.json    # Liberal rules (existing)
│
├── tests/                                     # Test suite
│   ├── __init__.py                            # Test package marker (new)
│   └── conftest.py                            # Pytest configuration (new)
│
└── docs/                                      # Documentation
    ├── AB_TESTING_GUIDE.md                    # A/B testing guide (existing)
    ├── PROJECT_SUMMARY.md                     # Project summary (existing)
    ├── README.md                              # Detailed documentation (existing)
    └── ab_testing_framework.md                # Framework docs (existing)