import json
import os
from typing import Dict, List, Any
from datetime import datetime, date
from dotenv.main import load_dotenv

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from underwriting_models.models import Applicant, UnderwritingResult, UnderwritingDecision

# Load environment variables
load_dotenv()

class UnderwritingEngine:
    def __init__(self, rules_file: str = "underwriting_rules.json"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        rules_file_dir = os.path.dirname(os.path.abspath(rules_file))
        print(script_dir)
        print(rules_file_dir)
        rules_file = os.path.join(rules_file_dir, "underwriting_rules\\underwriting_rules.json")
        print(f"Loading underwriting rules from: {rules_file}")

        """Initialize the underwriting engine with rules and LLM."""
        self.rules = self._load_rules(rules_file)
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,  # Low temperature for consistent decisions
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.prompt_template = self._create_prompt_template()
    
    def _load_rules(self, rules_file: str) -> Dict[str, Any]:
        """Load underwriting rules from JSON file."""
        with open(rules_file, 'r') as f:
            return json.load(f)
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the LangChain prompt template for underwriting decisions."""
        
        template = """You are an expert automobile insurance underwriter. Your task is to evaluate an insurance applicant based on established underwriting rules and make one of three decisions: ACCEPT, DENY, or ADJUDICATE.

UNDERWRITING RULES:
{rules}

APPLICANT INFORMATION:
{applicant_data}

EVALUATION INSTRUCTIONS:
1. Carefully review the applicant's information against the underwriting rules
2. Check for any HARD STOPS that would result in automatic DENIAL
3. Check for any conditions that require ADJUDICATION (manual review)
4. If no hard stops or adjudication triggers apply, evaluate for ACCEPTANCE
5. Provide your decision with clear reasoning

DECISION CRITERIA:
- DENY: If any hard stop criteria are met (invalid license, multiple DUI, excessive claims, fraud history, extended coverage lapse)
- ADJUDICATE: If moderate risk factors require manual review (moderate violations, single major violation, young driver with violations, high-performance vehicle, poor credit, short coverage lapse)
- ACCEPT: If applicant meets acceptance criteria (clean record, minimal issues within acceptable limits)

RESPONSE FORMAT:
Decision: [ACCEPT/DENY/ADJUDICATE]
Primary Reason: [Brief explanation of the main factor driving the decision]
Triggered Rules: [List specific rule IDs that influenced the decision]
Risk Factors: [List key risk factors identified]
Additional Notes: [Any other relevant observations]

Please evaluate the applicant now:"""

        return PromptTemplate(
            input_variables=["rules", "applicant_data"],
            template=template
        )
    
    def _format_applicant_data(self, applicant: Applicant) -> str:
        """Format applicant data for the LLM prompt."""
        
        # Format primary driver info
        primary_driver = applicant.primary_driver
        driver_info = f"""
PRIMARY DRIVER:
- Name: {primary_driver.first_name} {primary_driver.last_name}
- Age: {primary_driver.age}
- License: {primary_driver.license_number} ({primary_driver.license_state})
- License Status: {primary_driver.license_status.value}
- License Expiration: {primary_driver.license_expiration_date}
"""
        
        # Format violations
        if primary_driver.violations:
            driver_info += "\nVIOLATIONS:\n"
            for violation in primary_driver.violations:
                years_ago = (date.today() - violation.violation_date).days // 365
                driver_info += f"- {violation.violation_type.value} ({violation.violation_date}, {years_ago} years ago)\n"
        else:
            driver_info += "\nVIOLATIONS: None\n"
        
        # Format claims
        if primary_driver.claims:
            driver_info += "\nCLAIMS HISTORY:\n"
            for claim in primary_driver.claims:
                years_ago = (date.today() - claim.claim_date).days // 365
                driver_info += f"- {claim.claim_type.value}: ${claim.claim_amount:,.2f} ({claim.claim_date}, {years_ago} years ago)\n"
        else:
            driver_info += "\nCLAIMS HISTORY: None\n"
        
        # Format vehicles
        vehicle_info = "\nVEHICLES:\n"
        for vehicle in applicant.vehicles:
            vehicle_info += f"- {vehicle.year} {vehicle.make} {vehicle.model} ({vehicle.category.value})\n"
            vehicle_info += f"  VIN: {vehicle.vin}, Value: ${vehicle.value:,.2f}\n"
        
        # Format additional info
        additional_info = f"""
ADDITIONAL INFORMATION:
- Credit Score: {applicant.credit_score if applicant.credit_score else 'Not provided'}
- Prior Insurance Lapse: {applicant.prior_insurance_lapse_days} days
- Fraud History: {'Yes' if applicant.fraud_history else 'No'}
- Additional Drivers: {len(applicant.additional_drivers)}
"""
        
        return driver_info + vehicle_info + additional_info
    
    def _format_rules(self) -> str:
        """Format underwriting rules for the LLM prompt."""
        rules_text = "HARD STOPS (Automatic Denial):\n"
        
        for rule in self.rules["underwriting_rules"]["hard_stops"]["rules"]:
            rules_text += f"- {rule['rule_id']}: {rule['name']} - {rule['description']}\n"
        
        rules_text += "\nADJUDICATION TRIGGERS (Manual Review Required):\n"
        
        for rule in self.rules["underwriting_rules"]["adjudication_triggers"]["rules"]:
            rules_text += f"- {rule['rule_id']}: {rule['name']} - {rule['description']}\n"
        
        rules_text += "\nACCEPTANCE CRITERIA:\n"
        
        for rule in self.rules["underwriting_rules"]["acceptance_criteria"]["rules"]:
            rules_text += f"- {rule['rule_id']}: {rule['name']} - {rule['description']}\n"
        
        return rules_text
    
    def _parse_llm_response(self, response: str, applicant_id: str) -> UnderwritingResult:
        """Parse the LLM response into a structured result."""
        
        lines = response.strip().split('\n')
        decision = UnderwritingDecision.ADJUDICATE  # Default
        reason = "Unable to parse decision"
        triggered_rules = []
        risk_factors = []
        
        for line in lines:
            line = line.strip()
            if line.startswith("Decision:"):
                decision_text = line.split(":", 1)[1].strip().upper()
                if decision_text in ["ACCEPT", "DENY", "ADJUDICATE"]:
                    decision = UnderwritingDecision(decision_text.lower())
            
            elif line.startswith("Primary Reason:"):
                reason = line.split(":", 1)[1].strip()
            
            elif line.startswith("Triggered Rules:"):
                rules_text = line.split(":", 1)[1].strip()
                if rules_text and rules_text != "None":
                    triggered_rules = [r.strip() for r in rules_text.split(",")]
            
            elif line.startswith("Risk Factors:"):
                factors_text = line.split(":", 1)[1].strip()
                if factors_text and factors_text != "None":
                    risk_factors = [f.strip() for f in factors_text.split(",")]
        
        return UnderwritingResult(
            applicant_id=applicant_id,
            decision=decision,
            reason=reason,
            triggered_rules=triggered_rules,
            risk_factors=risk_factors
        )
    
    def evaluate_applicant(self, applicant: Applicant) -> UnderwritingResult:
        """Evaluate an applicant and return underwriting decision."""
        
        # Format the prompt
        formatted_rules = self._format_rules()
        formatted_applicant = self._format_applicant_data(applicant)
        
        prompt = self.prompt_template.format(
            rules=formatted_rules,
            applicant_data=formatted_applicant
        )
        
        # Get LLM response
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            llm_response = response.content
            
            # Parse and return result
            result = self._parse_llm_response(llm_response, applicant.applicant_id)
            return result
            
        except Exception as e:
            # Return error result
            return UnderwritingResult(
                applicant_id=applicant.applicant_id,
                decision=UnderwritingDecision.ADJUDICATE,
                reason=f"Error during evaluation: {str(e)}",
                triggered_rules=[],
                risk_factors=["System Error"]
            )

