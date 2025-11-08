# Part 2 Integration Guide: Auto-Fix Missing Clauses with Risk Percentage

## Overview
This guide shows you how to integrate the new **Document Updater** feature (Part 2) into your Streamlit app, which automatically generates missing clauses with risk percentage indicators.

---

## Step 1: Add CSS Styles to app.py

Add these styles to your existing CSS section in `app.py`:

```python
# Find the section with your CSS (around line 50-100) and ADD these new classes:

st.markdown("""
    <style>
    /* Your existing CSS styles... */
    
    /* NEW: Risk badge styles for Part 2 */
    .risk-high {
        background-color: #ff6b6b;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85em;
        display: inline-block;
        margin-left: 8px;
    }
    
    .risk-medium {
        background-color: #ffd166;
        color: #333;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85em;
        display: inline-block;
        margin-left: 8px;
    }
    
    .risk-low {
        background-color: #06d6a0;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85em;
        display: inline-block;
        margin-left: 8px;
    }
    </style>
""", unsafe_allow_html=True)
```

---

## Step 2: Add Import Statement

At the top of `app.py` (around line 10-30), add this import:

```python
from services.document_updater import DocumentUpdater, MissingClauseGeneration
```

---

## Step 3: Modify Tab Creation

**FIND** this line in `app.py` (around line 200-250):

```python
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Contract Analysis", 
    "📊 Dashboard", 
    "🔍 Clause Details", 
    "🔄 Regulatory Updates", 
    "⚙️ Settings"
])
```

**REPLACE** with (adding the new "Auto-Fix" tab):

```python
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Contract Analysis", 
    "📊 Dashboard", 
    "🔍 Clause Details", 
    "✨ Auto-Fix Missing Clauses",  # NEW TAB
    "🔄 Regulatory Updates", 
    "⚙️ Settings"
])
```

---

## Step 4: Add the New Tab Content

**FIND** where your tabs end (look for `with tab3:` section, around line 800-900), and **INSERT** this NEW section right after the `tab3` block:

```python
# ==================== TAB 4: AUTO-FIX MISSING CLAUSES ====================
with tab4:
    st.markdown('<h2 class="section-header">✨ Auto-Generate Missing Clauses</h2>', unsafe_allow_html=True)
    
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
        
        import plotly.graph_objects as go
        
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
                risk_badge = f'<span class="risk-high">🔴 {risk_pct:.0f}% RISK</span>'
            elif risk_pct >= 40:
                risk_badge = f'<span class="risk-medium">🟡 {risk_pct:.0f}% RISK</span>'
            else:
                risk_badge = f'<span class="risk-low">🟢 {risk_pct:.0f}% RISK</span>'
            
            with st.expander(
                f"**{req.article_reference}** - {req.clause_type}",
                expanded=(risk_pct >= 70)  # Auto-expand high risk
            ):
                # Show risk badge in expander
                st.markdown(risk_badge, unsafe_allow_html=True)
                
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
        st.subheader("🤖 Generate Missing Clauses")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info(
                "⚡ This feature will use AI to automatically generate compliant "
                "clause text for all missing requirements and insert them into your document."
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
                        existing_contract_text=st.session_state.processed_document.full_text,
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
            st.subheader("📥 Export Updated Document")
            
            col1, col2 = st.columns(2)
            
            with col1:
                output_format = st.selectbox(
                    "Output Format",
                    options=["docx", "txt"],
                    format_func=lambda x: "Word Document (.docx) - Highlighted" if x == "docx" else "Text File (.txt) - With Markers"
                )
            
            with col2:
                st.write("")  # Spacing
            
            if st.button("📥 Create Updated Document", type="primary", use_container_width=True):
                with st.spinner("Creating updated document..."):
                    try:
                        # Import datetime at top if not already
                        from datetime import datetime
                        
                        # Create updated document
                        updated_doc_buffer = updater.create_updated_document(
                            original_text=st.session_state.processed_document.full_text,
                            generated_clauses=generated,
                            output_format=output_format
                        )
                        
                        # Offer download
                        file_extension = "docx" if output_format == "docx" else "txt"
                        filename = f"contract_updated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
                        
                        st.download_button(
                            label=f"⬇️ Download Updated Contract (.{file_extension})",
                            data=updated_doc_buffer,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document" if output_format == "docx" else "text/plain",
                            use_container_width=True
                        )
                        
                        st.success("✅ Updated document ready for download!")
                        
                        # Show preview
                        with st.expander("📄 Preview Changes"):
                            st.info(
                                f"The updated document includes **{len(generated)} new clauses** "
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
                        st.error(f"❌ Error creating updated document: {e}")
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
```

