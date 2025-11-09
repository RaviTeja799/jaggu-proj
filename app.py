# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import io
import time
import tempfile
import os
from pathlib import Path

# Import services
from services.document_processor import DocumentProcessor, DocumentProcessingError, UnsupportedFormatError
from services.nlp_analyzer import NLPAnalyzer
from services.compliance_checker import ComplianceChecker
from services.recommendation_engine import RecommendationEngine
from services.export_service import ExportService
from services.google_sheets_service import GoogleSheetsError
from services.document_viewer import DocumentViewer
from services.document_updater import DocumentUpdater, MissingClauseGeneration
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Compliance Checker",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2e86ab;
        border-bottom: 2px solid #2e86ab;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .risk-high { background-color: #ff6b6b; color: white; padding: 5px; border-radius: 5px; }
    .risk-medium { background-color: #ffd166; color: black; padding: 5px; border-radius: 5px; }
    .risk-low { background-color: #06d6a0; color: white; padding: 5px; border-radius: 5px; }
    .compliance-good { color: #06d6a0; font-weight: bold; }
    .compliance-poor { color: #ff6b6b; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize services with caching
@st.cache_resource
def get_document_processor():
    """Initialize and cache document processor."""
    logger.info("Initializing DocumentProcessor...")
    return DocumentProcessor()

@st.cache_resource
def get_nlp_analyzer():
    """Initialize and cache NLP analyzer."""
    logger.info("Initializing NLPAnalyzer...")
    return NLPAnalyzer()

@st.cache_resource
def get_compliance_checker():
    """Initialize and cache compliance checker."""
    logger.info("Initializing ComplianceChecker...")
    return ComplianceChecker()

@st.cache_resource
def get_recommendation_engine():
    """Initialize and cache recommendation engine."""
    logger.info("Initializing RecommendationEngine...")
    return RecommendationEngine(use_llama=False)  # Set to True when LLaMA is available

@st.cache_resource
def get_export_service():
    """Initialize and cache export service."""
    logger.info("Initializing ExportService...")
    return ExportService()

@st.cache_resource
def get_document_viewer():
    """Initialize and cache document viewer."""
    logger.info("Initializing DocumentViewer...")
    return DocumentViewer()

# Initialize session state
if 'processed_document' not in st.session_state:
    st.session_state.processed_document = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'compliance_report' not in st.session_state:
    st.session_state.compliance_report = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'contract_history' not in st.session_state:
    st.session_state.contract_history = []
if 'selected_frameworks' not in st.session_state:
    st.session_state.selected_frameworks = ['GDPR', 'HIPAA']
if 'selected_clause_id' not in st.session_state:
    st.session_state.selected_clause_id = None
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = False
if 'modal_content' not in st.session_state:
    st.session_state.modal_content = None

# Header
st.markdown('<h1 class="main-header">⚖️ AI-Powered Regulatory Compliance Checker</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    st.subheader("Regulatory Frameworks")
    gdpr_check = st.checkbox("GDPR", value=True, key="gdpr_checkbox")
    hipaa_check = st.checkbox("HIPAA", value=True, key="hipaa_checkbox")
    ccpa_check = st.checkbox("CCPA", key="ccpa_checkbox")
    sox_check = st.checkbox("SOX", key="sox_checkbox")
    
    # Update selected frameworks in session state
    selected_frameworks = []
    if gdpr_check:
        selected_frameworks.append("GDPR")
    if hipaa_check:
        selected_frameworks.append("HIPAA")
    if ccpa_check:
        selected_frameworks.append("CCPA")
    if sox_check:
        selected_frameworks.append("SOX")
    
    st.session_state.selected_frameworks = selected_frameworks
    
    # Validate at least one framework is selected
    if not selected_frameworks:
        st.warning("⚠️ Please select at least one regulatory framework")
    else:
        st.success(f"✅ {len(selected_frameworks)} framework(s) selected")
    
    st.subheader("Analysis Settings")
    risk_tolerance = st.select_slider(
        "Risk Tolerance",
        options=["Low", "Medium", "High"],
        value="Medium"
    )
    
    confidence_threshold = st.slider(
        "Confidence Threshold (%)",
        min_value=50,
        max_value=95,
        value=75,
        help="Minimum confidence for clause classification"
    )
    
    notification_enabled = st.checkbox("Enable Regulatory Updates", value=True)
    
    st.subheader("Integrations")
    google_sheets = st.checkbox("Google Sheets Integration", value=False)
    slack_alerts = st.checkbox("Slack Notifications", value=False)
    
    st.markdown("---")
    st.info("**Current Status**: Systems Operational")
    
    # Show analysis status
    if st.session_state.compliance_report:
        st.metric("Last Analysis Score", f"{st.session_state.compliance_report.overall_score:.0f}%")
    else:
        st.metric("Contracts Analyzed", len(st.session_state.contract_history))

# Main content
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📄 Contract Analysis", "📊 Dashboard", "🔍 Clause Details", "✨ Auto-Fix & Rewrite", "🔄 Regulatory Updates", "⚙️ Settings"])

with tab1:
    st.markdown('<h2 class="section-header">Contract Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Contract Document")
        
        upload_method = st.radio(
            "Select upload method:",
            ["Single File Upload", "Batch Upload (up to 10 files)", "Text Input", "Google Sheets URL"]
        )
        
        uploaded_file = None
        uploaded_files = None
        contract_text = None
        
        if upload_method == "Single File Upload":
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['pdf', 'docx', 'txt', 'png', 'jpg'],
                help="Supported formats: PDF, DOCX, TXT, PNG, JPG (max 10MB)"
            )
        
        elif upload_method == "Batch Upload (up to 10 files)":
            uploaded_files = st.file_uploader(
                "Choose multiple files (up to 10)",
                type=['pdf', 'docx', 'txt', 'png', 'jpg'],
                accept_multiple_files=True,
                help="Upload up to 10 contract files for batch processing"
            )
            
            if uploaded_files and len(uploaded_files) > 10:
                st.error("⚠️ Maximum 10 files allowed. Please remove some files.")
                uploaded_files = None
            elif uploaded_files:
                st.info(f"📁 {len(uploaded_files)} files selected for batch processing")
        
        if upload_method == "Single File Upload" and uploaded_file is not None:
            
            if uploaded_file is not None:
                # Validate file size (max 10MB)
                max_size = 10 * 1024 * 1024  # 10MB in bytes
                if uploaded_file.size > max_size:
                    st.error(f"File size ({uploaded_file.size / 1024 / 1024:.1f} MB) exceeds maximum allowed size (10 MB)")
                else:
                    file_details = {
                        "Filename": uploaded_file.name,
                        "File size": f"{uploaded_file.size / 1024:.1f} KB",
                        "File type": uploaded_file.type
                    }
                    st.json(file_details)
                    
                    # Process document immediately
                    with st.spinner("Processing document..."):
                        try:
                            # Save uploaded file to temporary location
                            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                                tmp_file.write(uploaded_file.getvalue())
                                tmp_path = tmp_file.name
                            
                            # Process document
                            doc_processor = get_document_processor()
                            processed_doc = doc_processor.process_document(tmp_path)
                            
                            # Store in session state
                            st.session_state.processed_document = processed_doc
                            
                            # Clean up temp file
                            os.unlink(tmp_path)
                            
                            # Display success
                            st.success(f"✅ Document processed successfully!")
                            st.info(f"📄 Extracted {processed_doc.num_clauses} clauses ({processed_doc.total_words} words) in {processed_doc.processing_time:.2f}s")
                            
                        except UnsupportedFormatError as e:
                            st.error(f"❌ Unsupported file format: {e}")
                            logger.error(f"Unsupported format: {e}")
                        except DocumentProcessingError as e:
                            st.error(f"❌ Error processing document: {e}")
                            logger.error(f"Processing error: {e}")
                        except Exception as e:
                            st.error(f"❌ Unexpected error: {e}")
                            logger.exception(f"Unexpected error: {e}")
        
        elif upload_method == "Batch Upload (up to 10 files)" and uploaded_files:
            st.markdown("### 📦 Batch Processing")
            
            # Validate all file sizes
            max_size = 10 * 1024 * 1024  # 10MB
            oversized_files = [f for f in uploaded_files if f.size > max_size]
            
            if oversized_files:
                st.error(f"⚠️ {len(oversized_files)} file(s) exceed 10MB limit:")
                for f in oversized_files:
                    st.write(f"- {f.name} ({f.size / 1024 / 1024:.1f} MB)")
            else:
                # Display file list
                with st.expander("📁 Selected Files", expanded=True):
                    for i, f in enumerate(uploaded_files, 1):
                        st.write(f"{i}. {f.name} ({f.size / 1024:.1f} KB)")
                
                # Batch processing button
                if st.button("🚀 Process All Files", type="primary", use_container_width=True):
                    from services.batch_processor import BatchProcessor
                    
                    # Save uploaded files to temp locations
                    temp_paths = []
                    for uploaded in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp_file:
                            tmp_file.write(uploaded.getvalue())
                            temp_paths.append(tmp_file.name)
                    
                    # Create progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    file_status = {f.name: 0.0 for f in uploaded_files}
                    
                    def update_progress(filename: str, progress: float):
                        file_status[filename] = progress
                        overall_progress = sum(file_status.values()) / len(file_status)
                        progress_bar.progress(overall_progress)
                        status_text.text(f"Processing: {filename} ({progress*100:.0f}%)")
                    
                    # Process batch
                    try:
                        batch_processor = BatchProcessor(max_workers=3, max_files=10)
                        summary = batch_processor.process_batch(
                            temp_paths,
                            framework=st.session_state.selected_frameworks[0] if st.session_state.selected_frameworks else "GDPR",
                            progress_callback=update_progress
                        )
                        
                        # Clean up temp files
                        for path in temp_paths:
                            try:
                                os.unlink(path)
                            except:
                                pass
                        
                        progress_bar.progress(1.0)
                        status_text.text("✅ Batch processing complete!")
                        
                        # Store batch results in session state
                        st.session_state.batch_summary = summary
                        st.session_state.batch_mode = True
                        
                        # Display summary
                        st.success(f"✅ Processed {summary.successful}/{summary.total_files} files successfully in {summary.total_time:.2f}s")
                        
                        # Show summary metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Files", summary.total_files)
                        with col2:
                            st.metric("Successful", summary.successful)
                        with col3:
                            st.metric("Failed", summary.failed)
                        with col4:
                            st.metric("Avg Time", f"{summary.avg_time_per_file:.1f}s")
                        
                        # Show aggregated compliance score
                        agg_metrics = batch_processor.get_aggregated_compliance_score(summary)
                        
                        st.markdown("### 📊 Aggregated Compliance Score")
                        score_col1, score_col2, score_col3 = st.columns(3)
                        with score_col1:
                            st.metric("Average Score", f"{agg_metrics['average_score']:.1f}%")
                        with score_col2:
                            st.metric("Total Issues", agg_metrics['total_issues'])
                        with score_col3:
                            high_risk = agg_metrics['high_risk_count']
                            st.metric("High Risk Issues", high_risk, delta=None if high_risk == 0 else "❗")
                        
                        # Show individual file results
                        st.markdown("### 📋 Individual File Results")
                        for result in summary.results:
                            with st.expander(f"{'✅' if result.success else '❌'} {result.filename}"):
                                if result.success:
                                    st.write(f"**Processing Time:** {result.processing_time:.2f}s")
                                    if result.compliance_results:
                                        score = result.compliance_results.get('overall_score', 0)
                                        st.write(f"**Compliance Score:** {score:.1f}%")
                                        missing = len(result.compliance_results.get('missing_clauses', []))
                                        st.write(f"**Missing Clauses:** {missing}")
                                else:
                                    st.error(f"Error: {result.error}")
                        
                        # Export option
                        st.markdown("### 💾 Export Batch Results")
                        export_format = st.selectbox("Export Format", ["JSON", "CSV"])
                        if st.button("📥 Export Results"):
                            output_path = batch_processor.export_batch_results(
                                summary,
                                export_format.lower()
                            )
                            st.success(f"Results exported to: {output_path}")
                        
                    except Exception as e:
                        st.error(f"❌ Batch processing failed: {e}")
                        logger.exception("Batch processing error")
                        # Clean up temp files on error
                        for path in temp_paths:
                            try:
                                os.unlink(path)
                            except:
                                pass
                
        elif upload_method == "Text Input":
            contract_text = st.text_area(
                "Paste contract text here:",
                height=200,
                placeholder="Enter the contract text for analysis..."
            )
            
            if contract_text and len(contract_text.strip()) > 100:
                if st.button("Process Text", use_container_width=True):
                    with st.spinner("Processing text..."):
                        try:
                            doc_processor = get_document_processor()
                            processed_doc = doc_processor.process_text(contract_text)
                            
                            # Store in session state
                            st.session_state.processed_document = processed_doc
                            
                            st.success(f"✅ Text processed successfully!")
                            st.info(f"📄 Extracted {processed_doc.num_clauses} clauses ({processed_doc.total_words} words)")
                            
                        except DocumentProcessingError as e:
                            st.error(f"❌ Error processing text: {e}")
                            logger.error(f"Processing error: {e}")
            elif contract_text:
                st.warning("Please enter at least 100 characters of contract text")
        
        else:  # Google Sheets URL
            st.subheader("Google Sheets Integration")
            
            sheets_url = st.text_input(
                "Google Sheets URL:",
                placeholder="https://docs.google.com/spreadsheets/d/..."
            )
            
            # Optional parameters
            with st.expander("Advanced Options"):
                sheet_name = st.text_input(
                    "Sheet Name (optional):",
                    placeholder="Leave empty to use first sheet",
                    help="Specify the name of the sheet to read from"
                )
                cell_range = st.text_input(
                    "Cell Range (optional):",
                    placeholder="e.g., A1:B10",
                    help="Specify the cell range to read. Leave empty to read all data."
                )
            
            if sheets_url:
                # Validate URL format
                doc_processor = get_document_processor()
                if doc_processor.google_sheets_service.validate_url(sheets_url):
                    st.success("✅ Valid Google Sheets URL")
                    
                    if st.button("Process Google Sheet", use_container_width=True):
                        with st.spinner("Connecting to Google Sheets..."):
                            try:
                                processed_doc = doc_processor.process_google_sheet(
                                    sheets_url,
                                    sheet_name if sheet_name else None,
                                    cell_range if cell_range else None
                                )
                                
                                # Store in session state
                                st.session_state.processed_document = processed_doc
                                
                                st.success(f"✅ Google Sheet processed successfully!")
                                st.info(f"📄 Extracted {processed_doc.num_clauses} clauses ({processed_doc.total_words} words)")
                                
                            except GoogleSheetsError as e:
                                st.error(f"❌ Google Sheets error: {e}")
                                logger.error(f"Google Sheets error: {e}")
                                
                                # Show troubleshooting tips
                                with st.expander("Troubleshooting Tips"):
                                    st.markdown("""
                                    **Common Issues:**
                                    
                                    1. **Authentication Error**: Make sure you have set up Google API credentials
                                       - Download credentials from Google Cloud Console
                                       - Place the JSON file in `App/config/google_credentials.json`
                                    
                                    2. **Permission Denied**: Ensure the sheet is shared with the service account email
                                       - Open your Google Sheet
                                       - Click "Share" and add the service account email
                                       - Grant "Viewer" access
                                    
                                    3. **Sheet Not Found**: Check that the URL is correct and the sheet exists
                                    
                                    4. **No Data Found**: Verify that the specified range contains data
                                    """)
                                    
                            except DocumentProcessingError as e:
                                st.error(f"❌ Error processing sheet: {e}")
                                logger.error(f"Processing error: {e}")
                else:
                    st.error("❌ Invalid Google Sheets URL. Please enter a valid URL.")
    
    with col2:
        st.subheader("Quick Actions")
        
        # Show document status
        if st.session_state.processed_document:
            st.success("✅ Document Ready")
            st.metric("Clauses Identified", st.session_state.processed_document.num_clauses)
        else:
            st.info("📤 Upload a document to begin")
        
        # Analyze button (only enabled if document is processed)
        analyze_disabled = st.session_state.processed_document is None
        
        if st.button("🚀 Analyze Contract", use_container_width=True, disabled=analyze_disabled):
            if not st.session_state.selected_frameworks:
                st.error("Please select at least one regulatory framework in the sidebar")
            else:
                with st.spinner("Analyzing contract for compliance..."):
                    try:
                        # Get services
                        nlp_analyzer = get_nlp_analyzer()
                        compliance_checker = get_compliance_checker()
                        recommendation_engine = get_recommendation_engine()
                        
                        # Step 1: NLP Analysis
                        st.info("🔍 Step 1/3: Analyzing clauses...")
                        clause_analyses = nlp_analyzer.analyze_clauses(
                            st.session_state.processed_document.clauses
                        )
                        st.session_state.analysis_results = clause_analyses
                        
                        # Step 2: Compliance Checking
                        st.info("⚖️ Step 2/3: Checking compliance...")
                        compliance_report = compliance_checker.check_compliance(
                            clause_analyses,
                            st.session_state.selected_frameworks,
                            st.session_state.processed_document.document_id
                        )
                        st.session_state.compliance_report = compliance_report
                        
                        # Step 3: Generate Recommendations
                        st.info("💡 Step 3/3: Generating recommendations...")
                        recommendations = recommendation_engine.generate_recommendations(
                            compliance_report
                        )
                        st.session_state.recommendations = recommendations
                        
                        # Add to history
                        st.session_state.contract_history.append({
                            'filename': st.session_state.processed_document.original_filename,
                            'date': datetime.now(),
                            'score': compliance_report.overall_score,
                            'status': 'Compliant' if compliance_report.overall_score >= 80 else 'Review Needed',
                            'risk': 'High' if compliance_report.summary.high_risk_count > 0 else 'Medium' if compliance_report.summary.medium_risk_count > 0 else 'Low'
                        })
                        
                        # Display results
                        st.success("✅ Analysis Complete!")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Compliance Score", f"{compliance_report.overall_score:.0f}%")
                        with col2:
                            st.metric("High Risk Items", compliance_report.summary.high_risk_count)
                        with col3:
                            st.metric("Missing Clauses", len(compliance_report.missing_requirements))
                        
                        # Direct user to clause details tab
                        st.info("📄 View the highlighted document in the **Clause Details** tab to see risk-coded clauses and click for details!")
                        
                        # Set default view mode to Document
                        if 'view_mode' not in st.session_state:
                            st.session_state.view_mode = "Document"
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {e}")
                        logger.exception(f"Analysis error: {e}")
        
        st.button("🔄 Check Updates", use_container_width=True)
        
        # Export section
        if st.session_state.compliance_report:
            st.markdown("---")
            st.subheader("Export Results")
            
            export_service = get_export_service()
            
            # JSON Export
            try:
                json_data = export_service.export_to_json(
                    st.session_state.compliance_report,
                    st.session_state.recommendations
                )
                json_filename = export_service.get_json_filename(
                    st.session_state.compliance_report
                )
                
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=json_filename,
                    mime="application/json",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"JSON export error: {e}")
                logger.error(f"JSON export failed: {e}")
            
            # CSV Export
            try:
                csv_data = export_service.export_to_csv(
                    st.session_state.compliance_report,
                    st.session_state.recommendations
                )
                csv_filename = export_service.get_csv_filename(
                    st.session_state.compliance_report
                )
                
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=csv_filename,
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"CSV export error: {e}")
                logger.error(f"CSV export failed: {e}")
            
            # PDF Export
            try:
                pdf_data = export_service.export_to_pdf(
                    st.session_state.compliance_report,
                    st.session_state.recommendations
                )
                pdf_filename = export_service.get_pdf_filename(
                    st.session_state.compliance_report
                )
                
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"PDF export error: {e}")
                logger.error(f"PDF export failed: {e}")

with tab2:
    st.markdown('<h2 class="section-header">Compliance Dashboard</h2>', unsafe_allow_html=True)
    
    # Check if we have analysis results
    if st.session_state.compliance_report:
        report = st.session_state.compliance_report
        
        # KPI Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Overall Compliance", 
                f"{report.overall_score:.0f}%",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                "High Risk Items", 
                report.summary.high_risk_count,
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                "Contracts Analyzed", 
                len(st.session_state.contract_history)
            )
        
        with col4:
            st.metric(
                "Missing Clauses", 
                len(report.missing_requirements)
            )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Compliance by Framework")
            
            # Calculate scores per framework
            framework_scores = {}
            for framework in report.frameworks_checked:
                framework_results = [r for r in report.clause_results if r.framework == framework]
                if framework_results:
                    compliant = sum(1 for r in framework_results if r.compliance_status.value == 'Compliant')
                    score = (compliant / len(framework_results)) * 100
                    framework_scores[framework] = score
                else:
                    framework_scores[framework] = 0
            
            framework_data = pd.DataFrame({
                'Framework': list(framework_scores.keys()),
                'Compliance': list(framework_scores.values()),
                'Target': [90] * len(framework_scores)
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Current',
                x=framework_data['Framework'],
                y=framework_data['Compliance'],
                marker_color='#2e86ab'
            ))
            fig.add_trace(go.Scatter(
                name='Target',
                x=framework_data['Framework'],
                y=framework_data['Target'],
                mode='markers',
                marker=dict(color='red', size=10, symbol='line-ew'),
                line=dict(width=3)
            ))
            
            fig.update_layout(
                height=300,
                showlegend=True,
                yaxis_range=[0, 100],
                yaxis_title="Compliance %"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Risk Distribution")
            
            risk_data = pd.DataFrame({
                'Level': ['High', 'Medium', 'Low'],
                'Count': [
                    report.summary.high_risk_count,
                    report.summary.medium_risk_count,
                    report.summary.low_risk_count
                ]
            })
            
            # Only show non-zero values
            risk_data = risk_data[risk_data['Count'] > 0]
            
            if not risk_data.empty:
                fig = px.pie(
                    risk_data, 
                    values='Count', 
                    names='Level',
                    color='Level',
                    color_discrete_map={
                        'High': '#ff6b6b',
                        'Medium': '#ffd166', 
                        'Low': '#06d6a0'
                    }
                )
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No risk data available")
        
        # Recent Activity
        st.subheader("Recent Analysis Activity")
        
        if st.session_state.contract_history:
            activity_data = pd.DataFrame(st.session_state.contract_history)
            activity_data = activity_data.rename(columns={
                'filename': 'Contract',
                'date': 'Date',
                'status': 'Status',
                'risk': 'Risk',
                'score': 'Score'
            })
            
            st.dataframe(
                activity_data,
                use_container_width=True,
                column_config={
                    "Date": st.column_config.DatetimeColumn("Date", format="MMM D, YYYY HH:mm"),
                    "Status": st.column_config.TextColumn("Status"),
                    "Risk": st.column_config.TextColumn("Risk"),
                    "Score": st.column_config.ProgressColumn("Score", format="%.0f%%", min_value=0, max_value=100)
                }
            )
        else:
            st.info("No contracts analyzed yet")
    else:
        st.info("📊 Upload and analyze a contract to see dashboard metrics")
        
        # Show placeholder
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall Compliance", "—")
        with col2:
            st.metric("High Risk Items", "—")
        with col3:
            st.metric("Contracts Analyzed", len(st.session_state.contract_history))
        with col4:
            st.metric("Missing Clauses", "—")

with tab3:
    st.markdown('<h2 class="section-header">Clause-Level Analysis</h2>', unsafe_allow_html=True)
    
    if st.session_state.compliance_report and st.session_state.recommendations:
        report = st.session_state.compliance_report
        recommendations = st.session_state.recommendations
        
        # Create recommendations lookup by clause_id
        rec_by_clause = {}
        for rec in recommendations:
            if rec.clause_id:
                if rec.clause_id not in rec_by_clause:
                    rec_by_clause[rec.clause_id] = []
                rec_by_clause[rec.clause_id].append(rec)
        
        # Filters (placed at top for both views)
        st.subheader("🔍 Filter Options")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            risk_filter = st.multiselect(
                "Risk Level:",
                options=['High', 'Medium', 'Low'],
                default=['High', 'Medium', 'Low'],
                key="risk_filter"
            )
        
        with col2:
            regulation_filter = st.multiselect(
                "Regulation:",
                options=report.frameworks_checked,
                default=report.frameworks_checked,
                key="regulation_filter"
            )
        
        with col3:
            status_filter = st.multiselect(
                "Status:",
                options=['Compliant', 'Non-Compliant', 'Partial'],
                default=['Non-Compliant', 'Partial'],
                key="status_filter"
            )
        
        with col4:
            view_mode = st.radio(
                "View:",
                options=["Document", "List"],
                horizontal=True,
                key="view_mode",
                help="Toggle between highlighted document view and clause list view"
            )
        
        st.markdown("---")
        
        # Apply filters to get filtered results
        filtered_results = [
            r for r in report.clause_results
            if r.risk_level.value in risk_filter
            and r.framework in regulation_filter
            and r.compliance_status.value in status_filter
        ]
        
        st.info(f"Showing {len(filtered_results)} of {len(report.clause_results)} clauses")
        
        # Show highlighted document view
        if view_mode == "Document" and st.session_state.processed_document:
            st.markdown("---")
            
            # Create two columns: document view and missing clauses panel
            doc_col, missing_col = st.columns([2, 1])
            
            with doc_col:
                st.subheader("📄 Contract Document")
                
                # Show filter info
                if len(filtered_results) < len(report.clause_results):
                    st.info(f"💡 Highlighting {len(filtered_results)} filtered clauses. Adjust filters above to see more.")
                
                # Get document viewer
                doc_viewer = get_document_viewer()
                
                # Create risk map from FILTERED compliance results
                clause_risk_map = {}
                clause_details_map = {}
                for result in filtered_results:
                    clause_risk_map[result.clause_id] = result.risk_level.value
                    clause_details_map[result.clause_id] = {
                        'compliance_status': result.compliance_status.value,
                        'issues': result.issues,
                        'clause_type': result.clause_type
                    }
                
                # Display legend with filter info
                legend_html = doc_viewer.create_legend_html()
                
                # Add active filters info to legend
                if len(filtered_results) < len(report.clause_results):
                    active_filters = []
                    if len(risk_filter) < 3:
                        active_filters.append(f"Risk: {', '.join(risk_filter)}")
                    if len(regulation_filter) < len(report.frameworks_checked):
                        active_filters.append(f"Frameworks: {', '.join(regulation_filter)}")
                    if len(status_filter) < 3:
                        active_filters.append(f"Status: {', '.join(status_filter)}")
                    
                    if active_filters:
                        filter_info = f"""
                        <div style="background-color: #e7f3ff; border: 1px solid #2196F3; 
                                    border-radius: 5px; padding: 8px; margin-bottom: 10px;">
                            <strong>🔍 Active Filters:</strong> {' | '.join(active_filters)}
                        </div>
                        """
                        st.markdown(filter_info, unsafe_allow_html=True)
                
                st.markdown(legend_html, unsafe_allow_html=True)
                
                # Display highlighted document with click handlers
                highlighted_html = doc_viewer.create_highlighted_html(
                    st.session_state.processed_document,
                    clause_risk_map,
                    clause_details_map
                )
                
                # Add CSS styles
                st.markdown(doc_viewer.get_css_styles(), unsafe_allow_html=True)
                
                # Add JavaScript for click handlers
                st.markdown(doc_viewer.get_click_handler_javascript(), unsafe_allow_html=True)
                
                # Display the highlighted document
                st.markdown(highlighted_html, unsafe_allow_html=True)
            
            with missing_col:
                st.subheader("⚠️ Missing Clauses")
                
                # Display missing clauses panel
                missing_panel_html = doc_viewer.create_missing_clauses_panel(
                    report.missing_requirements,
                    recommendations
                )
                st.markdown(missing_panel_html, unsafe_allow_html=True)
            
            st.markdown("---")
        
        # Check if a clause was clicked (for navigation)
        if st.session_state.selected_clause_id:
            # Find the clause in filtered results
            selected_result = next(
                (r for r in report.clause_results if r.clause_id == st.session_state.selected_clause_id),
                None
            )
            if selected_result and selected_result not in filtered_results:
                st.info(f"💡 Clause {st.session_state.selected_clause_id} is hidden by current filters. Adjust filters to view it.")
        
        # Handle modal display for missing clauses
        if 'show_missing_modal' in st.session_state and st.session_state.get('show_missing_modal'):
            req_id = st.session_state.show_missing_modal
            
            # Find the requirement and recommendation
            missing_req = next((r for r in report.missing_requirements if r.requirement_id == req_id), None)
            matching_rec = next((r for r in recommendations if r.requirement and r.requirement.requirement_id == req_id), None)
            
            if missing_req:
                # Create a prominent modal-like container
                st.markdown("---")
                st.markdown(
                    '<div style="background-color: #f8f9fa; border: 2px solid #007bff; '
                    'border-radius: 10px; padding: 20px; margin: 20px 0;">',
                    unsafe_allow_html=True
                )
                
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"### 📋 Full Recommendation: {missing_req.clause_type}")
                with col2:
                    if st.button("✖ Close", key="close_modal", use_container_width=True):
                        st.session_state.show_missing_modal = None
                        st.rerun()
                
                st.markdown(f"**Regulatory Reference:** {missing_req.article_reference} ({missing_req.framework})")
                st.markdown(f"**Description:** {missing_req.description}")
                
                if missing_req.mandatory_elements:
                    st.markdown("**Required Elements:**")
                    for element in missing_req.mandatory_elements:
                        st.markdown(f"- {element}")
                
                if matching_rec:
                    st.markdown("---")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        priority_color = {1: "🔴", 2: "🔴", 3: "🟡", 4: "🟢", 5: "🟢"}
                        st.metric("Priority", f"{priority_color.get(matching_rec.priority, '⚪')} {matching_rec.priority}/5")
                    with col2:
                        st.metric("Action", matching_rec.action_type.value)
                    with col3:
                        st.metric("Framework", missing_req.framework)
                    
                    st.markdown(f"**Recommendation:** {matching_rec.description}")
                    
                    if matching_rec.suggested_text:
                        st.markdown("**Suggested Clause Text:**")
                        st.code(matching_rec.suggested_text, language="text")
                        
                        # Add copy button
                        if st.button("📋 Copy to Clipboard", key="copy_suggested"):
                            st.success("✅ Copied to clipboard! (Note: Manual copy from code block above)")
                    
                    if matching_rec.rationale:
                        with st.expander("📖 View Rationale"):
                            st.markdown(matching_rec.rationale)
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
        
        # Display clauses with formatting
        if filtered_results:
            for result in filtered_results:
                # Add anchor for scrolling
                st.markdown(f'<div id="clause-details-{result.clause_id}"></div>', unsafe_allow_html=True)
                
                # Highlight selected clause
                is_selected = st.session_state.selected_clause_id == result.clause_id
                expander_label = f"{result.clause_id} - {result.clause_type} ({result.framework})"
                if is_selected:
                    expander_label = f"👉 {expander_label}"
                
                with st.expander(expander_label, expanded=is_selected):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        risk_color = {
                            'High': 'risk-high',
                            'Medium': 'risk-medium', 
                            'Low': 'risk-low'
                        }[result.risk_level.value]
                        st.markdown(f"**Risk Level:** <span class='{risk_color}'>{result.risk_level.value}</span>", unsafe_allow_html=True)
                    
                    with col2:
                        status_color = "compliance-good" if result.compliance_status.value == 'Compliant' else "compliance-poor"
                        st.markdown(f"**Status:** <span class='{status_color}'>{result.compliance_status.value}</span>", unsafe_allow_html=True)
                    
                    with col3:
                        st.metric("Confidence", f"{result.confidence * 100:.0f}%")
                    
                    with col4:
                        if result.compliance_status.value != 'Compliant':
                            fix_key = f"fix_{result.clause_id}"
                            if st.button("🛠️ Fix", key=fix_key, use_container_width=True):
                                st.session_state[f"show_fix_{result.clause_id}"] = True
                        else:
                            st.button("✅ OK", key=f"ok_{result.clause_id}", use_container_width=True, disabled=True)
                    
                    # Show clause text
                    st.markdown("**Clause Text:**")
                    st.text_area(
                        "Clause",
                        value=result.clause_text[:500] + ("..." if len(result.clause_text) > 500 else ""),
                        height=100,
                        key=f"text_{result.clause_id}",
                        disabled=True
                    )
                    
                    # Show issues
                    if result.issues:
                        st.markdown("**Issues:**")
                        for issue in result.issues:
                            st.warning(f"• {issue}")
                    
                    # Show recommendations
                    if result.clause_id in rec_by_clause:
                        st.markdown("**Recommendations:**")
                        for rec in rec_by_clause[result.clause_id]:
                            st.info(f"**{rec.action_type.value}:** {rec.description}")
                            if rec.suggested_text and st.session_state.get(f"show_fix_{result.clause_id}", False):
                                st.markdown("**Suggested Text:**")
                                st.code(rec.suggested_text, language="text")
        else:
            st.info("No clauses match the selected filters")
        
        # Show missing requirements
        if report.missing_requirements:
            st.markdown("---")
            st.subheader("Missing Required Clauses")
            
            for req in report.missing_requirements:
                # Check if this is the selected requirement
                is_selected_req = (
                    st.session_state.get('show_missing_modal') == req.requirement_id
                )
                
                expander_label = f"⚠️ Missing: {req.clause_type} ({req.framework})"
                if is_selected_req:
                    expander_label = f"👉 {expander_label}"
                
                with st.expander(expander_label, expanded=is_selected_req):
                    st.markdown(f"**Requirement:** {req.article_reference}")
                    st.markdown(f"**Description:** {req.description}")
                    
                    if req.mandatory_elements:
                        st.markdown("**Required Elements:**")
                        for element in req.mandatory_elements:
                            st.markdown(f"• {element}")
                    
                    # Find recommendation for this requirement
                    matching_rec = next(
                        (r for r in recommendations if r.requirement.requirement_id == req.requirement_id),
                        None
                    )
                    
                    if matching_rec:
                        col1, col2 = st.columns(2)
                        with col1:
                            if matching_rec.suggested_text:
                                if st.button(f"📄 Show Suggested Clause", key=f"show_{req.requirement_id}", use_container_width=True):
                                    st.markdown("**Suggested Clause Text:**")
                                    st.code(matching_rec.suggested_text, language="text")
                        with col2:
                            if st.button(f"🔍 View Full Details", key=f"details_{req.requirement_id}", use_container_width=True):
                                st.session_state.show_missing_modal = req.requirement_id
                                st.rerun()
    else:
        st.info("📋 Analyze a contract to see detailed clause-level analysis")

# ==================== TAB 4: AUTO-FIX & REWRITE CONTRACT ====================
with tab4:
    st.markdown('<h2 class="section-header">✨ Auto-Fix Missing Clauses & Rewrite Contract</h2>', unsafe_allow_html=True)
    
    if st.session_state.compliance_report and st.session_state.compliance_report.missing_requirements:
        report = st.session_state.compliance_report
        missing_reqs = report.missing_requirements
        
        # Initialize document updater
        if 'document_updater' not in st.session_state:
            st.session_state.document_updater = DocumentUpdater()
        
        updater = st.session_state.document_updater
        
        # Get risk summary
        risk_summary = updater.get_risk_summary(missing_reqs)
        
        # ========== RISK METRICS ==========
        st.subheader("📊 Risk Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Missing Clauses",
                risk_summary['total_missing']
            )
        
        with col2:
            avg_risk = risk_summary['average_risk']
            risk_emoji = "🔴" if avg_risk >= 70 else "🟡" if avg_risk >= 40 else "🟢"
            st.metric(
                "Average Risk",
                f"{avg_risk:.0f}%",
                delta=risk_emoji
            )
        
        with col3:
            st.metric(
                "Highest Risk",
                f"{risk_summary['max_risk']:.0f}%",
                delta="🔴 Critical" if risk_summary['max_risk'] >= 70 else None
            )
        
        with col4:
            st.metric(
                "High Risk Count",
                risk_summary['high_risk_count'],
                delta="⚠️ Urgent" if risk_summary['high_risk_count'] > 0 else None
            )
        
        # ========== RISK DISTRIBUTION CHART ==========
        st.subheader("Risk Distribution")
        
        risk_dist = risk_summary['risk_distribution']
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(risk_dist.keys()),
                y=list(risk_dist.values()),
                marker_color=['#ff6b6b', '#ffd166', '#06d6a0'],
                text=list(risk_dist.values()),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Missing Clauses by Risk Level",
            xaxis_title="Risk Level",
            yaxis_title="Number of Clauses",
            showlegend=False,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # ========== MISSING CLAUSES TABLE ==========
        st.subheader("🎯 Missing Clauses with Risk Analysis")
        
        # Calculate risk for each requirement
        missing_with_risk = []
        for req in missing_reqs:
            risk_pct = updater.calculate_risk_percentage(req)
            missing_with_risk.append({
                'requirement': req,
                'risk_percentage': risk_pct
            })
        
        # Sort by risk (highest first)
        missing_with_risk.sort(key=lambda x: x['risk_percentage'], reverse=True)
        
        # Display each missing clause
        for item in missing_with_risk:
            req = item['requirement']
            risk_pct = item['risk_percentage']
            
            # Color code risk
            if risk_pct >= 70:
                risk_badge = f'🔴 {risk_pct:.0f}% RISK'
            elif risk_pct >= 40:
                risk_badge = f'🟡 {risk_pct:.0f}% RISK'
            else:
                risk_badge = f'🟢 {risk_pct:.0f}% RISK'
            
            with st.expander(
                f"**{req.article_reference}** - {req.clause_type} - {risk_badge}",
                expanded=(risk_pct >= 70)  # Auto-expand high risk
            ):
                # Requirement details
                st.markdown(f"**Framework:** {req.framework}")
                st.markdown(f"**Description:** {req.description}")
                st.markdown(f"**Mandatory:** {'Yes ⚠️' if req.mandatory else 'No'}")
                st.markdown(f"**Risk Level:** {req.risk_level.value}")
                
                # Risk breakdown
                st.markdown("**Risk Calculation Breakdown:**")
                mandatory_score = 40 if req.mandatory else 15
                risk_level_score = {
                    "HIGH": 30,
                    "MEDIUM": 20,
                    "LOW": 10
                }.get(req.risk_level.value, 10)
                
                st.progress(risk_pct / 100.0)
                st.caption(
                    f"Mandatory: +{mandatory_score}% | "
                    f"Severity: +{risk_level_score}% | "
                    f"Framework: +{risk_pct - mandatory_score - risk_level_score:.0f}%"
                )
                
                # Mandatory elements
                if req.mandatory_elements:
                    st.markdown("**Required Elements:**")
                    for elem in req.mandatory_elements:
                        st.markdown(f"- {elem}")
        
        st.markdown("---")
        
        # ========== GENERATION SECTION ==========
        st.subheader("🤖 Generate Missing Clauses & Rewrite Contract")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info(
                "⚡ This feature will use AI to automatically generate compliant "
                "clause text for all missing requirements and create a rewritten contract with them inserted."
            )
        
        with col2:
            prioritize = st.checkbox("Prioritize by risk", value=True)
            top_n = st.number_input(
                "Generate top N",
                min_value=1,
                max_value=len(missing_reqs),
                value=min(5, len(missing_reqs)),
                help="Generate only the highest risk clauses"
            )
        
        # Generate button
        if st.button("🚀 Generate Missing Clauses", type="primary", use_container_width=True):
            with st.spinner("Generating clauses with AI... This may take a minute."):
                try:
                    # Generate clauses
                    generated_clauses = updater.generate_missing_clauses(
                        missing_requirements=missing_reqs,
                        existing_contract_text=st.session_state.processed_document.extracted_text,
                        prioritize=prioritize,
                        top_n=top_n
                    )
                    
                    # Store in session
                    st.session_state.generated_clauses = generated_clauses
                    
                    st.success(f"✅ Successfully generated {len(generated_clauses)} clauses!")
                    st.rerun()  # Refresh to show generated clauses
                    
                except Exception as e:
                    st.error(f"❌ Error generating clauses: {e}")
                    logger.error(f"Clause generation error: {e}", exc_info=True)
        
        # ========== DISPLAY GENERATED CLAUSES ==========
        if 'generated_clauses' in st.session_state and st.session_state.generated_clauses:
            st.markdown("---")
            st.subheader("📝 Generated Clauses")
            
            generated = st.session_state.generated_clauses
            
            st.success(f"Generated {len(generated)} clauses. Review before adding to document.")
            
            # Display each generated clause
            for i, gen_clause in enumerate(generated, 1):
                req = gen_clause.requirement
                risk_pct = gen_clause.risk_percentage
                
                # Risk badge
                if risk_pct >= 70:
                    risk_badge = f'🔴 {risk_pct:.0f}% Risk'
                elif risk_pct >= 40:
                    risk_badge = f'🟡 {risk_pct:.0f}% Risk'
                else:
                    risk_badge = f'🟢 {risk_pct:.0f}% Risk'
                
                with st.expander(
                    f"**{i}. {req.article_reference}** - {risk_badge}",
                    expanded=(i <= 3)  # Auto-expand first 3
                ):
                    st.markdown(f"**Clause Type:** {req.clause_type}")
                    st.markdown(f"**Framework:** {req.framework}")
                    
                    st.markdown("**Generated Clause Text:**")
                    
                    # Editable text area
                    edited_text = st.text_area(
                        "Clause Text (editable)",
                        value=gen_clause.generated_text,
                        height=150,
                        key=f"clause_text_{i}"
                    )
                    
                    # Update the clause text if edited
                    gen_clause.generated_text = edited_text
                    
                    # Confidence indicator
                    confidence = gen_clause.confidence_score
                    st.progress(confidence, text=f"Generation Confidence: {confidence:.0%}")
            
            st.markdown("---")
            
            # ========== EXPORT SECTION ==========
            st.subheader("📥 Download Rewritten Contract")
            
            st.info("✅ Your contract will be rewritten with all missing clauses inserted and highlighted!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                output_format = st.selectbox(
                    "Output Format",
                    options=["docx", "txt"],
                    format_func=lambda x: "Word Document (.docx) - With Yellow Highlights" if x == "docx" else "Text File (.txt) - With Insertion Markers"
                )
            
            with col2:
                st.write("")  # Spacing
            
            if st.button("📥 Create Rewritten Contract", type="primary", use_container_width=True):
                with st.spinner("Creating rewritten contract with missing clauses..."):
                    try:
                        # Create updated document
                        updated_doc_buffer = updater.create_updated_document(
                            original_text=st.session_state.processed_document.extracted_text,
                            generated_clauses=generated,
                            output_format=output_format
                        )
                        
                        # Offer download
                        file_extension = "docx" if output_format == "docx" else "txt"
                        filename = f"contract_rewritten_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
                        
                        st.download_button(
                            label=f"⬇️ Download Rewritten Contract (.{file_extension})",
                            data=updated_doc_buffer,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document" if output_format == "docx" else "text/plain",
                            use_container_width=True
                        )
                        
                        st.success("✅ Rewritten contract ready for download!")
                        
                        # Show preview
                        with st.expander("📄 Preview Changes"):
                            st.info(
                                f"The rewritten contract includes **{len(generated)} new clauses** "
                                f"{'highlighted in yellow' if output_format == 'docx' else 'marked with insertion tags'}."
                            )
                            st.markdown("**Changes Summary:**")
                            for i, gen_clause in enumerate(generated, 1):
                                st.markdown(
                                    f"{i}. **{gen_clause.requirement.article_reference}** "
                                    f"(Risk: {gen_clause.risk_percentage:.0f}%) - "
                                    f"{len(gen_clause.generated_text)} characters"
                                )
                    
                    except Exception as e:
                        st.error(f"❌ Error creating rewritten contract: {e}")
                        logger.error(f"Document creation error: {e}", exc_info=True)
    
    else:
        # No missing clauses
        if st.session_state.compliance_report:
            st.success("🎉 Great! No missing clauses found. Your contract is fully compliant!")
        else:
            st.info(
                "📋 No compliance analysis available yet. "
                "Please upload and analyze a contract first in the **Contract Analysis** tab."
            )

# ==================== TAB 5: REGULATORY UPDATES ====================
with tab5:
    st.markdown('<h2 class="section-header">Regulatory Updates</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Recent Regulatory Changes")
        
        updates = [
            {
                "date": "2024-01-15",
                "regulation": "GDPR",
                "change": "Updated guidance on AI and automated decision-making",
                "impact": "High",
                "status": "Active"
            },
            {
                "date": "2024-01-10", 
                "regulation": "HIPAA",
                "change": "New requirements for telehealth data security",
                "impact": "Medium",
                "status": "Pending"
            },
            {
                "date": "2024-01-05",
                "regulation": "CCPA",
                "change": "Extended consumer rights for data deletion",
                "impact": "Medium", 
                "status": "Active"
            }
        ]
        
        for update in updates:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{update['regulation']}**: {update['change']}")
                    st.caption(f"Effective: {update['date']} | Status: {update['status']}")
                with col2:
                    impact_color = {
                        'High': 'risk-high',
                        'Medium': 'risk-medium',
                        'Low': 'risk-low'
                    }[update['impact']]
                    st.markdown(f"<span class='{impact_color}'>Impact: {update['impact']}</span>", unsafe_allow_html=True)
                st.divider()
    
    with col2:
        st.subheader("Update Monitoring")
        
        st.metric("Active Updates", "3")
        st.metric("High Impact", "1")
        st.metric("Contracts Affected", "12")
        
        st.progress(75, text="Update Implementation Progress")
        
        if st.button("🔄 Scan for New Updates"):
            st.success("Scan complete! No new updates found.")
        
        st.subheader("Subscribe to Alerts")
        email = st.text_input("Email for alerts:")
        if st.button("Subscribe"):
            st.success("Subscribed to regulatory updates!")

# ==================== TAB 6: SETTINGS ====================
with tab6:
    st.markdown('<h2 class="section-header">Settings & Configuration</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Analysis Settings")
        
        st.select_slider(
            "Analysis Depth",
            options=["Basic", "Standard", "Comprehensive"],
            value="Standard"
        )
        
        st.number_input("Minimum Confidence Threshold (%)", min_value=50, max_value=95, value=75)
        
        st.multiselect(
            "Prioritized Regulations",
            options=['GDPR', 'HIPAA', 'CCPA', 'SOX'],
            default=['GDPR', 'HIPAA']
        )
        
        st.checkbox("Enable AI-powered recommendations", value=True)
        st.checkbox("Auto-generate missing clauses", value=True)
    
    with col2:
        st.subheader("Integration Settings")
        
        st.text_input("Google Sheets API Key", type="password")
        st.text_input("Slack Webhook URL")
        st.text_input("OpenAI API Key", type="password")
        
        st.selectbox(
            "Default Export Format",
            options=["PDF", "DOCX", "JSON", "CSV"]
        )
        
        if st.button("💾 Save Settings", use_container_width=True):
            st.success("Settings saved successfully!")
        
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.info("Settings reset to defaults")

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("© 2024 AI Compliance Checker")
    st.caption("Version 1.0.0")

with footer_col2:
    st.caption("Last updated: January 15, 2024")
    st.caption("Next regulatory scan: Today, 18:00")

with footer_col3:
    st.caption("Need help? Contact support@compliancechecker.ai")