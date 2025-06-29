# src/generate_dataset.py

import pandas as pd
import random
from datetime import datetime, timedelta

# Define validation rules and code sets
FEMALE_ONLY_PROCEDURES = ['59400', '58150', '76801', '81025']
FEMALE_ONLY_DIAGNOSES = ['O80', 'Z34.90', 'N81.10']

MALE_ONLY_PROCEDURES = ['55700', '55250', '54150']  # Prostate procedures
MALE_ONLY_DIAGNOSES = ['N40.1', 'C61', 'N42.1']    # Prostate conditions

ADULT_ONLY_PROCEDURES = ['55700', '77067', '45378', '99397']  # Adult screening/procedures
PEDIATRIC_ONLY_PROCEDURES = ['90460', '99381', '99382']       # Child vaccines/checkups

EMERGENCY_PROCEDURES = ['36415', '99281', '99291', '99283']
ROUTINE_DIAGNOSES = ['Z00.00', 'Z12.11', 'Z01.419']

# Body part specific codes
KNEE_PROCEDURES = ['29827', '27447', '27486']
SHOULDER_PROCEDURES = ['29826', '23472', '29807']
FOOT_PROCEDURES = ['28285', '28296', '28306']

KNEE_DIAGNOSES = ['M25.561', 'M17.11', 'S83.511A']
SHOULDER_DIAGNOSES = ['M25.511', 'M75.30', 'S43.006A'] 
FOOT_DIAGNOSES = ['M25.571', 'M21.371', 'S92.001A']

