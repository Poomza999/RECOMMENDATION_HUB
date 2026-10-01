#!/usr/bin/env python3
"""Update all Food nodes in Neo4j with image data from data.json"""

import json
from neo4j_service import query

# Load data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Delete all existing Food nodes
print("Deleting existing Food nodes...")
query("MATCH (f:Food) DETACH DELETE f;", w=True)

# Re-insert Food nodes with image data
print("Inserting Food nodes with image data...")
query(
    """
    UNWIND $x AS x
    CREATE (f:Food {name:x.name, image_url:x.image_url, image_data:x.image_data})
    """,
    {"x": data["foods"]},
    w=True
)

print("Done! All Food nodes updated with images.")
print(f"Total: {len(data['foods'])} foods")
