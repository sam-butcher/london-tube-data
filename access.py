import psycopg2
from itertools import groupby

conn = psycopg2.connect(
    dbname="vaticle",
    user = "vaticle",
    host = "localhost",
    password = "postgres"
)

cur = conn.cursor()

def lineToStations(line):
    cur.execute("""
    SELECT s.name, l.lineId FROM stations s
    INNER JOIN connections c ON s.stationId = c.stationId
    INNER JOIN lines l ON c.lineId = l.lineId
    WHERE l.name = %s;
    """, (line,))
    res = cur.fetchall()
    if res == []:
        print("No results found")
    else:
        outs = dict()
        for key, val in groupby(res, key=lambda elem: elem[1]):
            outs[key] = [elem[0] for elem in val]
        if len(outs) != 1:
            print("Multiple matching lines found")
        for k in outs.keys():
            print()
            print(str(outs[k]))
            print()

def stationToLines(station):
    cur.execute("""
    SELECT l.name FROM lines l
    INNER JOIN connections c ON l.lineId = c.lineId
    INNER JOIN stations s ON c.stationId = s.stationId
    WHERE s.name = %s;
    """, (station,))
    res = cur.fetchall()
    if res == []:
        print("No results found")
    else:
        print()
        print([elem[0] for elem in res])
        print() 


help_message = """Please input 'stations' followed by a line name to get all stations that a given line stops at, 
'lines' followed by a station name to get all lines that go through a given station,
'help' to display this message again, 
or 'quit' to quit."""
help_message = help_message.replace("\n", "")

print(help_message)

userIn = input("")

while userIn != "quit":
    ins = userIn.split(" ")
    if ins[0] == "stations":
        lineToStations(ins[1])
    elif ins[0] == "lines":
        stationToLines(ins[1])
    elif ins[0] == "help":
        print(help_message)
    userIn = input("Please input another query: ")

cur.close()