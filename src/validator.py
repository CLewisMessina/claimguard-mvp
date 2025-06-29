# src/validator.py

"""
ClaimGuard - Healthcare Claims Validation Engine
Detects pre-payment errors in healthcare claims
"""

import pandas as pd
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ValidationResult:
    """Result of a single validation check"""
    claim_id: str
    error_type: str
    severity: str  # 'HIGH', 'MEDIUM', 'LOW'
    description: str
    recommendation: str
    confidence: float

class ClaimValidator:
    """Core validation engine for healthcare claims"""
    
    def __init__(self):
        self.validation_rules = [
            self.validate_gender_procedure,
            self.validate_age_procedure, 
            self.validate_anatomical_logic,
            self.validate_severity_mismatch
        ]
    
    def validate_gender_procedure(self, claim: Dict) -> List[ValidationResult]:
        """Check for gender-procedure mismatches"""
        errors = []
        
        female_only_procedures = ['59400', '58150', '76801', '81025']
        male_only_procedures = ['55700', '55250', '54150']
        
        age = claim['age']
        gender = claim['gender']
        cpt_code = claim['cpt_code']
        claim_id = str(claim['claim_id'])
        
        if gender == 'M' and cpt_code in female_only_procedures:
            errors.append(ValidationResult(
                claim_id=claim_id,
                error_type="Gender-Procedure Mismatch",
                severity="HIGH",
                description=f"Male patient assigned female-only procedure {cpt_code}",
                recommendation="Verify patient gender or correct procedure code",
                confidence=0.95
            ))
        
        if gender == 'F' and cpt_code in male_only_procedures:
            errors.append(ValidationResult(
                claim_id=claim_id,
                error_type="Gender-Procedure Mismatch", 
                severity="HIGH",
                description=f"Female patient assigned male-only procedure {cpt_code}",
                recommendation="Verify patient gender or correct procedure code",
                confidence=0.95
            ))
        
        return errors
    
    def validate_age_procedure(self, claim: Dict) -> List[ValidationResult]:
        """Check for age-procedure mismatches"""
        errors = []
        
        adult_only_procedures = ['55700', '77067', '45378', '99397']
        pediatric_only_procedures = ['90460', '99381', '99382']
        
        age = claim['age']
        cpt_code = claim['cpt_code']
        claim_id = str(claim['claim_id'])
        
        if age < 18 and cpt_code in adult_only_procedures:
            errors.append(ValidationResult(
                claim_id=claim_id,
                error_type="Age-Procedure Mismatch",
                severity="HIGH", 
                description=f"Patient age {age} inappropriate for adult procedure {cpt_code}",
                recommendation="Verify patient age or select age-appropriate procedure",
                confidence=0.90
            ))
        
        if age >= 18 and cpt_code in pediatric_only_procedures:
            errors.append(ValidationResult(
                claim_id=claim_id,
                error_type="Age-Procedure Mismatch",
                severity="MEDIUM",
                description=f"Adult patient (age {age}) assigned pediatric procedure {cpt_code}",
                recommendation="Consider adult-equivalent procedure code",
                confidence=0.85
            ))
        
        return errors
    
    def validate_anatomical_logic(self, claim: Dict) -> List[ValidationResult]:
        """Check for anatomical procedure-diagnosis mismatches"""
        errors = []
        
        # Body part procedure mappings
        body_procedures = {
            'knee': ['29827', '27447', '27486'],
            'shoulder': ['29826', '23472', '29807'],
            'foot': ['28285', '28296', '28306']
        }
        
        # Body part diagnosis mappings  
        body_diagnoses = {
            'knee': ['M25.561', 'M17.11', 'S83.511A'],
            'shoulder': ['M25.511', 'M75.30', 'S43.006A'],
            'foot': ['M25.571', 'M21.371', 'S92.001A']
        }
        
        cpt_code = claim['cpt_code']
        diagnosis_code = claim['diagnosis_code']
        claim_id = str(claim['claim_id'])
        
        # Find procedure body part
        procedure_body_part = None
        for body_part, procedures in body_procedures.items():
            if cpt_code in procedures:
                procedure_body_part = body_part
                break
        
        # Find diagnosis body part
        diagnosis_body_part = None  
        for body_part, diagnoses in body_diagnoses.items():
            if diagnosis_code in diagnoses:
                diagnosis_body_part = body_part
                break
        
        # Check for mismatch
        if (procedure_body_part and diagnosis_body_part and 
            procedure_body_part != diagnosis_body_part):
            errors.append(ValidationResult(
                claim_id=claim_id,
                error_type="Anatomical Logic Error",
                severity="HIGH",
                description=f"{procedure_body_part.title()} procedure ({cpt_code}) does not match {diagnosis_body_part} diagnosis ({diagnosis_code})",
                recommendation="Verify anatomical consistency between procedure and diagnosis",
                confidence=0.92
            ))
        
        return errors
    
    def validate_severity_mismatch(self, claim: Dict) -> List[ValidationResult]:
        """Check for procedure-diagnosis severity mismatches"""
        errors = []
        
        emergency_procedures = ['36415', '99281', '99291', '99283']
        routine_diagnoses = ['Z00.00', 'Z12.11', 'Z01.419']
        
        cpt_code = claim['cpt_code']
        diagnosis_code = claim['diagnosis_code']
        claim_id = str(claim['claim_id'])
        
        if cpt_code in emergency_procedures and diagnosis_code in routine_diagnoses:
            errors.append(ValidationResult(
                claim_id=claim_id,
                error_type="Severity Mismatch",
                severity="MEDIUM",
                description=f"Emergency procedure ({cpt_code}) inappropriate for routine diagnosis ({diagnosis_code})",
                recommendation="Verify medical necessity or use appropriate procedure code",
                confidence=0.80
            ))
        
        return errors
    
    def validate_single_claim(self, claim: Dict) -> List[ValidationResult]:
        """Validate a single claim against all rules"""
        all_errors = []
        
        for validation_rule in self.validation_rules:
            try:
                errors = validation_rule(claim)
                all_errors.extend(errors)
            except Exception as e:
                # Log error but continue validation
                print(f"Warning: Validation rule {validation_rule.__name__} failed for claim {claim.get('claim_id', 'unknown')}: {e}")
        
        return all_errors
    
    def validate_batch(self, claims_df: pd.DataFrame) -> Dict[str, Any]:
        """Validate a batch of claims and return comprehensive results"""
        start_time = datetime.now()
        
        all_validation_results = []
        duplicate_errors = self.check_duplicates(claims_df)
        
        # Validate each claim
        for _, claim in claims_df.iterrows():
            claim_dict = claim.to_dict()
            validation_results = self.validate_single_claim(claim_dict)
            all_validation_results.extend(validation_results)
        
        # Calculate summary statistics
        total_claims = len(claims_df)
        claims_with_errors = len(set([r.claim_id for r in all_validation_results]))
        error_rate = (claims_with_errors / total_claims) * 100 if total_claims > 0 else 0
        
        # Group errors by type
        error_by_type = {}
        for result in all_validation_results:
            error_type = result.error_type
            if error_type not in error_by_type:
                error_by_type[error_type] = 0
            error_by_type[error_type] += 1
        
        # Group errors by severity
        error_by_severity = {}
        for result in all_validation_results:
            severity = result.severity
            if severity not in error_by_severity:
                error_by_severity[severity] = 0
            error_by_severity[severity] += 1
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'validation_results': all_validation_results,
            'duplicate_errors': duplicate_errors,
            'summary': {
                'total_claims': total_claims,
                'claims_with_errors': claims_with_errors,
                'error_rate_percent': round(error_rate, 2),
                'total_errors': len(all_validation_results),
                'processing_time_seconds': round(processing_time, 3),
                'errors_by_type': error_by_type,
                'errors_by_severity': error_by_severity
            }
        }
    
    def check_duplicates(self, df: pd.DataFrame) -> List[Dict]:
        """Check for duplicate services (same patient, same day, same procedure)"""
        duplicates = df.groupby(['patient_id', 'service_date', 'cpt_code']).size()
        duplicate_groups = duplicates[duplicates > 1]
        
        duplicate_errors = []
        for (patient_id, service_date, cpt_code), count in duplicate_groups.items():
            duplicate_errors.append({
                'patient_id': patient_id,
                'service_date': service_date,
                'cpt_code': cpt_code, 
                'count': count,
                'error_type': 'Duplicate Service',
                'severity': 'MEDIUM',
                'description': f"Procedure {cpt_code} billed {count} times for patient {patient_id} on {service_date}",
                'recommendation': 'Review for legitimate multiple procedures or billing error'
            })
        
        return duplicate_errors

