#libraries
import psycopg2
import pandas as pd

#Connection to database
conn = psycopg2.connect( 
    database='fifa',
    user='username',
    password='secret',
    host='database'  
)

#Cursor 
cur = conn.cursor()

#Query the database

#Tables's samples
#World Cups
cur.execute("SELECT * FROM worldcups LIMIT 5")
wcrows = cur.fetchall()
# getting col names for display df
wccol_names = [desc[0].upper() for desc in cur.description]
dfwc = pd.DataFrame(wcrows, columns=wccol_names)

#World Matches
cur.execute("SELECT * FROM worldcupmatches LIMIT 5")
wmrows = cur.fetchall()
wmcol_names = [desc[0].upper() for desc in cur.description]
dfwm = pd.DataFrame(wmrows, columns=wmcol_names)

#World Players
cur.execute("SELECT * FROM worldcupplayers LIMIT 5")
wprows = cur.fetchall()
wpcol_names = [desc[0].upper() for desc in cur.description]
dfwp = pd.DataFrame(wprows, columns=wpcol_names)

#Additional queries
#Group by Wins, Looses, Draws
cur.execute("""WITH totals
AS
(
SELECT 
home_team_name AS team_name, home_team_initials AS team_initials,
(CASE 
WHEN home_team_goals > away_team_goals THEN 'Won'
WHEN home_team_goals < away_team_goals THEN 'Lost'
ELSE 'Draw' END) AS result
FROM worldcupmatches
 
UNION ALL

SELECT 
away_team_name AS team_name, away_team_initials AS team_initials,
(CASE 
WHEN away_team_goals > home_team_goals THEN 'Won'
WHEN away_team_goals < home_team_goals THEN 'Lost'
ELSE 'Draw' END) AS result
FROM worldcupmatches)
SELECT *, COUNT(*)
FROM totals 
GROUP BY team_name, team_initials, result
ORDER BY team_name ASC""")

total_results = cur.fetchall()
trcol_names = [desc[0] for desc in cur.description]
dftotal_results = pd.DataFrame(total_results, columns=trcol_names)

#All-time Champions
cur.execute("""SELECT winner, COUNT(*)
FROM worldcups
GROUP BY winner
ORDER BY count DESC""")

champions = cur.fetchall()
col_names = [desc[0] for desc in cur.description]
dfchampions = pd.DataFrame(champions, columns=col_names)

#Qty of participations in World cups
cur.execute("""SELECT DISTINCT(home_team_name), count(*) OVER (PARTITION BY home_team_name)
FROM worldcupmatches
GROUP BY year, home_team_name
ORDER BY count DESC""")

participations = cur.fetchall()
col_names = [desc[0] for desc in cur.description]
dfparticipations = pd.DataFrame(participations, columns=col_names)

#print(dfparticipations.head(3))

#Total attendance per country
cur.execute("""WITH total_attendance
AS(

SELECT home_team_name AS team ,attendance
FROM worldcupmatches

UNION ALL


SELECT away_team_name AS team, attendance
FROM worldcupmatches
)

SELECT team, SUM(attendance) AS Total
FROM total_attendance
GROUP BY team
ORDER BY SUM(attendance) DESC""")

totalatt = cur.fetchall()
col_names = [desc[0] for desc in cur.description]
dftotalatt = pd.DataFrame(totalatt, columns=col_names)


#Goals per half
cur.execute("""WITH total_half
AS(
SELECT 
year, (home_team_goals+away_team_goals) AS total_goals, (half_time_home_goals + half_time_away_goals) AS half_time_goals
FROM worldcupmatches
)

SELECT wc.country, th.year, SUM(total_goals) AS total_goals, SUM(half_time_goals) AS total_first_half, 
(SUM(total_goals) -  SUM(half_time_goals)) AS second_half_goals,
ROUND(((SUM(half_time_goals) * 1.00) /  (SUM(total_goals)*1.00)),2) AS perc_first_half,
ROUND((((SUM(total_goals) -  SUM(half_time_goals))* 1.00) /  (SUM(total_goals)*1.00)),2) AS perc_first_half
FROM total_half th
INNER JOIN worldcups wc ON th.year = wc.year
GROUP BY th.year, wc.country""")

goalshalf = cur.fetchall()
col_names = [desc[0] for desc in cur.description]
dfgoalshalf = pd.DataFrame(goalshalf, columns=col_names)

#Total goals per year

cur.execute("""WITH total_goals
AS
(
SELECT 
home_team_name AS team_name, home_team_initials AS team_initials, year,
SUM(home_team_goals) AS goals
FROM worldcupmatches
GROUP BY home_team_name, home_team_initials, year

 
UNION ALL

SELECT 
away_team_name AS team_name, away_team_initials AS team_initials, year,
SUM(away_team_goals) AS goals
FROM worldcupmatches
GROUP BY away_team_name, away_team_initials, year

)

SELECT *
FROM total_goals
ORDER BY year""")

totgoals = cur.fetchall()
col_names = [desc[0] for desc in cur.description]
dftotgoals = pd.DataFrame(totgoals, columns=col_names)







#World Cups - full
cur.execute("SELECT * FROM worldcups")
wcall = cur.fetchall()
# getting col names for display df
wcacol_names = [desc[0] for desc in cur.description]
dfwcall = pd.DataFrame(wcall, columns=wcacol_names)

#World Players - full
cur.execute("SELECT * FROM worldcupplayers")
wpall = cur.fetchall()
# getting col names for display df
wpacol_names = [desc[0] for desc in cur.description]
dfwpall = pd.DataFrame(wpall, columns=wpacol_names)


#World Matches - full
cur.execute("SELECT * FROM worldcupmatches")
wmall = cur.fetchall()
# getting col names for display df
wmacol_names = [desc[0] for desc in cur.description]
dfwmall = pd.DataFrame(wmall, columns=wmacol_names)


#print(dfgoalshalf.head(3))
#print(dftotal_results.head(3))
#print(dfchampions.head(3))
#print(dfparticipations.head(3))
#print(dftotalatt.head(3))


cur.close()
conn.close()