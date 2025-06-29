# src/ai_explainer.py
"""
ClaimGuard - Enhanced AI-Powered Explanation Generator
Sophisticated healthcare domain expertise with advanced medical reasoning
"""

import openai
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json

# Load environment variables
load_dotenv()

@dataclass
class ExplanationResult:
    """Enhanced AI-generated explanation for a claim error"""
    claim_id: str
    error_type: str
    ai_explanation: str
    medical_reasoning: str
    business_impact: str
    financial_impact: str
    regulatory_concerns: str
    next_steps: str
    confidence: float
    risk_level: str
    fraud_indicators: List[str]

class HealthcareCodeLookup:
    """Healthcare code lookup and context provider"""
    
    # Enhanced CPT code database with medical context
    CPT_CODES = {
        '59400': {
            'description': 'Routine obstetric care including antepartum care, vaginal delivery and postpartum care',
            'category': 'Obstetrics',
            'gender_requirement': 'Female only',
            'typical_age_range': '15-45',
            'complexity': 'High',
            'medical_necessity': 'Pregnancy confirmation required'
        },
        '58150': {
            'description': 'Total abdominal hysterectomy with or without removal of tube(s), with or without removal of ovary(s)',
            'category': 'Gynecologic Surgery',
            'gender_requirement': 'Female only',
            'typical_age_range': '25-65',
            'complexity': 'High',
            'medical_necessity': 'Documented gynecologic pathology'
        },
        '55700': {
            'description': 'Biopsy, prostate; needle or punch, single or multiple, any approach',
            'category': 'Urology',
            'gender_requirement': 'Male only',
            'typical_age_range': '40-80',
            'complexity': 'Moderate',
            'medical_necessity': 'Elevated PSA or abnormal DRE'
        },
        '29827': {
            'description': 'Arthroscopy, knee, surgical; with meniscectomy (medial AND lateral, including any meniscal shaving)',
            'category': 'Orthopedic Surgery',
            'gender_requirement': 'Any',
            'typical_age_range': '16-65',
            'complexity': 'Moderate',
            'medical_necessity': 'MRI-confirmed meniscal tear'
        },
        '99213': {
            'description': 'Office or other outpatient visit for the evaluation and management of an established patient',
            'category': 'Evaluation & Management',
            'gender_requirement': 'Any',
            'typical_age_range': 'Any',
            'complexity': 'Low',
            'medical_necessity': 'Medical condition requiring evaluation'
        },
        '77067': {
            'description': 'Screening mammography, bilateral (2-view study of each breast), including computer-aided detection',
            'category': 'Diagnostic Radiology',
            'gender_requirement': 'Female only',
            'typical_age_range': '40-74',
            'complexity': 'Low',
            'medical_necessity': 'Age-appropriate screening or clinical indication'
        },
        '90460': {
            'description': 'Immunization administration through 18 years of age via any route of administration',
            'category': 'Immunizations',
            'gender_requirement': 'Any',
            'typical_age_range': '0-18',
            'complexity': 'Low',
            'medical_necessity': 'Age-appropriate vaccination schedule'
        }
    }
    
    # Enhanced ICD-10 database with clinical context
    ICD10_CODES = {
        'M25.561': {
            'description': 'Pain in right knee',
            'category': 'Musculoskeletal',
            'body_system': 'Knee',
            'severity': 'Mild to Moderate',
            'typical_procedures': ['29827', '27447', '99213']
        },
        'N40.1': {
            'description': 'Benign prostatic hyperplasia with lower urinary tract symptoms',
            'category': 'Genitourinary',
            'body_system': 'Prostate',
            'severity': 'Moderate',
            'typical_procedures': ['55700', '52630', '99214']
        },
        'Z00.00': {
            'description': 'Encounter for general adult medical examination without abnormal findings',
            'category': 'Routine Care',
            'body_system': 'General',
            'severity': 'Routine',
            'typical_procedures': ['99213', '99396', '99397']
        },
        'O80': {
            'description': 'Encounter for full-term uncomplicated delivery',
            'category': 'Obstetrics',
            'body_system': 'Reproductive',
            'severity': 'Normal',
            'typical_procedures': ['59400', '59409', '59410']
        }
    }

    @classmethod
    def get_cpt_context(cls, cpt_code: str) -> Dict[str, Any]:
        """Get detailed context for CPT code"""
        return cls.CPT_CODES.get(cpt_code, {
            'description': f'CPT code {cpt_code}',
            'category': 'Unknown',
            'gender_requirement': 'Unknown',
            'typical_age_range': 'Unknown',
            'complexity': 'Unknown',
            'medical_necessity': 'Documentation required'
        })
    
    @classmethod
    def get_icd10_context(cls, icd10_code: str) -> Dict[str, Any]:
        """Get detailed context for ICD-10 code"""
        return cls.ICD10_CODES.get(icd10_code, {
            'description': f'ICD-10 code {icd10_code}',
            'category': 'Unknown',
            'body_system': 'Unknown',
            'severity': 'Unknown',
            'typical_procedures': []
        })

