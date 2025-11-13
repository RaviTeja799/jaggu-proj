"""
Test PDF Report Generation - Generate a sample compliance report.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.pdf_report_generator import PDFReportGenerator

print("=" * 70)
print("PDF REPORT GENERATION TEST")
print("=" * 70)
print()

# Initialize PDF generator
print("1. Initializing PDF Report Generator...")
print("-" * 70)
generator = PDFReportGenerator(output_dir="reports")
print("✅ PDF Generator initialized")
print(f"   Output directory: reports/")
print()

# Create sample analysis results
print("2. Creating sample compliance analysis data...")
print("-" * 70)

sample_results = {
    'contract_name': 'Enterprise_Service_Agreement_2025.pdf',
    'compliance_score': 78.5,
    'framework': 'GDPR',
    'processed_at': datetime.now().isoformat(),
    'total_clauses': 32,
    'compliant_clauses': 25,
    'non_compliant_clauses': 7,
    'missing_clauses': 12,
    'risk_distribution': {
        'high': 4,
        'medium': 8,
        'low': 3
    },
    'clause_analysis': [
        {
            'clause_id': 'Clause 3.1',
            'clause_text': 'The Company may collect, process, and store personal data of users for the purposes of service delivery, marketing, and analytics without explicit consent.',
            'is_compliant': False,
            'risk_level': 'high',
            'issues': [
                'Missing lawful basis for data processing',
                'No explicit consent mechanism mentioned',
                'Broad purpose specification violates GDPR Article 5(1)(b)',
                'No mention of data minimization principle'
            ]
        },
        {
            'clause_id': 'Clause 4.2',
            'clause_text': 'Personal data may be transferred to third countries including the United States without adequate safeguards or standard contractual clauses.',
            'is_compliant': False,
            'risk_level': 'high',
            'issues': [
                'Missing standard contractual clauses for data transfers',
                'No adequacy decision mentioned',
                'Violates GDPR Article 44 requirements',
                'Lack of data subject consent for international transfers'
            ]
        },
        {
            'clause_id': 'Clause 5.3',
            'clause_text': 'Data will be retained indefinitely for business purposes and historical records.',
            'is_compliant': False,
            'risk_level': 'medium',
            'issues': [
                'No specific retention period defined',
                'Violates storage limitation principle (Article 5(1)(e))',
                'Missing data deletion procedures'
            ]
        },
        {
            'clause_id': 'Clause 6.1',
            'clause_text': 'The Company implements appropriate technical and organizational measures to ensure data security, including encryption, access controls, and regular security audits.',
            'is_compliant': True,
            'risk_level': 'low',
            'issues': []
        },
        {
            'clause_id': 'Clause 7.4',
            'clause_text': 'Data subjects have the right to access their personal data upon written request within 30 days.',
            'is_compliant': True,
            'risk_level': 'low',
            'issues': []
        },
        {
            'clause_id': 'Clause 8.2',
            'clause_text': 'The Company will notify affected parties within 72 hours of discovering a personal data breach.',
            'is_compliant': True,
            'risk_level': 'low',
            'issues': []
        },
        {
            'clause_id': 'Clause 9.1',
            'clause_text': 'Third-party processors may be engaged without prior notification to data subjects.',
            'is_compliant': False,
            'risk_level': 'medium',
            'issues': [
                'Missing requirement for data processing agreements',
                'No mention of processor liability',
                'Violates transparency principle'
            ]
        },
        {
            'clause_id': 'Clause 10.5',
            'clause_text': 'Data subjects may request deletion of their data, subject to legal retention requirements and legitimate business interests.',
            'is_compliant': True,
            'risk_level': 'low',
            'issues': []
        },
        {
            'clause_id': 'Clause 11.3',
            'clause_text': 'The Company reserves the right to modify this agreement with 15 days notice.',
            'is_compliant': False,
            'risk_level': 'medium',
            'issues': [
                'Insufficient notice period for material changes',
                'No requirement for re-consent after modifications'
            ]
        },
        {
            'clause_id': 'Clause 12.1',
            'clause_text': 'All disputes shall be resolved through binding arbitration in accordance with commercial arbitration rules.',
            'is_compliant': True,
            'risk_level': 'low',
            'issues': []
        },
    ],
    'recommendations': [
        'Add explicit consent mechanisms for all data processing activities, clearly distinguishing between necessary and optional processing',
        'Implement standard contractual clauses (SCCs) for all international data transfers, particularly to non-adequate countries',
        'Define specific, justified retention periods for different data categories in compliance with Article 5(1)(e)',
        'Add transparency requirements for third-party processor engagement and ensure data processing agreements are in place',
        'Expand notice period for material changes to 30 days minimum and require re-consent for significant modifications',
        'Include provisions for data minimization and purpose limitation principles throughout the contract',
        'Add specific clauses addressing data subject rights including portability, rectification, and restriction of processing',
        'Implement privacy by design and by default principles in service delivery as per Article 25'
    ],
    'executive_summary': (
        'This Enterprise Service Agreement demonstrates moderate compliance with GDPR requirements, '
        'achieving an overall score of 78.5%. While the contract includes several positive elements '
        'such as security measures, breach notification procedures, and data subject access rights, '
        'significant gaps remain in critical areas. '
        '\n\n'
        'Key concerns include the absence of explicit consent mechanisms for data processing, '
        'inadequate safeguards for international data transfers, and undefined data retention periods. '
        'These issues present considerable legal risk and could result in regulatory penalties of up to '
        '€20 million or 4% of annual global turnover under GDPR Article 83. '
        '\n\n'
        'Immediate action is recommended to address high-risk compliance gaps, particularly regarding '
        'data transfer mechanisms and consent provisions. The contract requires substantial revisions '
        'before it can be considered fully GDPR-compliant.'
    )
}

print("✅ Sample data created")
print(f"   Contract: {sample_results['contract_name']}")
print(f"   Compliance Score: {sample_results['compliance_score']}%")
print(f"   Framework: {sample_results['framework']}")
print(f"   Total Clauses Analyzed: {sample_results['total_clauses']}")
print()

# Generate PDF report
print("3. Generating PDF Report...")
print("-" * 70)
try:
    pdf_path = generator.generate_compliance_report(sample_results)
    print("✅ PDF report generated successfully!")
    print(f"   Location: {pdf_path}")
    print()
    
    # Check file size
    import os
    file_size = os.path.getsize(pdf_path)
    print(f"   File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
    print()
    
except Exception as e:
    print(f"❌ Error generating PDF: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print()
print("✅ PDF report generation successful!")
print()
print("Report includes:")
print("  • Cover page with key metrics")
print("  • Executive summary")
print("  • Compliance score gauge chart")
print("  • Risk distribution visualization")
print("  • Detailed clause-by-clause analysis")
print("  • Professional recommendations")
print("  • Industry-standard formatting")
print()
print(f"Open the report: {pdf_path}")
print()
print("=" * 70)