def create_problematic_claims():
    """Create synthetic claims with intentional validation errors"""
    claims = []
    claim_id = 1000
    
    # 1. Gender-Procedure Mismatches (8 claims)
    for i in range(4):
        claims.append({
            'claim_id': claim_id,
            'patient_id': f'P{claim_id}',
            'age': random.randint(25, 45),
            'gender': 'M',  # Male
            'cpt_code': random.choice(FEMALE_ONLY_PROCEDURES),
            'diagnosis_code': random.choice(['Z00.00', 'R10.9', 'M79.3']),
            'service_date': '2025-06-15',
            'provider_id': f'PR{random.randint(100, 999)}',
            'charge_amount': random.randint(200, 2000),
            'expected_error': 'Gender-Procedure Mismatch',
            'error_description': 'Male patient with female-only procedure'
        })
        claim_id += 1
    
    for i in range(4):
        claims.append({
            'claim_id': claim_id,
            'patient_id': f'P{claim_id}',
            'age': random.randint(20, 50),
            'gender': 'F',  # Female
            'cpt_code': random.choice(MALE_ONLY_PROCEDURES),
            'diagnosis_code': random.choice(['Z00.00', 'R31.9', 'N39.0']),
            'service_date': '2025-06-16',
            'provider_id': f'PR{random.randint(100, 999)}',
            'charge_amount': random.randint(300, 1500),
            'expected_error': 'Gender-Procedure Mismatch', 
            'error_description': 'Female patient with male-only procedure'
        })
        claim_id += 1
    
    # 2. Age-Procedure Mismatches (6 claims)
    for i in range(3):
        claims.append({
            'claim_id': claim_id,
            'patient_id': f'P{claim_id}',
            'age': random.randint(5, 16),  # Child
            'gender': random.choice(['M', 'F']),
            'cpt_code': random.choice(ADULT_ONLY_PROCEDURES),
            'diagnosis_code': 'Z00.129',  # Routine child health exam
            'service_date': '2025-06-17',
            'provider_id': f'PR{random.randint(100, 999)}',
            'charge_amount': random.randint(150, 800),
            'expected_error': 'Age-Procedure Mismatch',
            'error_description': 'Child with adult-only procedure'
        })
        claim_id += 1
    
    for i in range(3):
        claims.append({
            'claim_id': claim_id,
            'patient_id': f'P{claim_id}',
            'age': random.randint(45, 75),  # Adult
            'gender': random.choice(['M', 'F']),
            'cpt_code': random.choice(PEDIATRIC_ONLY_PROCEDURES),
            'diagnosis_code': random.choice(['Z00.00', 'Z01.419']),
            'service_date': '2025-06-18',
            'provider_id': f'PR{random.randint(100, 999)}',
            'charge_amount': random.randint(100, 300),
            'expected_error': 'Age-Procedure Mismatch',
            'error_description': 'Adult with pediatric procedure'
        })
        claim_id += 1
    
    # 3. Anatomical Logic Errors (6 claims)
    anatomical_mismatches = [
        (KNEE_PROCEDURES, SHOULDER_DIAGNOSES, 'Knee procedure with shoulder diagnosis'),
        (SHOULDER_PROCEDURES, FOOT_DIAGNOSES, 'Shoulder procedure with foot diagnosis'),
        (FOOT_PROCEDURES, KNEE_DIAGNOSES, 'Foot procedure with knee diagnosis')
    ]
    
    for procedures, wrong_diagnoses, description in anatomical_mismatches:
        for i in range(2):
            claims.append({
                'claim_id': claim_id,
                'patient_id': f'P{claim_id}',
                'age': random.randint(25, 65),
                'gender': random.choice(['M', 'F']),
                'cpt_code': random.choice(procedures),
                'diagnosis_code': random.choice(wrong_diagnoses),
                'service_date': '2025-06-19',
                'provider_id': f'PR{random.randint(100, 999)}',
                'charge_amount': random.randint(500, 3000),
                'expected_error': 'Anatomical Logic Error',
                'error_description': description
            })
            claim_id += 1
    
    # 4. Severity Mismatches (4 claims)
    for i in range(4):
        claims.append({
            'claim_id': claim_id,
            'patient_id': f'P{claim_id}',
            'age': random.randint(20, 70),
            'gender': random.choice(['M', 'F']),
            'cpt_code': random.choice(EMERGENCY_PROCEDURES),
            'diagnosis_code': random.choice(ROUTINE_DIAGNOSES),
            'service_date': '2025-06-20',
            'provider_id': f'PR{random.randint(100, 999)}',
            'charge_amount': random.randint(800, 5000),
            'expected_error': 'Severity Mismatch',
            'error_description': 'Emergency procedure with routine diagnosis'
        })
        claim_id += 1
    
    # 5. Duplicate Services (3 claims - same patient, same day, same procedure)
    base_patient = 'P9999'
    duplicate_date = '2025-06-21'
    duplicate_cpt = '99213'
    
    for i in range(3):
        claims.append({
            'claim_id': claim_id,
            'patient_id': base_patient,  # Same patient
            'age': 45,
            'gender': 'F',
            'cpt_code': duplicate_cpt,   # Same procedure
            'diagnosis_code': 'M25.561',
            'service_date': duplicate_date,  # Same date
            'provider_id': 'PR123',
            'charge_amount': 250,
            'expected_error': 'Duplicate Service',
            'error_description': 'Same procedure billed multiple times same day'
        })
        claim_id += 1
    
    # 6. Add some VALID claims for contrast (6 claims)
    valid_combinations = [
        (30, 'F', '99213', 'M25.561'),  # Office visit for knee pain
        (55, 'M', '55700', 'N40.1'),    # Prostate biopsy for enlarged prostate
        (8, 'M', '90460', 'Z00.129'),   # Child vaccination  
        (42, 'F', '77067', 'Z12.31'),   # Mammogram screening
        (35, 'M', '29827', 'M25.561'),  # Knee arthroscopy for knee pain
        (28, 'F', '99214', 'F32.9')     # Office visit for depression
    ]
    
    for age, gender, cpt, diagnosis in valid_combinations:
        claims.append({
            'claim_id': claim_id,
            'patient_id': f'P{claim_id}',
            'age': age,
            'gender': gender,
            'cpt_code': cpt,
            'diagnosis_code': diagnosis,
            'service_date': '2025-06-22',
            'provider_id': f'PR{random.randint(100, 999)}',
            'charge_amount': random.randint(150, 1200),
            'expected_error': 'None',
            'error_description': 'Valid claim - no errors detected'
        })
        claim_id += 1
    
    return claims