class ClaimExplainer:
    """Enhanced AI-powered explanation generator with healthcare domain expertise"""
    
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "800"))  # Increased for detailed explanations
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
        self.code_lookup = HealthcareCodeLookup()
    
    def generate_explanation(self, validation_error: Dict, claim_data: Dict) -> ExplanationResult:
        """Generate comprehensive AI explanation with healthcare domain expertise"""
        
        # Get enhanced medical context
        cpt_context = self.code_lookup.get_cpt_context(claim_data.get('cpt_code', ''))
        icd10_context = self.code_lookup.get_icd10_context(claim_data.get('diagnosis_code', ''))
        
        # Create sophisticated prompt
        prompt = self._create_enhanced_prompt(validation_error, claim_data, cpt_context, icd10_context)
        
        try:
            # Call OpenAI API with enhanced system prompt
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": self._get_healthcare_expert_system_prompt()
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse enhanced response
            explanation_text = response.choices[0].message.content
            sections = self._parse_enhanced_explanation(explanation_text)
            
            # Determine risk level and fraud indicators
            risk_level, fraud_indicators = self._assess_risk_and_fraud(validation_error, claim_data, cpt_context)
            
            return ExplanationResult(
                claim_id=str(claim_data.get('claim_id', 'unknown')),
                error_type=validation_error.get('error_type', 'Unknown Error'),
                ai_explanation=sections.get('explanation', explanation_text),
                medical_reasoning=sections.get('medical_reasoning', 'Medical analysis pending'),
                business_impact=sections.get('business_impact', 'Potential payment error'),
                financial_impact=sections.get('financial_impact', 'Impact assessment required'),
                regulatory_concerns=sections.get('regulatory_concerns', 'Compliance review needed'),
                next_steps=sections.get('next_steps', 'Review and correct'),
                confidence=0.92,  # Higher confidence for enhanced explanations
                risk_level=risk_level,
                fraud_indicators=fraud_indicators
            )
            
        except Exception as e:
            # Enhanced fallback with medical context
            return self._create_enhanced_fallback_explanation(validation_error, claim_data, cpt_context, icd10_context, str(e))
    
    def _get_healthcare_expert_system_prompt(self) -> str:
        """Advanced system prompt establishing healthcare domain expertise"""
        return """You are a senior healthcare claims analyst and certified medical coder with 15+ years of experience in pre-payment claim validation. Your expertise includes:

- Advanced knowledge of CPT-4 and ICD-10-CM coding systems
- Healthcare billing regulations and CMS guidelines
- Medical necessity determination and clinical protocols
- Fraud detection and risk assessment methodologies
- Healthcare finance and reimbursement optimization

When analyzing claims errors, provide sophisticated medical reasoning that demonstrates deep healthcare domain knowledge. Focus on clinical accuracy, regulatory compliance, and business impact with specific financial implications.

Your analysis should be suitable for healthcare administrators, medical directors, and compliance officers who need actionable insights for immediate decision-making."""
    
    def _create_enhanced_prompt(self, validation_error: Dict, claim_data: Dict, cpt_context: Dict, icd10_context: Dict) -> str:
        """Create sophisticated healthcare-focused prompt with medical context"""
        
        error_type = validation_error.get('error_type', 'Unknown')
        description = validation_error.get('description', 'No description')
        
        # Patient and claim details
        age = claim_data.get('age', 'unknown')
        gender = claim_data.get('gender', 'unknown')
        cpt_code = claim_data.get('cpt_code', 'unknown')
        diagnosis = claim_data.get('diagnosis_code', 'unknown')
        charge = claim_data.get('charge_amount', 'unknown')
        
        prompt = f"""
HEALTHCARE CLAIM VALIDATION ERROR ANALYSIS

ERROR CLASSIFICATION:
- Error Type: {error_type}
- Error Description: {description}
- Severity Level: {validation_error.get('severity', 'Unknown')}

PATIENT DEMOGRAPHICS:
- Age: {age} years
- Gender: {gender}

MEDICAL CODING DETAILS:
- Procedure Code (CPT): {cpt_code}
  - Description: {cpt_context.get('description', 'Unknown procedure')}
  - Category: {cpt_context.get('category', 'Unknown')}
  - Gender Requirement: {cpt_context.get('gender_requirement', 'Unknown')}
  - Typical Age Range: {cpt_context.get('typical_age_range', 'Unknown')}
  - Complexity Level: {cpt_context.get('complexity', 'Unknown')}
  - Medical Necessity: {cpt_context.get('medical_necessity', 'Unknown')}

- Diagnosis Code (ICD-10): {diagnosis}
  - Description: {icd10_context.get('description', 'Unknown diagnosis')}
  - Category: {icd10_context.get('category', 'Unknown')}
  - Body System: {icd10_context.get('body_system', 'Unknown')}
  - Severity: {icd10_context.get('severity', 'Unknown')}

FINANCIAL DETAILS:
- Claim Amount: ${charge}
- Provider Impact: Payment delay/denial risk

ANALYSIS REQUIRED:
Provide comprehensive analysis in the following format:

MEDICAL_REASONING: [Clinical explanation of why this combination is problematic from medical/coding perspective, including specific medical knowledge]

BUSINESS_IMPACT: [Immediate operational consequences for the healthcare organization, including workflow disruption]

FINANCIAL_IMPACT: [Specific dollar impact, including potential overpayment, recovery costs, and audit penalties]

REGULATORY_CONCERNS: [CMS compliance issues, coding guideline violations, and audit risk factors]

NEXT_STEPS: [Prioritized action items with specific timelines and responsible parties]

Provide analysis that demonstrates deep healthcare domain expertise and actionable business intelligence."""
        
        return prompt
    
    def _parse_enhanced_explanation(self, explanation_text: str) -> Dict[str, str]:
        """Parse enhanced AI response into structured sections"""
        sections = {
            'explanation': '',
            'medical_reasoning': '',
            'business_impact': '',
            'financial_impact': '',
            'regulatory_concerns': '',
            'next_steps': ''
        }
        
        lines = explanation_text.split('\n')
        current_section = 'explanation'
        
        section_markers = {
            'MEDICAL_REASONING:': 'medical_reasoning',
            'BUSINESS_IMPACT:': 'business_impact',
            'FINANCIAL_IMPACT:': 'financial_impact',
            'REGULATORY_CONCERNS:': 'regulatory_concerns',
            'NEXT_STEPS:': 'next_steps',
            'EXPLANATION:': 'explanation'
        }
        
        for line in lines:
            line = line.strip()
            
            # Check for section markers
            section_found = False
            for marker, section_key in section_markers.items():
                if line.startswith(marker):
                    current_section = section_key
                    content = line.replace(marker, '').strip()
                    if content:
                        sections[current_section] = content
                    section_found = True
                    break
            
            # Add content to current section
            if not section_found and line and current_section:
                if sections[current_section]:
                    sections[current_section] += f" {line}"
                else:
                    sections[current_section] = line
        
        return sections
    
    def _assess_risk_and_fraud(self, validation_error: Dict, claim_data: Dict, cpt_context: Dict) -> tuple[str, List[str]]:
        """Assess risk level and identify potential fraud indicators"""
        
        fraud_indicators = []
        risk_level = "LOW"
        
        error_type = validation_error.get('error_type', '')
        age = claim_data.get('age', 0)
        gender = claim_data.get('gender', '')
        charge = claim_data.get('charge_amount', 0)
        
        # Gender-procedure mismatch analysis
        if 'Gender-Procedure Mismatch' in error_type:
            risk_level = "HIGH"
            fraud_indicators.extend([
                "Biologically impossible procedure-gender combination",
                "Potential identity theft or data entry manipulation",
                "Requires immediate manual verification"
            ])
        
        # Age-procedure mismatch analysis
        elif 'Age-Procedure Mismatch' in error_type:
            if age < 18 and cpt_context.get('gender_requirement') == 'Female only':
                risk_level = "HIGH"
                fraud_indicators.append("Pediatric patient with adult reproductive procedure")
            else:
                risk_level = "MEDIUM"
                fraud_indicators.append("Age-inappropriate procedure selection")
        
        # Anatomical logic errors
        elif 'Anatomical Logic Error' in error_type:
            risk_level = "HIGH"
            fraud_indicators.extend([
                "Anatomically inconsistent procedure-diagnosis pairing",
                "Potential upcoding or unbundling scheme",
                "Clinical documentation likely insufficient"
            ])
        
        # High-value claim additional scrutiny
        if charge > 2000:
            fraud_indicators.append(f"High-value claim (${charge}) requires enhanced review")
            if risk_level == "LOW":
                risk_level = "MEDIUM"
        
        return risk_level, fraud_indicators
    
    def _create_enhanced_fallback_explanation(self, validation_error: Dict, claim_data: Dict, 
                                           cpt_context: Dict, icd10_context: Dict, error_msg: str) -> ExplanationResult:
        """Create enhanced fallback explanation with medical context"""
        
        error_type = validation_error.get('error_type', 'Unknown Error')
        
        # Enhanced fallback explanations with medical reasoning
        enhanced_fallbacks = {
            'Gender-Procedure Mismatch': {
                'explanation': f"Biologically impossible combination: {cpt_context.get('description', 'procedure')} cannot be performed on {claim_data.get('gender', 'unknown')} patients.",
                'medical_reasoning': f"CPT {claim_data.get('cpt_code')} is anatomically restricted to {cpt_context.get('gender_requirement', 'specific gender')} due to biological requirements.",
                'business_impact': 'Immediate claim denial likely. Manual review required to prevent fraudulent payment.',
                'financial_impact': f"Potential ${claim_data.get('charge_amount', 0)} improper payment if processed. Recovery costs estimated at $200-500.",
                'regulatory_concerns': 'CMS guidelines violation. Audit red flag requiring documentation review.',
                'next_steps': '1. Verify patient demographics immediately 2. Review medical records 3. Investigate potential fraud indicators'
            },
            'Age-Procedure Mismatch': {
                'explanation': f"Age {claim_data.get('age')} inappropriate for {cpt_context.get('description', 'procedure')} (typical range: {cpt_context.get('typical_age_range', 'unknown')}).",
                'medical_reasoning': f"Medical necessity questionable. {cpt_context.get('category')} procedures require age-appropriate clinical indication.",
                'business_impact': 'Medical necessity review required. Potential prior authorization needed.',
                'financial_impact': f"Risk of ${claim_data.get('charge_amount', 0)} denial. Appeal costs estimated at $150-300.",
                'regulatory_concerns': 'Age-based coverage criteria may not be met. Documentation of medical necessity required.',
                'next_steps': '1. Review clinical documentation 2. Verify medical necessity 3. Consider age-appropriate alternatives'
            }
        }
        
        fallback = enhanced_fallbacks.get(error_type, {
            'explanation': f"Validation error detected: {validation_error.get('description', 'Unknown error')}",
            'medical_reasoning': 'Medical review recommended for clinical appropriateness assessment.',
            'business_impact': 'Potential payment error requiring manual review and correction.',
            'financial_impact': 'Financial impact assessment pending detailed review.',
            'regulatory_concerns': 'Compliance review recommended to ensure regulatory adherence.',
            'next_steps': 'Manual review recommended with clinical documentation verification.'
        })
        
        risk_level, fraud_indicators = self._assess_risk_and_fraud(validation_error, claim_data, cpt_context)
        
        return ExplanationResult(
            claim_id=str(claim_data.get('claim_id', 'unknown')),
            error_type=error_type,
            ai_explanation=f"[Enhanced Fallback] {fallback['explanation']} (AI Service Unavailable: {error_msg})",
            medical_reasoning=fallback['medical_reasoning'],
            business_impact=fallback['business_impact'],
            financial_impact=fallback['financial_impact'],
            regulatory_concerns=fallback['regulatory_concerns'],
            next_steps=fallback['next_steps'],
            confidence=0.75,  # Lower confidence for fallback but still substantial
            risk_level=risk_level,
            fraud_indicators=fraud_indicators
        )

