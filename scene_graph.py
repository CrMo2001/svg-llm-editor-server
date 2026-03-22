scene_graph_template = {
    "chart": {
        "type": "chart",
        "titles": [
            {
                "type": "text",
                "role": "chart_title",
                "content": {},
                "style": {},
                "position": {},
            }
        ],
        "backgrounds": [{"type": "background", "style": {}, "geometry": {}}],
        "axes": [
            {
                "type": "axis",
                "orientation": "x | y",
                "scale_ref": "string",
                "components": {
                    "domain": {"type": "line", "style": {}, "position": {}},
                    "ticks": [{"type": "line", "position": {}, "style": {}}],
                    "labels": [
                        {"type": "text", "content": {}, "position": {}, "style": {}}
                    ],
                    "title": {
                        "type": "text",
                        "content": {},
                        "position": {},
                        "style": {},
                    },
                },
            }
        ],
        "legend": {
            "type": "legend",
            "title": {"type": "text", "content": {}, "style": {}, "position": {}},
            "items": [
                {
                    "type": "legend_item",
                    "data_key": "string",
                    "mark": {
                        "type": "symbol",
                        "style": {},
                        "geometry": {},
                        "position": {},
                    },
                    "label": {
                        "type": "text",
                        "content": {},
                        "style": {},
                        "position": {},
                    },
                }
            ],
        },
        "grids": {
            "gridX": [{"type": "line", "position": {}, "style": {}}],
            "gridY": [{"type": "line", "position": {}, "style": {}}],
        },
        "marks": [
            {
                "type": "mark_group",
                "mark_type": "rect | circle | line | arc | area | point",
                "data_key": "string",
                "encoding": {
                    "position": ["x", "y"],
                    "size": ["width", "height", "radius"],
                    "style": ["fill", "stroke", "opacity"],
                    "geometry": ["angle", "innerRadius", "outerRadius"],
                    "text": ["label", "value"],
                },
                "marks": [
                    {
                        "type": "mark",
                        "position": {},
                        "size": {},
                        "style": {},
                        "geometry": {},
                        "data": {},
                    }
                ],
                "labels": [
                    {
                        "type": "text",
                        "role": "mark_label | value_label",
                        "content": {},
                        "position": {},
                        "style": {},
                    }
                ],
                "subgroups": [{"type": "mark_group"}],
            }
        ],
    }
}
