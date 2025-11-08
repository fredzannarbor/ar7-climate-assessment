#!/usr/bin/env python3
"""
add_citations_to_prompts.py

Programmatically add literature search and citation requirements to all AR7 prompts.
"""

import json
from pathlib import Path

# Citation guidance templates
LITERATURE_SEARCH_TEMPLATE = """
**MANDATORY FIRST STEP: COMPREHENSIVE LITERATURE SEARCH**

Before writing, conduct thorough search of peer-reviewed scientific literature published between:
- **AR6 Literature Cutoff**: November 1, 2020
- **AR7 Literature Cutoff**: June 30, 2026

Search for relevant publications on {search_topics}.

**Search Databases**:
- Web of Science
- Scopus
- PubMed (health/biology topics)
- Google Scholar
- Discipline-specific databases

**Priority Sources**:
1. Peer-reviewed journal articles (highest priority)
2. IPCC special reports and updates
3. National climate assessments
4. Major international reports (UNEP, WMO, etc.)

"""

CITATION_REQUIREMENT_TEMPLATE = """
**STRICT CITATION REQUIREMENT**:

EVERY significant factual statement, quantitative finding, or assessment conclusion MUST be supported by in-text citations.

**Citation Format**:
- Single study: (Author et al., 2024)
- Multiple studies: (Author1 et al., 2023; Author2 et al., 2024; Author3 et al., 2025)
- Quantitative claims: "X increased by Y% (Author et al., 2024)"

**Examples of properly cited statements**:
- "Global mean temperature increased by 1.2°C since pre-industrial times (IPCC, 2023; Smith et al., 2024)."
- "Coral reefs face existential threats at 1.5°C warming (Hughes et al., 2024; Frieler et al., 2025)."
- "Adaptation finance flows reached $50 billion in 2024 (UNEP, 2025), representing only 10% of estimated needs (Kumar et al., 2024)."

**Reference List Format**:
Author, A.B., Author, C.D., & Author, E.F. (Year). Article title. Journal Name, Volume(Issue), pages. https://doi.org/XX.XXXX/xxxxx

"""

MANDATORY_ENDING = """
**REQUIRED: Complete References Section**

End the chapter with a comprehensive References section listing all cited works in alphabetical order by first author. Use standard academic citation format with DOIs where available.
"""

# Search topics by chapter type
SEARCH_TOPICS = {
    "summary": "climate impacts, projections, adaptation progress, loss and damage across all sectors and regions",
    "framing": "vulnerability frameworks, risk assessment methodologies, adaptation concepts, climate justice",
    "impacts": "observed impacts, attribution studies, climate projections, risk assessments, tipping points",
    "adaptation": "adaptation effectiveness, monitoring and evaluation, gaps and barriers, capacity building",
    "options": "adaptation interventions, feasibility studies, best practices, technology innovation",
    "loss_damage": "loss quantification, attribution, response mechanisms, insurance, compensation frameworks",
    "finance": "climate finance flows, needs assessments, funding mechanisms, investment analyses",
    "regional": "regional climate impacts, vulnerabilities, adaptation measures, case studies for {region}",
    "ecosystem": "ecosystem impacts, biodiversity loss, ecosystem services, nature-based solutions for {system}",
    "sectoral": "sectoral climate impacts, adaptation measures, vulnerability assessments for {sector}",
    "annexes": "methodologies, definitions, data sources, mapping techniques",
    "tgia": "assessment methodologies, best practices, implementation guidance, indicators and metrics"
}


