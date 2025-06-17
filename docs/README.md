# Automobile Insurance Underwriting System

A Python/LangChain application that evaluates automobile insurance applicants using OpenAI's GPT-4 and structured underwriting rules.

## Features

- **Structured Underwriting Rules**: JSON-based rules for hard stops, adjudication triggers, and acceptance criteria
- **LangChain Integration**: Sophisticated prompt templates for consistent LLM evaluation
- **OpenAI GPT-4**: Advanced language model for nuanced underwriting decisions
- **Sample Test Data**: 6 diverse applicants covering accept/deny/adjudicate scenarios
- **A/B Testing Ready**: Framework designed for easy rule modification and testing

## Project Structure

```
underwriting-ai-agent-demo/
├── main.py                          # 🎯 Main entry point
├── pyproject.toml                   # Modern Python config
├── requirements.txt                 # Dependencies
│
├── underwriting/                    # 📦 Main package
│   ├── core/                        # Business logic
│   │   ├── models.py               # Pydantic data models
│   │   ├── engine.py               # LLM underwriting engine
│   │   └── exceptions.py           # Custom exceptions
│   ├── ai/                         # AI components
│   │   └── prompts.py              # LangChain prompt templates
│   ├── testing/                    # A/B testing framework
│   │   ├── ab_engine.py            # Comparison engine
│   │   └── statistical_analysis.py # Statistical testing
│   ├── web/                        # 🌐 Flask web interface
│   │   ├── app.py                  # Flask application
│   │   ├── routes.py               # Web routes
│   │   ├── forms.py                # Web forms
│   │   ├── templates/              # HTML templates
│   │   └── static/                 # CSS, JS, assets
│   ├── cli/                        # Command-line interfaces
│   ├── data/                       # Sample data and generators
│   └── utils/                      # Utilities and helpers
│
├── config/rules/                   # 📋 Underwriting rules
│   ├── underwriting_rules.json    # Standard rules
│   ├── underwriting_rules_conservative.json
│   └── underwriting_rules_liberal.json
│
├── tests/                          # 🧪 Test suite
└── docs/                           # 📚 Documentation
```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set OpenAI API Key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run Tests**:
   ```bash
   python main.py --test
   ```

## Usage

### Full Test Suite
```bash
python main.py --test
```
Runs all 6 sample applicants through the underwriting engine with expected results validation.

### Interactive Mode
```bash
python main.py --interactive
```
Allows manual selection and evaluation of individual applicants.

### Default Mode
```bash
python main.py
```
Runs the full test suite with interactive pauses between applicants.

## Sample Applicants

The system includes 6 carefully designed test cases:

### Accept Cases (2)
- **APP001**: Clean record mature driver (39 years old, no violations/claims)
- **APP002**: Good driver with minimal issues (46 years old, 1 minor violation, 1 not-at-fault claim)

### Deny Cases (2)  
- **APP003**: Multiple DUI violations (hard stop rule)
- **APP004**: Extended coverage lapse + excessive claims (hard stop rule)

### Adjudicate Cases (2)
- **APP005**: Young driver with violations (21 years old, 2 violations)
- **APP006**: Single major violation requiring review (reckless driving)

## Underwriting Rules

The system uses structured JSON rules covering:

- **Hard Stops**: Automatic denial criteria (invalid license, multiple DUI, excessive claims, fraud, extended lapse)
- **Adjudication Triggers**: Manual review requirements (moderate violations, young drivers, high-performance vehicles, poor credit)
- **Acceptance Criteria**: Automatic approval conditions (clean records, minimal issues)

## A/B Testing Framework

The system is designed for easy A/B testing scenarios:

1. **Rule Modifications**: Edit `underwriting_rules.json` to change thresholds
2. **Prompt Variations**: Modify templates in `underwriting_engine.py`
3. **Business Logic Changes**: Update decision criteria and factors

## Example Output

```
=== APP001: Sarah Johnson ===
Age: 39
License Status: valid
Violations: 0
Claims: 0
Credit Score: 750
Coverage Lapse: 0 days

*** UNDERWRITING DECISION ***
Decision: ACCEPT
Reason: Clean record mature driver
Expected: ACCEPT | Actual: ACCEPT | ✓ MATCH
```

## Dependencies

- **langchain**: LLM application framework
- **langchain-openai**: OpenAI integration for LangChain
- **openai**: OpenAI API client
- **pydantic**: Data validation and modeling
- **python-dotenv**: Environment variable management

## Future Enhancements

- Web interface for real-time testing
- Database integration for applicant storage
- Advanced analytics and reporting
- Integration with external data sources (MVR, credit bureaus)
- Machine learning model comparison
- Regulatory compliance tracking

