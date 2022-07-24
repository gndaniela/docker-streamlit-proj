import psycopg2

#Connection to database
conn = psycopg2.connect( 
    database='fifa',
    user='username',
    password='secret',
    host='database'  
)

#Cursor 
cur = conn.cursor()

#Insert data into tables
with open('./files/WorldCups.csv') as csvFile:
    next(csvFile) # skip headers
    cur.copy_from(csvFile, "worldcups", sep=",", null='')
    conn.commit()

with open('./files/WorldCupMatches.csv') as csvFile:
    next(csvFile) # skip headers
    cur.copy_from(csvFile, "worldcupmatches", sep=",", null='')
    conn.commit()

with open('./files/WorldCupPlayers.csv') as csvFile:
    next(csvFile) # skip headers
    cur.copy_from(csvFile, "worldcupplayers", sep=",", null='')
    conn.commit()

#Add primary and foreign keys
cur.execute("""ALTER TABLE worldcups
  ADD CONSTRAINT worldcups_pk 
    PRIMARY KEY ("year");""")

cur.execute("""ALTER TABLE worldcupmatches
  ADD CONSTRAINT worldcupmatches_pk 
    PRIMARY KEY (matchid);""")    

cur.execute("""ALTER TABLE worldcupmatches
  ADD CONSTRAINT worldcupmatches_fk 
    FOREIGN KEY ("year") REFERENCES worldcups("year");""")  

cur.execute("""ALTER TABLE worldcupplayers
  ADD CONSTRAINT worldcupplayers_fk 
    FOREIGN KEY (matchid) REFERENCES worldcupmatches(matchid);""")  

#Close communication with database
cur.close()
conn.close()  

