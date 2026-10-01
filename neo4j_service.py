from pathlib import Path
import json
import os
import streamlit as st
from neo4j import GraphDatabase, RoutingControl
from dotenv import load_dotenv

load_dotenv()

DATA = json.loads(
    (Path(__file__).parent / "data.json").read_text(encoding="utf-8")
)


@st.cache_resource
def get_driver():
    try:
        c = st.secrets["neo4j"]
    except (KeyError, FileNotFoundError):
        c = {
            "uri": os.getenv("NEO4J_URI"),
            "username": os.getenv("NEO4J_USERNAME"),
            "password": os.getenv("NEO4J_PASSWORD"),
            "database": os.getenv("NEO4J_DATABASE", "neo4j")
        }

    driver = GraphDatabase.driver(
        c["uri"],
        auth=(c["username"], c["password"])
    )

    driver.verify_connectivity()
    return driver


def query(c, p=None, w=False):
    records, _, _ = get_driver().execute_query(
        c,
        parameters_=p or {},
        database_=st.secrets["neo4j"].get("database", "neo4j"),
        routing_=RoutingControl.WRITE if w else RoutingControl.READ
    )

    return [x.data() for x in records]


def setup_data():

    # -----------------------------
    # Constraints
    # -----------------------------
    query(
        """
        CREATE CONSTRAINT user_name_unique
        IF NOT EXISTS
        FOR (n:User)
        REQUIRE n.name IS UNIQUE
        """,
        w=True
    )

    query(
        """
        CREATE CONSTRAINT food_name_unique
        IF NOT EXISTS
        FOR (n:Food)
        REQUIRE n.name IS UNIQUE
        """,
        w=True
    )

    # -----------------------------
    # Users
    # -----------------------------
    query(
        """
        UNWIND $x AS n
        MERGE (:User {name:n})
        """,
        {"x": DATA["users"]},
        True
    )

    # -----------------------------
    # Foods
    # -----------------------------
    query(
        """
        UNWIND $x AS x

        MERGE (f:Food {name:x.name})

        SET
            f.image_url = coalesce(f.image_url, x.image_url),
            f.image_data = x.image_data
        """,
        {"x": DATA["foods"]},
        True
    )

    # -----------------------------
    # Orders / selections
    # -----------------------------
    query(
        """
        UNWIND $x AS x

        MATCH (u:User {name:x.user})
        MATCH (f:Food {name:x.food})

        MERGE (u)-[r:ORDERED]->(f)

        ON CREATE SET
            r.ordered_at = date('2026-09-01')
        """,
        {"x": DATA["likes"]},
        True
    )

    # -----------------------------
    # Generate friendships
    # -----------------------------
    query(
        """
        MATCH (a:User)-[:ORDERED]->(f)<-[:ORDERED]-(b:User)

        WHERE a.name < b.name

        WITH
            a,
            b,
            count(DISTINCT f) AS shared_foods

        WHERE shared_foods > 0

        MERGE (a)-[:FRIEND]->(b)
        """,
        w=True
    )

    # -----------------------------
    # Migrate old relationships
    # -----------------------------
    query(
        """
        MATCH (u:User)-[:LIKES|RENTED]->(f:Food)

        MERGE (u)-[:ORDERED]->(f)
        """,
        w=True
    )


def users():
    return [
        x["name"]
        for x in query(
            """
            MATCH (u:User)
            RETURN u.name AS name
            ORDER BY name
            """
        )
    ]


def foods():
    return query(
        """
        MATCH (f:Food)

        RETURN
            f.name AS name,
            f.image_url AS image_url,
            f.image_data AS image_data

        ORDER BY name
        """
    )


def friends(u):
    return [
        x["name"]
        for x in query(
            """
            MATCH (:User {name:$u})-[:FRIEND]-(f:User)

            RETURN DISTINCT
                f.name AS name

            ORDER BY name
            """,
            {"u": u}
        )
    ]


