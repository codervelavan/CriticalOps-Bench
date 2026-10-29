import pandas as pd
import streamlit as st
from core.evaluation import run_evaluation
from core.scoring import demo_use_cases, score_use_case
from core.store import init_db, list_incidents, metrics_summary, review_incident, save_incident
from core.triage import triage_incident

st.set_page_config(page_title="CriticalOps AI Workbench", page_icon="🛠️", layout="wide")
init_db()

st.title("CriticalOps AI Workbench")
st.caption("Portfolio prototype • governed AI decision support for industrial maintenance • all records are synthetic")
st.warning("Safety notice: this is a demonstration only. It does not control equipment or provide operational instructions. Always follow approved site procedures and qualified human judgment.")

tab_assess, tab_triage, tab_review, tab_evaluate, tab_metrics = st.tabs([
    "Use-case assessment", "Incident triage", "Human review", "Evaluation", "Operations metrics"
])

with tab_assess:
    st.subheader("Prioritise an AI opportunity")
    st.write("Score one proposed use case on value, feasibility, data readiness, governance readiness, scalability and effort.")
    with st.form("score_form"):
        name = st.text_input("Use-case name", "Maintenance incident triage and SOP retrieval")
        problem = st.text_area("Business problem", "Maintenance analysts spend time classifying incidents and searching approved work instructions.")
        col1, col2, col3 = st.columns(3)
        with col1:
            business_value = st.slider("Business value", 1, 5, 5)
            feasibility = st.slider("Technical feasibility", 1, 5, 4)
        with col2:
            data_readiness = st.slider("Data readiness", 1, 5, 4)
            governance = st.slider("Governance readiness", 1, 5, 4)
        with col3:
            scalability = st.slider("Scalability", 1, 5, 4)
            effort = st.slider("Implementation effort (5 = high)", 1, 5, 3)
        submit = st.form_submit_button("Assess use case", type="primary")
    if submit:
        result = score_use_case({
            "name": name, "business_problem": problem, "business_value": business_value,
            "technical_feasibility": feasibility, "data_readiness": data_readiness,
            "governance_readiness": governance, "scalability": scalability,
            "implementation_effort": effort,
        })
        st.metric("Readiness-weighted score", f"{result['score']}/100")
        st.write(f"**Recommendation:** {result['recommendation']}")
        st.write("**Risks / next steps**")
        for risk in result["risks_and_next_steps"]:
            st.write(f"- {risk}")
        st.json(result["score_breakdown"])
        st.caption(result["disclaimer"])
    with st.expander("Example use cases"):
        for item in demo_use_cases():
            st.write(f"**{item['name']}** — {item['assessment']['score']}/100: {item['assessment']['recommendation']}")

with tab_triage:
    st.subheader("Incident triage and knowledge retrieval")
    st.write("Submit a synthetic incident to receive a suggested category, priority, queue and local knowledge references.")
    with st.form("triage_form"):
        incident_id = st.text_input("Incident ID (optional)", "")
        asset_id = st.text_input("Asset ID", "PUMP-204")
        site = st.text_input("Site", "Demo Manufacturing Site")
        description = st.text_area("Incident description", "Pump PUMP-204 has rising vibration and unusual bearing noise; production impact is moderate.")
        c1, c2, c3 = st.columns(3)
        with c1:
            impact = st.slider("Production impact", 1, 5, 3)
        with c2:
            downtime = st.number_input("Estimated downtime (hours)", min_value=0.0, max_value=10000.0, value=1.0, step=0.5)
        with c3:
            safety_related = st.checkbox("Potential safety issue reported", value=False)
        triage_submit = st.form_submit_button("Triage incident", type="primary")
    if triage_submit:
        ticket = {
            "incident_id": incident_id.strip() or None, "asset_id": asset_id, "site": site,
            "description": description, "production_impact": impact,
            "estimated_downtime_hours": downtime, "safety_related": safety_related,
        }
        result = triage_incident(ticket)
        save_incident(ticket, result)
        st.session_state["last_incident"] = result["incident_id"]
        st.success(f"Saved incident {result['incident_id']} for human review.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Suggested category", result["category"].replace("_", " "))
        c2.metric("Suggested priority", result["suggested_priority"])
        c3.metric("Evidence score (lexical baseline)", result["retrieval_confidence"])
        st.write("**Suggested queue:**", result["suggested_queue"])
        st.write("**Suggested next step:**", result["suggested_next_step"])
        st.write("**Draft response:**")
        st.info(result["draft_response"])
        st.write("**Retrieved knowledge references:**")
        if result["retrieved_sources"]:
            st.dataframe(pd.DataFrame(result["retrieved_sources"]), use_container_width=True, hide_index=True)
        else:
            st.write("No knowledge references retrieved; use the fallback/escalation path.")
        st.caption(f"Mode: {result['model_mode']} / {result['retrieval_mode']}. Human review required.")

