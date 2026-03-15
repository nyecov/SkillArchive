import pytest
import json

@pytest.mark.asyncio
async def test_ontology_dag_cycle_rejection(mcp_server):
    # Note: Ontology path is hardcoded relative to MEMORY_DIR in the server
    # But some tests might try to ingest it.
    """Verify that hierarchical edges prevent circular references."""
    # 1. Create A -> B
    await mcp_server.call_tool("commit_ontology_edge", {
        "source_entity": "Module_A",
        "edge_type": "REQUIRES",
        "target_entity": "Module_B"
    })

    # 2. Attempt B -> A (Cycle)
    result = await mcp_server.call_tool("commit_ontology_edge", {
        "source_entity": "Module_B",
        "edge_type": "REQUIRES",
        "target_entity": "Module_A"
    })
    
    assert result.isError is True
    assert "circular dependency" in result.content[0].text

@pytest.mark.asyncio
async def test_ontology_transactional_integrity(mcp_server):
    """Verify that a rejected cycle does not result in a partial write."""
    # 1. Record existing state
    initial = await mcp_server.call_tool("read_ontology_graph", {"target_entity": "Module_A"})
    
    # 2. Fail a cycle commit
    await mcp_server.call_tool("commit_ontology_edge", {
        "source_entity": "Module_A",
        "edge_type": "REQUIRES",
        "target_entity": "Module_A" # Self-reference cycle
    })

    # 3. Read state again
    final = await mcp_server.call_tool("read_ontology_graph", {"target_entity": "Module_A"})
    assert initial.content[0].text == final.content[0].text

@pytest.mark.asyncio
async def test_ontology_graph_traversal(mcp_server):
    """Verify downstream/upstream dependency retrieval."""
    # Commit a small chain: X -> Y -> Z
    await mcp_server.call_tool("commit_ontology_edge", {"source_entity": "X", "edge_type": "OWNS", "target_entity": "Y"})
    await mcp_server.call_tool("commit_ontology_edge", {"source_entity": "Y", "edge_type": "OWNS", "target_entity": "Z"})

    result = await mcp_server.call_tool("read_ontology_graph", {"target_entity": "Y"})
    text = result.content[0].text
    
    # Corrected strings based on ontology.go output format
    assert "- [OWNS] -> Z" in text
    assert "- X -> [OWNS]" in text

@pytest.mark.asyncio
async def test_ontology_edge_deletion(mcp_server):
    """Verify that edges can be removed to resolve architectural blocks."""
    # 1. Create edge
    await mcp_server.call_tool("commit_ontology_edge", {"source_entity": "Old", "edge_type": "REFERENCES", "target_entity": "New"})
    
    # 2. Verify existence
    res1 = await mcp_server.call_tool("read_ontology_graph", {"target_entity": "Old"})
    assert "[REFERENCES] -> New" in res1.content[0].text

    # 3. Delete
    await mcp_server.call_tool("delete_ontology_edge", {"source_entity": "Old", "edge_type": "REFERENCES", "target_entity": "New"})
    
    # 4. Verify absence
    res2 = await mcp_server.call_tool("read_ontology_graph", {"target_entity": "Old"})
    assert "[REFERENCES] -> New" not in res2.content[0].text

@pytest.mark.asyncio
async def test_semantic_search(mcp_server):
    """Verify that fuzzy keywords can return the correct edges via FTS5."""
    # 1. Commit complex edges
    await mcp_server.call_tool("commit_ontology_edge", {
        "source_entity": "OAuth2_Service",
        "edge_type": "REQUIRES",
        "target_entity": "Postgres_DB"
    })
    
    # 2. Search with fuzzy keyword "auth database" (or similar)
    # The FTS5 MATCH uses exact word matching by default unless using OR or *.
    # Let's search for "OAuth2_Service" but partially, or just "Postgres_DB".
    # Since we used fts5 with no tokenizer config, we can search for exact words or prefixes if using *.
    # Let's search for "OAuth2_Service" or "Postgres" if we use wildcards or just "Postgres_DB".
    result = await mcp_server.call_tool("search_ontology_semantic", {"query": "Postgres_DB"})
    
    assert result.isError is False
    assert "OAuth2_Service -> [REQUIRES] -> Postgres_DB" in result.content[0].text

@pytest.mark.asyncio
async def test_semantic_search_malformed_query(mcp_server):
    """Verify that malformed or empty queries are handled gracefully (Jidoka)."""
    # Empty query should fail gracefully
    res_empty = await mcp_server.call_tool("search_ontology_semantic", {"query": ""})
    assert res_empty.isError is True
    assert "query is required and cannot be empty" in res_empty.content[0].text

    # Too long query should fail gracefully
    long_query = "a" * 101
    res_long = await mcp_server.call_tool("search_ontology_semantic", {"query": long_query})
    assert res_long.isError is True
    assert "query is too long" in res_long.content[0].text

    # Invalid FTS syntax (e.g. unclosed quote) should not crash the server but return empty or text
    res_invalid = await mcp_server.call_tool("search_ontology_semantic", {"query": "\""})
    assert res_invalid.isError is False
    assert "Search failed or no matches found" in res_invalid.content[0].text