---

## Step 5: Update Tab References

Since we added a new tab, you need to update the OLD tab numbers:

**BEFORE:**
- Tab 1: Contract Analysis
- Tab 2: Dashboard  
- Tab 3: Clause Details
- Tab 4: Regulatory Updates ← FIND THIS
- Tab 5: Settings ← AND THIS

**AFTER:**
- Tab 1: Contract Analysis
- Tab 2: Dashboard
- Tab 3: Clause Details
- Tab 4: Auto-Fix Missing Clauses ← NEW
- Tab 5: Regulatory Updates ← Now tab5 instead of tab4
- Tab 6: Settings ← Now tab6 instead of tab5

**FIND** lines with `with tab4:` and `with tab5:` (the OLD Regulatory Updates and Settings tabs).

**CHANGE** them to:

```python
# Old: with tab4:
# New:
with tab5:  # Regulatory Updates moved from tab4 to tab5

# ... existing Regulatory Updates code ...

# Old: with tab5:
# New:
with tab6:  # Settings moved from tab5 to tab6

# ... existing Settings code ...
```

---

## Step 6: Test the Integration

1. **Save `app.py`** with all the changes
2. **Restart your Streamlit app:**
   ```powershell
   python -m streamlit run app.py
   ```
3. **Test workflow:**
   - Go to **Contract Analysis** tab
   - Upload a contract
   - Select frameworks (GDPR, HIPAA, etc.)
   - Click "Analyze Contract"
   - Go to new **✨ Auto-Fix Missing Clauses** tab
   - You should see:
     - Risk summary metrics
     - Risk distribution chart
     - Missing clauses sorted by risk percentage
     - Generate button
   - Click **🚀 Generate Missing Clauses**
   - Review generated clauses
   - Click **📥 Create Updated Document**
   - Download the updated contract

---

## Features Included

✅ **Risk Percentage Calculation** - Each missing clause shows 0-100% risk score  
✅ **Risk Distribution Chart** - Visual breakdown of high/medium/low risk clauses  
✅ **Risk Breakdown** - Shows how risk score is calculated (Mandatory + Severity + Framework)  
✅ **Prioritized Generation** - Option to generate only highest risk clauses first  
✅ **AI Clause Generation** - Uses LLaMA to create compliant clause text  
✅ **Editable Clauses** - Review and edit generated text before inserting  
✅ **DOCX Export** - Creates Word document with yellow highlighted new clauses  
✅ **Text Export** - Creates text file with `[INSERTED]` markers  
✅ **Confidence Scores** - Shows AI confidence for each generated clause  

---

## Troubleshooting

**Issue: "DocumentUpdater not found"**
- Make sure `services/document_updater.py` exists
- Check the import statement is correct

**Issue: "Tab4 already exists error"**
- You may have duplicate tabs. Check your tab definitions carefully
- Make sure you updated the old tab4/tab5 to tab5/tab6

**Issue: "No missing clauses shown"**
- Run analysis in Contract Analysis tab first
- Make sure compliance report has missing requirements

**Issue: "Generate button does nothing"**
- Check console/terminal for errors
- LLaMA model may take time to load (1-2 minutes first time)

---

## What's Next?

After integrating Part 2, you can enhance further with:

1. **Side-by-side comparison** - Show original vs updated document
2. **Clause approval workflow** - Let users accept/reject individual clauses
3. **Version history** - Track different versions of updated contracts
4. **Batch processing** - Update multiple contracts at once
5. **Custom risk formulas** - Let admins configure risk calculation weights

---

## Summary

You now have a complete **Auto-Fix Missing Clauses** feature that:
- Calculates risk percentages for each missing clause
- Visualizes risk distribution  
- Generates compliant clause text using AI
- Exports updated documents with highlighting
- Provides full transparency into the risk calculation

This completes **Part 2** of your project! 🎉
