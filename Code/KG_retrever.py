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
    LIMIT 40
    """
    print(query_foods)
    with driver.session() as session:
        result = session.run(query_foods)
        return [record.data() for record in result]

# Define the query
query_break = """
MATCH (ft)-[:foods_for]->(dis)-[:condition_who_aims]->(g)-[:and_likes]->(fc)-[:can_have]->(b:Breakfast_Items)
WHERE fc.Region = '{region}'
  AND ft.Diet = '{diet}'
  AND g.Type = '{d_type}'
  AND dis.Condition = '{condition}'
RETURN DISTINCT b.br as Breakfast_combo
LIMIT 4
"""
query_dinner = """
MATCH (ft)-[:foods_for]->(dis)-[:condition_who_aims]->(g)-[:and_likes]->(fc)-[:can_have]->(d:Dinner_Items) 
WHERE fc.Region = '{region}'
  AND ft.Diet = '{diet}'
  AND g.Type = '{d_type}'
  AND dis.Condition = '{condition}'
RETURN DISTINCT d.dn as Dinner_combo
LIMIT 4
"""

query_lunch = """
MATCH (ft)-[:foods_for]->(dis)-[:condition_who_aims]->(g)-[:and_likes]->(fc)-[:can_have]->(l:Lunch_Items) 
WHERE fc.Region = '{region}'
  AND ft.Diet = '{diet}'
  AND g.Type = '{d_type}'
  AND dis.Condition = '{condition}'
RETURN DISTINCT l.lu as Lunch_combo
LIMIT 3
"""

query_morn_snack = """
MATCH (ft)-[:foods_for]->(dis)-[:condition_who_aims]->(g)-[:and_likes]->(fc)-[:can_have]->(m:Mor_snac_Items) 
WHERE fc.Region = '{region}'
  AND ft.Diet = '{diet}'
  AND g.Type = '{d_type}'
  AND dis.Condition = '{condition}'
RETURN DISTINCT m.ms as Morning_snack_combo
LIMIT 2
"""

query_post_work = """
MATCH (ft)-[:foods_for]->(dis)-[:condition_who_aims]->(g)-[:and_likes]->(fc)-[:can_have]->(po:Post_workout_snack_Items) 
WHERE fc.Region = '{region}'
  AND ft.Diet = '{diet}'
  AND g.Type = '{d_type}'
  AND dis.Condition = '{condition}'
RETURN DISTINCT po.pos as Post_workout_snack_combo
LIMIT 3
"""
query_pre_work = """
MATCH (ft)-[:foods_for]->(dis)-[:condition_who_aims]->(g)-[:and_likes]->(fc)-[:can_have]->(pr:Pre_workout_snack_Items) 
WHERE fc.Region = '{region}'
  AND ft.Diet = '{diet}'
  AND g.Type = '{d_type}'
  AND dis.Condition = '{condition}'
RETURN DISTINCT pr.prs as Post_workout_snack_combo
LIMIT 2
"""
def KG_data_retiver(region,diet,d_type,condition):
  kg_data = []
  querys = [query_break,query_lunch,query_dinner,query_morn_snack,query_post_work,query_pre_work]
  for query in querys:
    food_query =  query.format(region=region,diet=diet,d_type=d_type,condition=condition)
    # Execute the query and collect the results
    with driver.session() as session:
        results = session.run(food_query)
        food_items = [record for record in results]
    kg_data.append(food_items)
    # # Print the collected results
    # for result in food_items:
    #   print(result)

  return kg_data
