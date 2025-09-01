def format_kb_results(results):
    items = "\n\n".join(
        f"**Q:** {r['question']}\n**A:** {r['answer']}\n(Confidence: {r['confidence']:.2f})"
        for r in results
    )
    return (
        "Retrieved knowledge base results below. "
        "⚠️ Use only entries clearly relevant to the user’s query. "
        "If none fit, ignore them.\n\n"
        f"{items}"
    )

def format_issue_guide_results(results):
    items = "\n\n".join(
        f"**Issue:** {r['issue']}\n"
        f"**Troubleshooting Steps:** {r['troubleshooting_steps']}\n"
        f"**Quick Fixes:** {r['quick_fixes']}\n"
        f"**Escalation Criteria:** {r['escalation_criteria']}\n"
        f"(Confidence: {r['confidence']:.2f})"
        for r in results
    )
    return (
        "Guide entries retrieved below. "
        "⚠️ Use only if they clearly address the user’s issue. "
        "If none fit, ignore them.\n\n"
        f"{items}"
    )
