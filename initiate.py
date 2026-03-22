from fastapi import WebSocket
from dotenv import load_dotenv
import os
import json
import requests

from scene_graph import scene_graph_template
from dependency import denpendency_template

"""
generate scene graph and dependecies by raw svg
"""


async def initiate(ws: WebSocket, data: dict):
    load_dotenv()
    svg_code = data.get("svg")

    # generate scene graph
    print("generating scene graph")
    print("====================")
    await ws.send_json({"type": "status", "message": "Generating scene graph"})
    scene_graph_prompt = build_scene_graph_prompt(svg_code)
    scene_graph_text = call_model(scene_graph_prompt)

    # generate dependencies
    print("generating dependencies")
    print("====================")
    await ws.send_json({"type": "status", "message": "Generating dependencies"})
    dependencies_prompt = build_dependencies_prompt(svg_code, scene_graph_text)
    dependencies_text = call_model(dependencies_prompt)

    # send results
    print("sending results")
    print("====================")
    await ws.send_json(
        {
            "type": "result",
            "scene_graph": scene_graph_text,
            "dependencies": dependencies_text,
        }
    )


def call_model(prompt):
    headers = {
        "Authorization": f"Bearer {os.getenv("API_KEY")}",
        "Content-Type": "application/json",
    }

    data = {
        "model": os.getenv("OPENAI_MODEL", "gpt-5.1"),
        "messages": [
            {
                "role": "system",
                "content": "You are an expert SVG scene graph generator.",
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


def build_scene_graph_prompt(svg_text):
    return (
        "You are given an SVG string and a Scene Graph JSON template.\n"
        "Your task is to analyze the SVG and populate the template with concrete values.\n\n"
        "Requirements:\n"
        "1. Strictly follow the provided JSON schema. Do NOT change field names or structure.\n"
        "2. You MAY expand list-type fields (e.g., marks, ticks, legend items) to include multiple instances if needed.\n"
        "3. Do NOT add new keys that are not defined in the templates.\n"
        "4. Only fill in values that can be directly inferred from the SVG.\n"
        "5. If a value cannot be determined, set it to null.\n"
        "6. Preserve all hierarchical relationships and nesting.\n"
        "Output Format:\n"
        "- Return ONLY a valid JSON object for the scene graph.\n"
        "- Do NOT include any explanations, comments, or extra text.\n\n"
        "SVG:\n"
        f"{svg_text}\n\n"
        "SceneGraph Template:\n"
        f"{json.dumps(scene_graph_template, ensure_ascii=False, indent=2)}\n"
    )


def build_dependencies_prompt(svg_text, scene_graph):
    return (
        "You are given an SVG string, a Scene Graph JSON, and a Dependencies JSON template.\n"
        "Your task is to analyze the SVG and the Scene Graph, then populate the Dependencies template.\n\n"
        "Requirements:\n"
        "1. Strictly follow the provided JSON schema, but you MAY add optional fields if they help explicit reasoning (e.g., element_id, element_path, svg_selector, hierarchy_path, source_value, target_value).\n"
        "2. For each dependency, locate the corresponding SVG element pair and extract concrete attributes and values from the SVG (positions, sizes, domains, transforms).\n"
        "3. Populate dependencies with these concrete element references and values so the relationships are explicit and traceable.\n"
        "4. You MAY adapt the dependencies content to make global-edit reasoning easier, as long as the JSON remains valid and consistent.\n"
        "5. Only include relationships that are clearly supported by the SVG.\n"
        "6. Ensure all referenced elements exist in the provided scene_graph.\n"
        "7. Avoid redundant or duplicated dependencies.\n\n"
        "Output Format:\n"
        "- Return ONLY a valid JSON object for dependencies.\n"
        "- Do NOT include any explanations, comments, or extra text.\n\n"
        "SVG:\n"
        f"{svg_text}\n\n"
        "SceneGraph:\n"
        f"{json.dumps(scene_graph, ensure_ascii=False, indent=2)}\n\n"
        "Dependencies Template:\n"
        f"{json.dumps(denpendency_template, ensure_ascii=False, indent=2)}\n"
    )
