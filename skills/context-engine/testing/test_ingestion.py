import os
import pytest

@pytest.mark.asyncio
async def test_ingest_standard_markdown(mcp_server, test_workspace):
    """Verify ingestion of a standard markdown file."""
    fpath = os.path.join(test_workspace, "test_file.md")
    with open(fpath, "w") as f:
        f.write("# Hello\nThis is a test document.")

    rel_path = "temp__mem/Head/tests/staging/test_file.md"
    result = await mcp_server.call_tool("ingest_context", {"target_path": rel_path})
    
    assert "Hello" in result.content[0].text
    assert "test document" in result.content[0].text

@pytest.mark.asyncio
async def test_ingest_path_traversal_denied(mcp_server):
    """Verify that path traversal attempts are rejected."""
    rel_path = "../../../windows/system32/drivers/etc/hosts"
    result = await mcp_server.call_tool("ingest_context", {"target_path": rel_path})
    
    # Validation
    assert result.isError is True
    assert "outside the workspace root" in result.content[0].text.lower()

@pytest.mark.asyncio
async def test_ingest_16k_character_chunking(mcp_server, test_workspace):
    """Verify that files exceeding the 16k character limit are truncated/chunked."""
    large_content = "X" * 20000
    fpath = os.path.join(test_workspace, "large_file.txt")
    with open(fpath, "w") as f:
        f.write(large_content)

    rel_path = "temp__mem/Head/tests/staging/large_file.txt"
    result = await mcp_server.call_tool("ingest_context", {"target_path": rel_path})
    
    # Heuristic cap check
    content = result.content[0].text
    assert len(content) <= 17000 # Buffer for headers etc
    assert "[TRUNCATED]" in content or "(chunked)" in content or len(content) < 20000

@pytest.mark.asyncio
async def test_ingest_query_filtering(mcp_server, test_workspace):
    """Verify that the query filter only extracts relevant sections."""
    # Build a file > 4000 chars to ensure BANANA window excludes APPLE
    content = "APPLE: Red fruit\n" + ("." * 4000) + "\nBANANA: Yellow fruit\n" + ("." * 4000) + "\nCHERRY: Small red fruit"
    fpath = os.path.join(test_workspace, "fruits.txt")
    with open(fpath, "w") as f:
        f.write(content)

    rel_path = "temp__mem/Head/tests/staging/fruits.txt"
    result = await mcp_server.call_tool("ingest_context", {
        "target_path": rel_path,
        "query": "BANANA"
    })
    
    text = result.content[0].text
    assert "BANANA" in text
    assert "Yellow fruit" in text
    assert "APPLE" not in text