def add_citation_requirements(prompt_data: dict, chapter_key: str) -> dict:
    """Add literature search and citation requirements to a prompt"""

    # Determine search topics based on chapter type
    if "summary" in chapter_key:
        search_topic = SEARCH_TOPICS["summary"]
    elif "chapter_1" in chapter_key:
        search_topic = SEARCH_TOPICS["framing"]
    elif "chapter_2" in chapter_key or "vulnerabilities" in chapter_key:
        search_topic = SEARCH_TOPICS["impacts"]
    elif "chapter_3" in chapter_key or "adaptation_progress" in chapter_key:
        search_topic = SEARCH_TOPICS["adaptation"]
    elif "chapter_4" in chapter_key or "adaptation_options" in chapter_key:
        search_topic = SEARCH_TOPICS["options"]
    elif "chapter_5" in chapter_key or "losses_damages" in chapter_key:
        search_topic = SEARCH_TOPICS["loss_damage"]
    elif "chapter_6" in chapter_key or "finance" in chapter_key:
        search_topic = SEARCH_TOPICS["finance"]
    elif any(reg in chapter_key for reg in ["africa", "asia", "australasia", "america", "europe", "north_america", "small_islands"]):
        region = chapter_key.split("_")[-1] if "_" in chapter_key else "the region"
        search_topic = SEARCH_TOPICS["regional"].format(region=region)
    elif any(eco in chapter_key for eco in ["ecosystem", "terrestrial", "ocean", "coastal"]):
        system = "terrestrial and freshwater" if "terrestrial" in chapter_key else "ocean and coastal"
        search_topic = SEARCH_TOPICS["ecosystem"].format(system=system)
    elif any(sec in chapter_key for sec in ["water", "agriculture", "settlements", "health", "poverty"]):
        sector = chapter_key.split("_")[-1] if "_" in chapter_key else "the sector"
        search_topic = SEARCH_TOPICS["sectoral"].format(sector=sector)
    elif "annex" in chapter_key:
        search_topic = SEARCH_TOPICS["annexes"]
    elif "tgia" in chapter_key:
        search_topic = SEARCH_TOPICS["tgia"]
    else:
        search_topic = "climate change impacts, adaptation, and vulnerability"

    # Add to system prompt if there are messages
    if "messages" in prompt_data and len(prompt_data["messages"]) > 0:
        # Find system message
        system_idx = None
        user_idx = None

        for i, msg in enumerate(prompt_data["messages"]):
            if msg.get("role") == "system":
                system_idx = i
            elif msg.get("role") == "user":
                user_idx = i

        # Add to system message
        if system_idx is not None:
            original_system = prompt_data["messages"][system_idx]["content"]
            if "MANDATORY CITATION" not in original_system:
                prompt_data["messages"][system_idx]["content"] = original_system + "\n\n" + CITATION_REQUIREMENT_TEMPLATE

        # Add to user message
        if user_idx is not None:
            original_user = prompt_data["messages"][user_idx]["content"]
            if "LITERATURE SEARCH REQUIRED" not in original_user:
                lit_search = LITERATURE_SEARCH_TEMPLATE.format(search_topics=search_topic)
                new_user = lit_search + "\n" + CITATION_REQUIREMENT_TEMPLATE + "\n" + original_user + "\n\n" + MANDATORY_ENDING
                prompt_data["messages"][user_idx]["content"] = new_user

    return prompt_data


def main():
    # Load original prompts
    original_file = Path("prompts/ar7_model_comparison_prompts.json")
    output_file = Path("prompts/ar7_model_comparison_prompts_v2_full_cited.json")

    print(f"Loading: {original_file}")

    with open(original_file) as f:
        prompts_data = json.load(f)

    print(f"Found {len(prompts_data.get('prompt_keys', []))} chapters")

    # Add metadata about revision
    if "metadata" not in prompts_data:
        prompts_data["metadata"] = {}

    prompts_data["metadata"].update({
        "version": "2.0_full_cited",
        "revised_date": "2025-01-07",
        "revision": "Added mandatory literature search (Nov 2020-June 2026) and citation requirements to all prompts",
        "citation_policy": "Every significant factual statement must be cited"
    })

    # Add citation requirements section
    prompts_data["citation_requirements"] = {
        "mandatory": True,
        "literature_period": {
            "start": "2020-11-01",
            "end": "2026-06-30",
            "description": "AR6 cutoff to AR7 cutoff"
        },
        "citation_format": "In-text: (Author et al., Year). References at end with full citations.",
        "minimum_citations_per_chapter": 50,
        "reference_list_required": True
    }

    # Process each chapter
    chapters_updated = 0

    for chapter_key in prompts_data.get("prompt_keys", []):
        if chapter_key in prompts_data:
            print(f"Updating: {chapter_key}")
            prompts_data[chapter_key] = add_citation_requirements(
                prompts_data[chapter_key],
                chapter_key
            )
            chapters_updated += 1

    # Save updated prompts
    with open(output_file, 'w') as f:
        json.dump(prompts_data, f, indent=2)

    print(f"\n✅ Updated {chapters_updated} chapters")
    print(f"✅ Saved to: {output_file}")
    print(f"\nAll prompts now include:")
    print(f"  • Mandatory literature search (Nov 2020 - June 2026)")
    print(f"  • Strict citation requirements")
    print(f"  • Reference list requirements")
    print(f"  • Search strategy guidance")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
