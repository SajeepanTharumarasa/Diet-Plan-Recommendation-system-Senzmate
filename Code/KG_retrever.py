from neo4j import GraphDatabase

# generate a cyber text with conditions for KG data retrival.
uri = "neo4j+s://75b6527a.databases.neo4j.io"
user = "neo4j"
password = "dey-uWoTDE9TljwOirEmfnh6s0SpCeCb7GK4_oUUzRs"

driver = GraphDatabase.driver(uri, auth=(user, password))


def run_query(region, diet, condition, type, value):
    v_min = value-200
    v_max = value+200
    query_foods = f"""
    MATCH (det)-[:who_has]->(con)-[:aims]->(g)-[:can_have]->(b)-[:and]->(ms)-[:and]->(l)-[:and]->(es)-[:and]->(dn)-[:and]->(pos)-[:and]->(pre)
      WHERE det.Region = "{region}"
      AND det.Diet = "{diet}"
      AND g.Type = "{type}"
      AND con.Condition = "{condition}"
      AND {v_min} <= det.Value <= {v_max}
    RETURN 
      det.Region AS Region,
      det.Diet AS DietType,
      g AS Goal, con AS Condition,
      b AS BreakfastItems,
      ms AS MorningSnackItems,
      l AS LunchItems,
      es AS EveningSnackItems,
      dn AS DinnerItems,
      pos AS PostWorkoutSnackItems,
      pre AS PreWorkoutSnackItems
    LIMIT 20
    """
    print(query_foods)
    with driver.session() as session:
        result = session.run(query_foods)
        return [record.data() for record in result]


