from neo4j import GraphDatabase

# generate a cyber text with conditions for KG data retrival.
uri = "neo4j+s://75b6527a.databases.neo4j.io"
user = "neo4j"
password = "dey-uWoTDE9TljwOirEmfnh6s0SpCeCb7GK4_oUUzRs"

driver = GraphDatabase.driver(uri, auth=(user, password))


def run_query(region, diet, condition, type, value):
    query = f"""
    MATCH (det:Diet_Details)-[s1:who_has]->(con:Condition)-[s2:aims]->(g:Goal)-[s3:can_have]->(b)-[s4:servings_of]->(bs)-[s5:contains_calories_of]->(bcal)
    WHERE det.Region = '{region}'
      AND det.Diet = '{diet}'
      AND con.Condition = '{condition}'
      AND g.Type = '{type}'
      AND det.Value = {value}
      
    RETURN
      det.Region AS Region,
      det.Diet AS Diet,
      det.Value AS Value,
      con.Condition AS Condition,
      g.Type AS GoalType,
      b AS BreakfastItems,
      bs AS BreakfastServings,
      bcal AS BreakfastCalories
    LIMIT 30
    """
    print(query)
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]


