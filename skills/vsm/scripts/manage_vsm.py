import argparse
import json
from pathlib import Path

def generate_vsm_report(name, tokens, tool_sequence, mudas):
    """
    Standardizes the Poka-yoke VSM output.
    """
    report = f"""# Value Stream Map: {name}

## 1. Current State Diagnostics (Metric-Evidence)
- **Token Usage:** {tokens}
- **Tool Sequence:** {tool_sequence}
- **Fault Clusters:** [Check Jidoka logs for {name}]

## 2. Bottlenecks & Muda Identification
"""
    for muda in mudas:
        report += f"- **{muda['type']}:** {muda['description']}\n"
    
    report += """
## 3. Future State Proposal
[Agent: Describe the optimized flow here based on the data above.]

## 4. Associated Hazards (KYT Required)
- **KYT Note:** Mandatory hazard prediction pass required before implementing changes to this value stream.
"""
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic VSM Report Generator")
    parser.add_argument("--name", required=True, help="Name of the process being mapped")
    parser.add_argument("--tokens", required=True, help="Approximate token consumption")
    parser.add_argument("--tools", required=True, help="Sequence of tool calls")
    parser.add_argument("--muda", action="append", help="Add a Muda (Waste) identification (Format: 'Type:Description')")

    args = parser.parse_args()
    
    mudas = []
    if args.muda:
        for m in args.muda:
            if ":" in m:
                t, d = m.split(":", 1)
                mudas.append({"type": t.strip(), "description": d.strip()})
    
    print(generate_vsm_report(args.name, args.tokens, args.tools, mudas))
