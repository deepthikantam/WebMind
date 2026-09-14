import sys
import io

# Force UTF-8 encoding for console output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from agent import WebMindAgent

def test_hackathon_scout_task():
    task_query = (
        "Find relevant AI hackathons, compare their deadline, prize, eligibility and format, "
        "verify the best option from the official page, and prepare a submission-ready shortlist."
    )
    
    agent = WebMindAgent()
    result = agent.run(user_goal=task_query, deep_mode=True)
    
    battlecard = result.get("battlecard", {})
    action_card = result.get("action_card", {})
    verification = result.get("verification", {})
    comparison_rows = battlecard.get("comparison_rows") or battlecard.get("comparison_matrix", [])
    recommendation = battlecard.get("recommendation") or battlecard.get("recommended_choice", "")
    risks = battlecard.get("risks") or battlecard.get("risk_factors", [])
    next_steps = battlecard.get("next_steps") or battlecard.get("actionable_next_steps", [])
    sources = battlecard.get("sources", [])
    trace = result.get("execution_trace", [])
    
    print("\n" + "="*60)
    print("WEBMIND CONTROL — AGENT 7-STAGE PIPELINE TEST RESULT")
    print("="*60)
    print(f"User Task: {result.get('user_goal')}")
    print(f"Top Recommendation: {recommendation}")
    print(f"Verdict: {battlecard.get('verdict')}")
    print(f"Verification Status: {verification.get('status')} (Score: {verification.get('confidence_score')}%)")
    
    print("\n--- ⚡ VERIFIED ACTION EXECUTION CARD (ANAKIN URL SCRAPER) ---")
    print(f"  Target Opportunity: {action_card.get('selected_opportunity')}")
    print(f"  Official Portal: {action_card.get('official_page')}")
    print(f"  Registration Gateway: {action_card.get('registration_url')}")
    print(f"  Verified Deadline: {action_card.get('verified_deadline')}")
    print(f"  Eligibility: {action_card.get('eligibility_status')}")
    print(f"  Immediate Next Action: {action_card.get('next_action')}")
    print("  Required Submission Artifacts:")
    for f in action_card.get("required_fields", []):
        print(f"    - {f}")
    print(f"  Execution Proof: {action_card.get('execution_proof')}")

    print("\n--- 7-STAGE AGENT TRACE ---")
    step_names = [t.get("step_name") for t in trace]
    for t in trace:
        print(f"[{t.get('step_name')}] {t.get('title')} -> {t.get('details')[:80]}...")
    
    print("\n--- COMPARISON ROWS (SHORTLIST MATRIX) ---")
    for i, row in enumerate(comparison_rows):
        print(f"  Row {i+1}: {row.get('dimension')} | Opt A: {row.get('option_a')} | Opt B: {row.get('option_b')}")
        
    print("\n--- CRITICAL RISKS ---")
    for r in risks:
        print(f"  Risk: {r}")
        
    print("\n--- NEXT STEPS ---")
    for s in next_steps:
        print(f"  Step: {s}")
        
    print("\n--- LIVE CITATIONS ---")
    for src in sources:
        print(f"  Citation: {src}")
    print("="*60)
    
    # Assertions
    assert "PLAN" in step_names, "Missing PLAN step in trace"
    assert "TOOL" in step_names, "Missing TOOL step in trace"
    assert "OBSERVE" in step_names, "Missing OBSERVE step in trace"
    assert "REASON" in step_names, "Missing REASON step in trace"
    assert "ACT" in step_names, "Missing ACT step in trace"
    assert "VERIFY" in step_names, "Missing VERIFY step in trace"
    assert "RESULT" in step_names, "Missing RESULT step in trace"
    assert len(comparison_rows) >= 2, f"Expected >= 2 comparison rows, got {len(comparison_rows)}"
    assert recommendation and recommendation != "Analysis Complete", f"Specific recommendation required, got '{recommendation}'"
    assert len(risks) >= 1, "Expected risks"
    assert len(next_steps) >= 1, "Expected next steps"
    assert len(sources) >= 1, "Expected live sources"
    assert verification.get("status") in ["VERIFIED", "PASSED"], "Verification check failed"
    
    # Action Card & Consistency Assertions
    assert "action_card" in result and result["action_card"], "Missing action_card in result"
    assert result["action_card"].get("selected_opportunity"), "Missing selected_opportunity in action_card"
    assert recommendation == result["action_card"].get("selected_opportunity"), f"Recommendation mismatch: '{recommendation}' vs '{result['action_card'].get('selected_opportunity')}'"
    assert result["action_card"].get("registration_url") or result["action_card"].get("registration_note"), "Missing registration_url or registration_note in action_card"
    assert len(result["action_card"].get("required_fields", [])) >= 1, "Missing required_fields in action_card"
    assert "execution_proof" in result["action_card"], "Missing execution_proof in action_card"
    assert result["action_card"]["execution_proof"].get("tool_used") == "Anakin URL Scraper", "Execution proof tool must be Anakin URL Scraper"
    
    print("\n✅ ALL 7-STAGE AGENT PIPELINE & ACTION CARD ASSERTIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_hackathon_scout_task()