def test_enhanced_ai_explainer():
    """Test the enhanced AI explainer with sophisticated healthcare analysis"""
    print("🤖 Testing Enhanced ClaimGuard AI Explainer...")
    print("🏥 Healthcare Domain Expert Mode Activated")
    
    try:
        explainer = ClaimExplainer()
        print("✅ OpenAI client initialized with healthcare expertise")
    except Exception as e:
        print(f"❌ Failed to initialize enhanced AI explainer: {e}")
        print("💡 Check your OPENAI_API_KEY in .env file")
        return
    
    # Test with sophisticated validation error
    sample_error = {
        'error_type': 'Gender-Procedure Mismatch',
        'description': 'Male patient assigned female-only obstetric procedure 59400',
        'severity': 'HIGH'
    }
    
    sample_claim = {
        'claim_id': '1001',
        'age': 35,
        'gender': 'M',
        'cpt_code': '59400',
        'diagnosis_code': 'O80',
        'charge_amount': 2500
    }
    
    try:
        result = explainer.generate_explanation(sample_error, sample_claim)
        
        print(f"\n🎯 Enhanced AI Analysis Generated:")
        print(f"📋 Claim ID: {result.claim_id}")
        print(f"🚨 Error Type: {result.error_type}")
        print(f"⚡ Risk Level: {result.risk_level}")
        print(f"\n🏥 MEDICAL REASONING:")
        print(f"   {result.medical_reasoning}")
        print(f"\n💼 BUSINESS IMPACT:")
        print(f"   {result.business_impact}")
        print(f"\n💰 FINANCIAL IMPACT:")
        print(f"   {result.financial_impact}")
        print(f"\n📋 REGULATORY CONCERNS:")
        print(f"   {result.regulatory_concerns}")
        print(f"\n🎯 NEXT STEPS:")
        print(f"   {result.next_steps}")
        print(f"\n🔍 FRAUD INDICATORS:")
        for indicator in result.fraud_indicators:
            print(f"   • {indicator}")
        print(f"\n📊 Confidence: {result.confidence:.0%}")
        
    except Exception as e:
        print(f"❌ Enhanced AI explanation failed: {e}")
        print("🔄 Fallback system would activate with enhanced medical context")

if __name__ == "__main__":
    test_enhanced_ai_explainer()