def create_validation_rules():
    """Create the validation rule functions"""
    validation_code = '''
def validate_gender_procedure(age, gender, cpt_code, diagnosis_code):
    """Check for gender-procedure mismatches"""
    errors = []
    
    female_only_procedures = ['59400', '58150', '76801', '81025']
    male_only_procedures = ['55700', '55250', '54150']
    
    if gender == 'M' and cpt_code in female_only_procedures:
        errors.append(f"Male patient cannot have female-only procedure {cpt_code}")
    
    if gender == 'F' and cpt_code in male_only_procedures:
        errors.append(f"Female patient cannot have male-only procedure {cpt_code}")
    
    return errors

def validate_age_procedure(age, gender, cpt_code, diagnosis_code):
    """Check for age-procedure mismatches"""
    errors = []
    
    adult_only_procedures = ['55700', '77067', '45378', '99397']
    pediatric_only_procedures = ['90460', '99381', '99382']
    
    if age < 18 and cpt_code in adult_only_procedures:
        errors.append(f"Patient age {age} too young for adult procedure {cpt_code}")
    
    if age >= 18 and cpt_code in pediatric_only_procedures:
        errors.append(f"Patient age {age} too old for pediatric procedure {cpt_code}")
    
    return errors

def validate_anatomical_logic(age, gender, cpt_code, diagnosis_code):
    """Check for anatomical mismatches"""
    errors = []
    
    # Define body part mappings
    body_part_procedures = {
        'knee': ['29827', '27447', '27486'],
        'shoulder': ['29826', '23472', '29807'], 
        'foot': ['28285', '28296', '28306']
    }
    
    body_part_diagnoses = {
        'knee': ['M25.561', 'M17.11', 'S83.511A'],
        'shoulder': ['M25.511', 'M75.30', 'S43.006A'],
        'foot': ['M25.571', 'M21.371', 'S92.001A']
    }
    
    # Find what body part the procedure is for
    procedure_body_part = None
    for body_part, procedures in body_part_procedures.items():
        if cpt_code in procedures:
            procedure_body_part = body_part
            break
    
    # Find what body part the diagnosis is for  
    diagnosis_body_part = None
    for body_part, diagnoses in body_part_diagnoses.items():
        if diagnosis_code in diagnoses:
            diagnosis_body_part = body_part
            break
    
    # Check for mismatch
    if (procedure_body_part and diagnosis_body_part and 
        procedure_body_part != diagnosis_body_part):
        errors.append(f"{procedure_body_part.title()} procedure {cpt_code} does not match {diagnosis_body_part} diagnosis {diagnosis_code}")
    
    return errors

def validate_severity_logic(age, gender, cpt_code, diagnosis_code):
    """Check for severity mismatches"""
    errors = []
    
    emergency_procedures = ['36415', '99281', '99291', '99283']
    routine_diagnoses = ['Z00.00', 'Z12.11', 'Z01.419']
    
    if cpt_code in emergency_procedures and diagnosis_code in routine_diagnoses:
        errors.append(f"Emergency procedure {cpt_code} inappropriate for routine diagnosis {diagnosis_code}")
    
    return errors

def validate_claim(claim_data):
    """Run all validation rules on a single claim"""
    all_errors = []
    
    age = claim_data['age']
    gender = claim_data['gender'] 
    cpt_code = claim_data['cpt_code']
    diagnosis_code = claim_data['diagnosis_code']
    
    # Run all validation functions
    all_errors.extend(validate_gender_procedure(age, gender, cpt_code, diagnosis_code))
    all_errors.extend(validate_age_procedure(age, gender, cpt_code, diagnosis_code))
    all_errors.extend(validate_anatomical_logic(age, gender, cpt_code, diagnosis_code))
    all_errors.extend(validate_severity_logic(age, gender, cpt_code, diagnosis_code))
    
    return all_errors

def check_duplicates(df):
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
            'error': f"Duplicate service: {cpt_code} billed {count} times for patient {patient_id} on {service_date}"
        })
    
    return duplicate_errors
'''
    
    return validation_code

# Generate the dataset
if __name__ == "__main__":
    # Create problematic claims
    claims_data = create_problematic_claims()
    
    # Convert to DataFrame
    df = pd.DataFrame(claims_data)
    
    # Save to CSV in data directory
    df.to_csv('data/synthetic_claims_dataset.csv', index=False)
    
    print(f"Created {len(claims_data)} synthetic claims")
    print("\nError Distribution:")
    error_counts = df['expected_error'].value_counts()
    for error_type, count in error_counts.items():
        print(f"  {error_type}: {count} claims")
    
    print(f"\nDataset saved to 'data/synthetic_claims_dataset.csv'")
    
    # Display sample claims
    print("\nSample Problematic Claims:")
    problematic = df[df['expected_error'] != 'None'].head(3)
    for _, claim in problematic.iterrows():
        print(f"\nClaim {claim['claim_id']}: {claim['error_description']}")
        print(f"  Patient: {claim['age']}yo {claim['gender']}, CPT: {claim['cpt_code']}, Diagnosis: {claim['diagnosis_code']}")
