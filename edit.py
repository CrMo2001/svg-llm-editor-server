from fastapi import WebSocket
from dotenv import load_dotenv
import os
import json
import requests


async def edit(ws: WebSocket, data: dict):
    load_dotenv()
    instruction = data.get("instruction")
    svg = data.get("svg")
    scene_graph = data.get("scene_graph")
    dependecies = data.get("dependences")

    await ws.send_json({"type": "status", "message": "Editing..."})
    result = call_model(scene_graph, dependecies, instruction, svg)
    await ws.send_json({"type": "result", "svg": result})


def call_model(scene_graph: str, dependencies: str, instruction: str, svg: str):
    headers = {
        "Authorization": f"Bearer {os.getenv("API_KEY")}",
        "Content-Type": "application/json",
    }

    prompt = (
        "You are given:\n"
        "1. A scene graph representing the structure of the SVG chart\n"
        "2. The dependency schema representing the relationships between elements\n"
        "3. An editing instruction\n\n"
        "4. The original SVG code\n\n"
        "## Task\n"
        "Perform a **global, structure-aware edit** of the SVG.\n\n"
        "---\n\n"
        "## Process (MANDATORY)\n"
        "1. Identify directly affected elements and their original values according to the svg code and scene graph.\n"
        "2. Trace dependencies using the provided JSONs (Pay special attention to `layout_cascade`).\n"
        "3. CALCULATE the new quantitative values. If mark width/height changes and padding is fixed, mathematically deduce the new axis length and viewBox dimensions.\n"
        "4. Apply edits in a consistent order: element → layout → axis → dependent elements.\n"
        "Do not skip dependency reasoning.\n\n"
        "## CRITICAL CONSTRAINTS (DO NOT VIOLATE)\n"
        "1. **ZERO DELETION**: You MUST preserve EVERY single element from the original SVG (axes, text labels, legends, ALL segments and colors of stacked bars). Do NOT delete any nodes unless explicitly requested.\n"
        "2. **NO SHORTCUTS**: Do NOT use comments like `<!-- rest of the code -->` or `...`. You MUST output the complete, fully renderable SVG code.\n"
        "3. **COORDINATE SHIFTING**: If you change the thickness/size of an element, you MUST mathematically recalculate and shift the position (e.g., `x` or `y` attribute) of ALL subsequent elements and groups. You must manually add the size difference to their coordinates to maintain the original padding/gap. Elements MUST NOT overlap.\n"
        '4. **CANVAS EXPANSION**: If the total computed layout size increases, you MUST expand the `<svg viewBox="...">` and axis lines accordingly so nothing is clipped.\n\n'
        "## Requirements\n"
        "1. Preserve stacking, alignment, and spacing constraints.\n"
        "2. Maintain consistent gaps and proportions.\n"
        "3. Ensure all elements remain within valid axis ranges.\n\n"
        "## Output Format (STRICT)\n"
        "You should only output the modified SVG code, without any additional text, comments or code blocks. The modified SVG code should be fully renderable and should not contain any syntax errors.\n\n"
        "## Goal\n"
        "Modify the SVG while preserving all structural relationships defined by the provided JSONs.\n\n"
    )
    prompt += f"SceneGraph:\n{scene_graph}\n\n"
    prompt += f"Dependency:\n{dependencies}\n\n"
    prompt += f"Instruction:\n{instruction}\n\n"
    prompt += f"SVG:\n{svg}"
    data = {
        "model": os.getenv("OPENAI_MODEL", "gpt-5.1"),
        "messages": [
            {
                "role": "system",
                "content": "You are an expert SVG editor.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
    }

    timeout = None

    response = requests.post(
        os.getenv("BASE_URL"), headers=headers, json=data, timeout=timeout
    )
    response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]