# Utility functions for easy testing
def load_test_data(file_path: str = 'data/synthetic_claims_dataset.csv') -> pd.DataFrame:
    """Load test claims data"""
    return pd.read_csv(file_path)

def run_validation_test():
    """Quick test of the validation engine"""
    print("🔍 Testing ClaimGuard Validation Engine...")
    
    # Load test data
    try:
        df = load_test_data()
        print(f"✅ Loaded {len(df)} test claims")
    except FileNotFoundError:
        print("❌ Test data not found. Run generate_dataset.py first.")
        return
    
    # Initialize validator
    validator = ClaimValidator()
    
    # Run validation
    results = validator.validate_batch(df)
    
    # Display results
    summary = results['summary']
    print(f"\n📊 Validation Results:")
    print(f"   Total Claims: {summary['total_claims']}")
    print(f"   Claims with Errors: {summary['claims_with_errors']}")
    print(f"   Error Rate: {summary['error_rate_percent']}%")
    print(f"   Processing Time: {summary['processing_time_seconds']}s")
    
    print(f"\n🚨 Errors by Type:")
    for error_type, count in summary['errors_by_type'].items():
        print(f"   {error_type}: {count}")
    
    print(f"\n⚠️ Errors by Severity:")
    for severity, count in summary['errors_by_severity'].items():
        print(f"   {severity}: {count}")
    
    # Show a few example errors
    print(f"\n📋 Sample Errors:")
    for i, result in enumerate(results['validation_results'][:3]):
        print(f"   {i+1}. {result.error_type}: {result.description}")

if __name__ == "__main__":
    run_validation_test()
