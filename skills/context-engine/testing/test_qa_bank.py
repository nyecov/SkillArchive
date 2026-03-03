import os
import pytest
import asyncio

@pytest.mark.asyncio
async def test_append_interview_qa(test_workspace, mcp_server):
    """Verify that appending a QA pair writes a formatted TOON block with a timestamp."""
    toon_pair = "[Q: What is the core problem?]\n[A: Context bloat.]"
    
    res = await mcp_server.call_tool("append_interview_qa", {
        "toon_qa_pair": toon_pair
    })
    
    assert not res.isError
    assert "Successfully appended" in res.content[0].text

    bank_path = os.path.join(test_workspace, "interview_qa_bank.toon")
    assert os.path.exists(bank_path)
    
    with open(bank_path, "r") as f:
        content = f.read()
        
    assert "[META: Timestamp:" in content
    assert "[Q: What is the core problem?]" in content
    assert "[A: Context bloat.]" in content

@pytest.mark.asyncio
async def test_retrieve_interview_patterns_empty(test_workspace, mcp_server):
    """Verify that reading an empty or non-existent bank returns a graceful message."""
    bank_path = os.path.join(test_workspace, "interview_qa_bank.toon")
    if os.path.exists(bank_path):
        os.remove(bank_path)

    res = await mcp_server.call_tool("retrieve_interview_patterns", {})
    assert not res.isError
    assert "currently empty" in res.content[0].text

@pytest.mark.asyncio
async def test_retrieve_interview_patterns_query(test_workspace, mcp_server):
    """Verify that querying filters out unrelated blocks and only returns semantic matches."""
    # Seed data
    await mcp_server.call_tool("append_interview_qa", {
        "toon_qa_pair": "[Q: How do we fix latency?]\n[A: Use the daemon mode.]"
    })
    await asyncio.sleep(0.1) # ensure timestamp difference if needed
    await mcp_server.call_tool("append_interview_qa", {
        "toon_qa_pair": "[Q: What is the risk?]\n[A: Directory traversal.]"
    })

    # Query for latency
    res = await mcp_server.call_tool("retrieve_interview_patterns", {
        "query": "latency"
    })
    
    assert not res.isError
    text = res.content[0].text
    
    assert "latency" in text
    assert "daemon mode" in text
    assert "Directory traversal" not in text # Should filter out the unrelated block

@pytest.mark.asyncio
async def test_append_rejects_invalid_toon(test_workspace, mcp_server):
    """Verify the Poka-yoke validation blocks raw unstructured text from corrupting the TOON bank."""
    res = await mcp_server.call_tool("append_interview_qa", {
        "toon_qa_pair": "Just a normal markdown paragraph."
    })
    
    assert res.isError
    assert "Invalid TOON format" in res.content[0].text

@pytest.mark.asyncio
async def test_prune_interview_qa(test_workspace, mcp_server):
    """Verify that pruning by keyword removes only the matching block."""
    # Seed data
    await mcp_server.call_tool("append_interview_qa", {
        "toon_qa_pair": "[Q: Keep this?]\n[A: Yes.]"
    })
    await mcp_server.call_tool("append_interview_qa", {
        "toon_qa_pair": "[Q: Delete this?]\n[A: Trash it.]"
    })

    # Prune
    res = await mcp_server.call_tool("prune_interview_qa", {
        "query": "Trash it"
    })
    
    assert not res.isError
    assert "Removed 1 entries" in res.content[0].text
    
    # Verify remaining
    res_read = await mcp_server.call_tool("retrieve_interview_patterns", {})
    text = res_read.content[0].text
    assert "Keep this" in text
    assert "Trash it" not in text
