"""
PART 2 UI Integration - Document Update with Missing Clauses
Add this to your app.py file
"""

# Add this import at the top of app.py
from services.document_updater import DocumentUpdater, MissingClauseGeneration

# Add this after your existing tab initialization
# This creates a new tab for document enhancement

with st.tabs(["📄 Contract Analysis", "📊 Dashboard", "🔍 Clause Details", 
              "✨ Auto-Fix Missing Clauses", "🔄 Regulatory Updates", "⚙️ Settings"]):
    
    # ... existing tabs ...
    
    # NEW TAB 4: Auto-Fix Missing Clauses
    with tab4:
        st.markdown('<h2 class="section-header">✨ Auto-Generate Missing Clauses</h2>', unsafe_allow_html=True)
        
        if st.session_state.compliance_report and st.session_state.compliance_report.missing_requirements:
            report = st.session_state.compliance_report
            missing_reqs = report.missing_requirements
            
            # Risk Summary Section
            st.subheader("📊 Risk Summary")
            
            # Initialize document updater
            if 'document_updater' not in st.session_state:
                st.session_state.document_updater = DocumentUpdater()
            
            updater = st.session_state.document_updater
            
            # Get risk summary
            risk_summary = updater.get_risk_summary(missing_reqs)
            
            # Display risk metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Missing Clauses",
                    risk_summary['total_missing'],
                    delta=None
                )
            
            with col2:
                avg_risk = risk_summary['average_risk']
                risk_color = "🔴" if avg_risk >= 70 else "🟡" if avg_risk >= 40 else "🟢"
                st.metric(
                    "Average Risk",
                    f"{avg_risk:.0f}%",
                    delta=risk_color
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
                    delta="Urgent" if risk_summary['high_risk_count'] > 0 else None
                )
            
            # Risk Distribution Chart
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
            
            # Missing Clauses Table with Risk Percentages
            st.subheader("🎯 Missing Clauses with Risk Analysis")
            
            # Calculate risk for each missing requirement
            missing_with_risk = []
            for req in missing_reqs:
                risk_pct = updater.calculate_risk_percentage(req)
                missing_with_risk.append({
                    'requirement': req,
                    'risk_percentage': risk_pct
                })
            
            # Sort by risk (highest first)
            missing_with_risk.sort(key=lambda x: x['risk_percentage'], reverse=True)
            
            # Display each missing clause with details
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
                    f"**{req.article_reference}** - {req.clause_type} {risk_badge}",
                    expanded=(risk_pct >= 70)  # Auto-expand high risk items
                ):
                    # Requirement details
                    st.markdown(f"**Framework:** {req.framework}")
                    st.markdown(f"**Description:** {req.description}")
                    st.markdown(f"**Mandatory:** {'Yes ⚠️' if req.mandatory else 'No'}")
                    st.markdown(f"**Risk Level:** {req.risk_level.value}")
                    
                    # Risk breakdown
                    st.markdown("**Risk Calculation:**")
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
                    
                    # Keywords
                    if req.keywords:
                        with st.expander("Keywords (for reference)"):
                            st.write(", ".join(req.keywords[:10]))
            
            st.markdown("---")
            
            # Generation Section
            st.subheader("🤖 Generate Missing Clauses")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.info(
                    "⚡ This feature will use AI to automatically generate compliant "
                    "clause text for all missing requirements and insert them into your document."
                )
            
            with col2:
                # Generation options
                prioritize = st.checkbox("Prioritize by risk", value=True)
                top_n = st.number_input(
                    "Generate top N clauses",
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
                        
                    except Exception as e:
                        st.error(f"❌ Error generating clauses: {e}")
                        logger.error(f"Clause generation error: {e}", exc_info=True)
            
            # Display generated clauses
            if 'generated_clauses' in st.session_state and st.session_state.generated_clauses:
                st.markdown("---")
                st.subheader("📝 Generated Clauses")
                
                generated = st.session_state.generated_clauses
                
                # Summary
                st.success(f"Generated {len(generated)} clauses. Review before adding to document.")
                
                # Display each generated clause
                for i, gen_clause in enumerate(generated, 1):
                    req = gen_clause.requirement
                    
                    # Risk badge
                    risk_pct = gen_clause.risk_percentage
                    if risk_pct >= 70:
                        risk_badge = f'🔴 {risk_pct:.0f}% Risk'
                        risk_class = "risk-high"
                    elif risk_pct >= 40:
                        risk_badge = f'🟡 {risk_pct:.0f}% Risk'
                        risk_class = "risk-medium"
                    else:
                        risk_badge = f'🟢 {risk_pct:.0f}% Risk'
                        risk_class = "risk-low"
                    
                    with st.expander(
                        f"**{i}. {req.article_reference}** - {risk_badge}",
                        expanded=True
                    ):
                        st.markdown(f"**Clause Type:** {req.clause_type}")
                        st.markdown(f"**Framework:** {req.framework}")
                        
                        st.markdown("**Generated Clause Text:**")
                        st.text_area(
                            "Clause Text",
                            value=gen_clause.generated_text,
                            height=150,
                            key=f"clause_text_{i}",
                            help="You can edit this text before inserting"
                        )
                        
                        # Confidence indicator
                        confidence = gen_clause.confidence_score
                        st.progress(confidence, text=f"Generation Confidence: {confidence:.0%}")
                        
                        # Action buttons
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button(f"✅ Approve Clause {i}", key=f"approve_{i}"):
                                st.success(f"Clause {i} approved!")
                        with col_b:
                            if st.button(f"✏️ Edit Clause {i}", key=f"edit_{i}"):
                                st.info("Edit mode activated - modify text above")
                
                st.markdown("---")
                
                # Export Updated Document
                st.subheader("📥 Export Updated Document")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    output_format = st.selectbox(
                        "Output Format",
                        options=["docx", "txt"],
                        format_func=lambda x: "Word Document (.docx)" if x == "docx" else "Text File (.txt)"
                    )
                
                with col2:
                    st.write("")  # Spacing
                
                if st.button("📥 Create Updated Document", type="primary", use_container_width=True):
                    with st.spinner("Creating updated document..."):
                        try:
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
                                    f"The updated document includes {len(generated)} new clauses "
                                    f"highlighted in yellow with risk indicators."
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
            # No missing clauses or no analysis done yet
            if st.session_state.compliance_report:
                st.success("🎉 Great! No missing clauses found. Your contract is complete!")
            else:
                st.info(
                    "📋 No compliance analysis available yet. "
                    "Please upload and analyze a contract first in the 'Contract Analysis' tab."
                )