def stats():

    result = query(
        """
        MATCH (u:User)
        WITH count(u) AS users

        MATCH (f:Food)
        WITH users, count(f) AS foods

        OPTIONAL MATCH (:User)-[fr:FRIEND]-(:User)

        WITH
            users,
            foods,
            count(fr) / 2 AS friendships

        OPTIONAL MATCH (:User)-[o:ORDERED]->(:Food)

        RETURN
            users,
            foods,
            friendships,
            count(o) AS orders
        """
    )

    if result:
        return result[0]

    return {
        "users": 0,
        "foods": 0,
        "friendships": 0,
        "orders": 0
    }


def recommendations(u):

    return query(
        """
        MATCH (me:User {name:$u})
              -[:FRIEND]-
              (friend:User)
              -[:ORDERED]->
              (food:Food)

        WHERE NOT EXISTS {
            MATCH (me)-[:ORDERED]->(food)
        }

        WITH
            food,
            collect(DISTINCT friend.name) AS friend_names,
            count(DISTINCT friend) AS score

        RETURN
            food.name AS name,
            food.image_url AS image_url,
            food.image_data AS image_data,
            friend_names,
            score

        ORDER BY
            score DESC,
            food.name
        """,
        {"u": u}
    )


def add_user(n):

    n = n.strip()

    if n:
        query(
            """
            MERGE (:User {name:$n})
            """,
            {"n": n},
            True
        )


def add_friend(a, b):

    if a != b:
        query(
            """
            MATCH (a:User {name:$a})
            MATCH (b:User {name:$b})

            MERGE (a)-[:FRIEND]->(b)
            """,
            {
                "a": a,
                "b": b
            },
            True
        )


def remove_friend(a, b):

    query(
        """
        MATCH (a:User {name:$a})
              -[r:FRIEND]-
              (b:User {name:$b})

        DELETE r
        """,
        {
            "a": a,
            "b": b
        },
        True
    )


def delete_user(n):

    query(
        """
        MATCH (u:User {name:$n})
        DETACH DELETE u
        """,
        {"n": n},
        True
    )


def add_food(n, url="", data=""):

    n = n.strip()

    if n:
        query(
            """
            MERGE (f:Food {name:$n})

            SET
                f.image_url = $url,
                f.image_data = $data
            """,
            {
                "n": n,
                "url": url,
                "data": data
            },
            True
        )


def delete_food(n):

    query(
        """
        MATCH (f:Food {name:$n})
        DETACH DELETE f
        """,
        {"n": n},
        True
    )


def order(u, n):

    query(
        """
        MATCH (u:User {name:$u})
        MATCH (f:Food {name:$n})

        MERGE (u)-[r:ORDERED]->(f)

        SET r.ordered_at = date()
        """,
        {
            "u": u,
            "n": n
        },
        True
    )


def remove_order(u, n):

    query(
        """
        MATCH (:User {name:$u})
              -[r:ORDERED]->
              (:Food {name:$n})

        DELETE r
        """,
        {
            "u": u,
            "n": n
        },
        True
    )


def ordered(u):

    return query(
        """
        MATCH (:User {name:$u})
              -[r:ORDERED]->
              (f:Food)

        RETURN
            f.name AS name

        ORDER BY name
        """,
        {"u": u}
    )


def edges(person=None, show_orders=True):

    p = {"u": person} if person else {}

    if person:
        users_clause = "MATCH (u:User {name:$u})"
    else:
        users_clause = "MATCH (u:User)"

    fs = query(
        users_clause
        + """
        MATCH (u)-[:FRIEND]-(f:User)

        RETURN DISTINCT
            u.name AS a,
            f.name AS b
        """,
        p
    )

    if show_orders:
        os = query(
            users_clause
            + """
            MATCH (u)-[:ORDERED]->(f:Food)

            RETURN
                u.name AS a,
                f.name AS b
            """,
            p
        )
    else:
        os = []

    return fs, os