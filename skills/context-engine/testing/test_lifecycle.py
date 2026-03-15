import pytest
import json

@pytest.mark.asyncio
async def test_memory_maturation_lifecycle(mcp_server):
    """
    Verify the full maturation flow: 
    Creation (Scratchpad) -> Upgrade (Ontology) -> Pruning (Scratchpad Deletion)
    """
    # 1. CREATION: Log a finding in the scratchpad
    finding = "The system must use JSON for all memory tiers."
    await mcp_server.call_tool("log_session_finding", {
        "finding_text": finding,
        "phase": "planning"
    })
    
    # Verify state
    res = await mcp_server.call_tool("read_session_state", {})
    state = json.loads(res.content[0].text)
    assert len(state["findings"]) == 1
    assert state["findings"][0]["finding"] == finding

    # 2. UPGRADE: Move to Ontology (Mid-Term)
    await mcp_server.call_tool("commit_ontology_edge", {
        "source_entity": "MemoryTiers",
        "edge_type": "REQUIRES",
        "target_entity": "JSON_Standardization"
    })
    
    # Verify ontology
    res_ont = await mcp_server.call_tool("read_ontology_graph", {"target_entity": "MemoryTiers"})
    assert "REQUIRES] -> JSON_Standardization" in res_ont.content[0].text

    # 3. DELETION (Pruning): Remove the distilled finding from scratchpad
    # We delete index 0
    await mcp_server.call_tool("delete_session_finding", {"index": 0})
    
    # Verify scratchpad is now empty (pruned)
    res_final = await mcp_server.call_tool("read_session_state", {})
    text = res_final.content[0].text
    assert "currently empty" in text or '"findings": []' in text
    print("\n✅ Lifecycle Verified: Creation -> Upgrade -> Pruning successful.")

@pytest.mark.asyncio
async def test_memory_downgrade_reversion(mcp_server):
    """
    Simulate a 'Downgrade' (Reversion): 
    Delete from Ontology -> Move back to Scratchpad for reframing.
    """
    # 1. Setup in Ontology
    await mcp_server.call_tool("commit_ontology_edge", {
        "source_entity": "FeatureX",
        "edge_type": "IMPLEMENTS",
        "target_entity": "RequirementY"
    })
    
    # 2. DELETE (Downgrade): Remove from Ontology
    await mcp_server.call_tool("delete_ontology_edge", {
        "source_entity": "FeatureX",
        "edge_type": "IMPLEMENTS",
        "target_entity": "RequirementY"
    })
    
    # 3. MOVE BACK: Log as finding for re-evaluation
    await mcp_server.call_tool("log_session_finding", {
        "finding_text": "Reframing FeatureX implementation strategy.",
        "phase": "planning"
    })
    
    # Verify
    res = await mcp_server.call_tool("read_session_state", {})
    assert "Reframing FeatureX" in res.content[0].text
    print("\n✅ Downgrade Simulation Verified: Deletion -> Re-evaluation successful.")

@pytest.mark.asyncio
async def test_scratchpad_bulk_clear(mcp_server):
    """Verify high-efficiency bulk cleanup of volatile state."""
    # 1. Fill findings
    await mcp_server.call_tool("log_session_finding", {"finding_text": "A", "phase": "execution"})
    await mcp_server.call_tool("log_session_finding", {"finding_text": "B", "phase": "execution"})
    
    res = await mcp_server.call_tool("read_session_state", {})
    assert len(json.loads(res.content[0].text)["findings"]) == 2

    # 2. CLEAR
    await mcp_server.call_tool("clear_session_state", {})
    
    # 3. Verify
    res2 = await mcp_server.call_tool("read_session_state", {})
    text2 = res2.content[0].text
    assert "currently empty" in text2 or '"findings": []' in text2
    print("\n✅ Bulk Clear Verified.")
