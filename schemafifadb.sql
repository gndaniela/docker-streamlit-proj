DROP TABLE IF EXISTS "worldcups" CASCADE;
CREATE TABLE "public"."worldcups" (
    "year" integer,
    "country" character varying(50),
    "winner" character varying(50),
    "runners_up" character varying(50),
    "third" character varying(50),
    "fourth" character varying(50),
    "goalsscored" integer,
    "qualifiedteams" integer,
    "matchesplayed" integer,
    "attendance" integer
    
);

DROP TABLE IF EXISTS "worldcupmatches" CASCADE;
CREATE TABLE "public"."worldcupmatches" (
    "year" integer ,
    "datetime" character varying(50),
    "stage" character varying(50),
    "stadium" character varying(50),
    "city" character varying(50),
    "home_team_name" character varying(50),
    "home_team_goals" integer,
    "away_team_goals" integer,
    "away_team_name" character varying(50),
    "win_conditions" character varying(50),
    "attendance" integer,
    "half_time_home_goals" integer,
    "half_time_away_goals" integer,
    "referee" character varying(36),
    "assistant_1" character varying(36),
    "assistant_2" character varying(36),
    "roundid" integer,
    "matchid" integer,
    "home_team_initials" character varying(3),
    "away_team_initials" character varying(3)
);

DROP TABLE IF EXISTS "worldcupplayers" CASCADE;
CREATE TABLE "public"."worldcupplayers" (
    "roundid" integer,
    "matchid" integer,
    "team_initials" character varying(3),
    "coach_name" character varying(31),
    "line_up" character varying(1),
    "shirt_number" integer,
    "player_name" character varying(35),
    "position" character varying(3),
    "event" character varying(24)
   
   
) 