with tab_review:
    st.subheader("Human review queue")
    incidents = list_incidents(500)
    pending = [item for item in incidents if item.get("review_status") == "pending"]
    if not pending:
        st.info("No incidents awaiting review yet. Submit one in the Incident triage tab.")
    else:
        labels = {f"{x['incident_id']} — {x.get('category', '')} — {x.get('suggested_priority', '')}": x for x in pending}
        selected_label = st.selectbox("Select incident", list(labels.keys()))
        selected = labels[selected_label]
        st.write("**Ticket:**", selected.get("ticket", {}).get("description", ""))
        st.write("**Proposed response:**", selected.get("draft_response", ""))
        with st.form("review_form"):
            decision = st.selectbox("Decision", ["approved", "rejected", "needs_more_information"])
            reviewer = st.text_input("Reviewer", "Maintenance Analyst")
            comment = st.text_area("Review note", "Reviewed demo evidence and confirmed the next step.")
            review_submit = st.form_submit_button("Record review", type="primary")
        if review_submit:
            review_incident(selected["incident_id"], decision, reviewer, comment)
            st.success("Review decision recorded in the local audit log.")
            st.rerun()
    with st.expander("Recent incident history"):
        if incidents:
            st.dataframe(pd.DataFrame([{k: x.get(k) for k in ["incident_id", "category", "suggested_priority", "review_status", "reviewer", "reviewed_at"]} for x in incidents]), use_container_width=True, hide_index=True)

with tab_evaluate:
    st.subheader("Offline baseline evaluation")
    st.write("Runs the current deterministic triage baseline against labelled synthetic cases. Treat results as prototype measurements only.")
    if st.button("Run evaluation suite", type="primary"):
        report = run_evaluation()
        st.session_state["eval_report"] = report
    report = st.session_state.get("eval_report")
    if report:
        c1, c2, c3 = st.columns(3)
        c1.metric("Category exact match", f"{report['category_exact_match_pct']}%")
        c2.metric("Priority exact match", f"{report['priority_exact_match_pct']}%")
        c3.metric("Safety escalation checks", f"{report['safety_escalation_pass_pct']}%")
        st.dataframe(pd.DataFrame(report["results"]), use_container_width=True, hide_index=True)
        st.caption(report["interpretation"])

with tab_metrics:
    st.subheader("Operational overview")
    summary = metrics_summary()
    c1, c2, c3 = st.columns(3)
    c1.metric("Incidents triaged", summary["total_incidents"])
    c2.metric("Pending human reviews", summary["pending_reviews"])
    c3.metric("Critical reviews", summary["critical_reviews"])
    c4, c5 = st.columns(2)
    c4.metric("Retrieval fallback rate", f"{summary['fallback_rate_pct']}%")
    c5.write("**Review decisions**")
    c5.json(summary["review_counts"])
    if summary["category_counts"]:
        st.write("**Incident categories**")
        st.bar_chart(pd.DataFrame.from_dict(summary["category_counts"], orient="index", columns=["count"]))
    incidents = list_incidents(1000)
    if incidents:
        df = pd.DataFrame([{
            "incident_id": x["incident_id"], "created_at": x.get("created_at"),
            "category": x.get("category"), "suggested_priority": x.get("suggested_priority"),
            "review_status": x.get("review_status"), "fallback_used": x.get("fallback_used"),
            "retrieval_confidence": x.get("retrieval_confidence"),
        } for x in incidents])
        st.download_button("Download incident metrics CSV", df.to_csv(index=False).encode("utf-8"), "criticalops_incidents.csv", "text/csv")
