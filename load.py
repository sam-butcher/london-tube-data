import psycopg2
import json

conn = psycopg2.connect(
    dbname="vaticle",
    user = "vaticle",
    host = "localhost",
    password = "postgres"
)

cur = conn.cursor()

cur.execute("DROP TABLE stations CASCADE;")

cur.execute("""
CREATE TABLE stations (
    stationId VARCHAR PRIMARY KEY, 
    name VARCHAR, 
    latitude FLOAT, 
    longitude FLOAT
);""")

cur.execute("DROP TABLE lines CASCADE;")

cur.execute("""
CREATE TABLE lines (
    lineId INTEGER PRIMARY KEY, 
    name VARCHAR
);""")

cur.execute("DROP TABLE connections;")

cur.execute("""
CREATE TABLE connections (
    lineId INTEGER REFERENCES lines(lineId),
    stationId VARCHAR REFERENCES stations(stationId),
    PRIMARY KEY(lineId, stationId)
);""")

f = open('train-network.json')

data = json.load(f)

for i in data['stations']:
    cur.execute("""
    INSERT INTO stations (stationId, name, latitude, longitude)
    VALUES(%s, %s, %s, %s);
    """, (i['id'], i['name'], i['latitude'], i['longitude']))

lineId = 0
for i in data['lines']:
    cur.execute("""
    INSERT INTO lines (lineId, name)
    VALUES(%s, %s);
    """, (lineId, i['name']))
    for j in i['stations']:
        cur.execute("""
        INSERT INTO connections (lineId, stationId)
        VALUES(%s, %s);
        """, (lineId, j))
    lineId += 1

f.close()

cur.close()

conn.commit()