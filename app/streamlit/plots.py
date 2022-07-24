#Libraries
import psycopg2
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
#import plotly.graph_objs as gobj
#from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import squarify


#Local
import textcontent
import queries as qu

#Class for plots

class define_plot:
    def __init__(self,data):
        self.data = data
        self.fig=None
        self.update_layout=None

    def bar(self,x,y,color,orientation,hover_name,custom_data):
        self.fig=px.bar(self.data,x=x,y=y,orientation=orientation,color=color,color_discrete_sequence=px.colors.sequential.Viridis,
                         hover_name=hover_name, custom_data=[self.data[custom_data]])
        self.fig.update_traces(hovertemplate='Value:%{customdata[0]}')
        self.fig.update_layout(yaxis={'categoryorder':'array', 'categoryarray':self.data.index})
        self.fig.update_layout(yaxis_title=None,xaxis_title=None)
        #self.fig.update_traces(marker=dict(colorscale=px.colors.discrete.Viridis))

    def bar_cont(self,x,y,color,orientation,hover_name,custom_data):
        self.fig=px.bar(self.data,x=x,y=y,orientation=orientation,color=color,color_continuous_scale=px.colors.sequential.Viridis,
                         hover_name=hover_name, custom_data=[self.data[custom_data]])
        self.fig.update_traces(hovertemplate='Value:%{customdata[0]}')
        self.fig.update_layout(yaxis={'categoryorder':'array', 'categoryarray':self.data.index})
        self.fig.update_layout(yaxis_title=None,xaxis_title=None)
        #self.fig.update_traces(marker=dict(colorscale=px.colors.discrete.Viridis))    

    def pie_sequential(self,x,y):
        self.fig = px.pie(self.data,values=x,names=y,color_discrete_sequence=px.colors.sequential.Viridis,hole=.5)
        self.fig.update_traces(textposition='inside')
        self.fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    def map(self,locations,color,hover_name,animation_frame):
        self.fig = px.choropleth(self.data, locations=locations, color=color, 
                hover_name=hover_name,animation_frame=animation_frame,locationmode='country names', 
                range_color=[0,25],color_continuous_scale=px.colors.sequential.Viridis)

    def boxplot(self,x,y):
        self.fig = px.box(self.data, x=x, y=y, notched=True,color_discrete_sequence=px.colors.sequential.Viridis)
        self.fig.update_layout(yaxis_title=None,xaxis_title=None)
        self.fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':self.data.index})

    def bar_group(self,x,y,color):
        self.fig = px.bar(self.data, x=x, y=y, color=color, barmode="group",color_discrete_map={'First Half':'#5ec962','Second Half':'#3b528b'})
        self.fig.update_layout(yaxis_title=None,xaxis_title=None)

    def treemap(self,x,y):
         self.fig = squarify.plot(sizes=self.data[x], label=self.data[y], alpha=.8)
         self.fig = plt.axis('off') 

    def bar_rounds(self,x,y,text,color):
        self.fig =px.bar(self.data, x=x, y=y,text=text,color=color,color_continuous_scale=px.colors.sequential.Viridis) 
        self.fig.update_layout(yaxis_title=None,xaxis_title=None,showlegend=False,xaxis={'categoryorder':'array', 'categoryarray':[
        'Group A',
        'Group B',
        'Group C',
        'Group D',
        'Group E',
        'Group F',
        'Group G',
        'Group H',
        'First round',
        'Round of 16',
        'Quarter-finals',
        'Semi-finals',
        'Third place',
        'Final'
        ]}) 

          
    def plot(self):
        st.write(self.fig)


#Top 10 - Most appearances in a WC
#pie_app = define_plot(qu.dfparticipations.rename(columns={'home_team_name':"Team"}).head(10))
#pie_app.pie_sequential("count","Team")


#Top 10 - More won matches by year
data_won = qu.dftotal_results[['team_name','team_initials','result','count']]
data_won = data_won[qu.dftotal_results['result']=='Won'].sort_values('count',ascending=False).reset_index(drop=True).head(10)
bar_won = define_plot(data_won)
bar_won.bar_cont('count','team_name','count','h','team_name','count')

#Goals interactive map
map_goals = define_plot(qu.dftotgoals)
map_goals.map('team_name','goals','team_name','year')


#Host with more attendance
total_att_host = qu.dfwcall.groupby('country', as_index=False)['attendance'].mean().sort_values('attendance',ascending=False).reset_index(drop=True)
bar_att = define_plot(total_att_host)
bar_att.bar('country','attendance','country','v','country','attendance')

#Dirtiest matches

dfevents = qu.dfwpall[['matchid','team_initials','player_name','line_up','event']].dropna(subset=['event'])
dfevents[['event1','event2','event3','event4','event5','event6']] = dfevents['event'].str.split('\'', expand=True)
dfevents.drop('event',axis=1,inplace=True)
dfevents = dfevents.melt(id_vars=['matchid','player_name','team_initials'], var_name='event', value_name='event_type')
dfevents = dfevents[dfevents['event'].str.contains("event")].dropna(subset=['event_type']).reset_index()
dfevents['type'] = dfevents['event_type'].str.strip().str[0]
dfevents['event_minute'] = dfevents['event_type'].str.strip().str[1:3]
dfevents.drop(['event','event_type','index'],axis=1,inplace=True)
dfevents = dfevents.dropna(subset=['type']).reset_index()

dfdirty = dfevents[(dfevents['type'] == 'R') | (dfevents['type'] == 'Y') ].groupby('matchid',as_index=False)['type'].count()\
          .sort_values('type',ascending=False) #.head(10)
dfdirtiest = pd.merge(dfdirty, qu.dfwmall[['matchid','year','home_team_name',"away_team_name"]]) 

dirt_map = pd.concat([dfdirtiest[['type','year','home_team_name']].rename(columns={'home_team_name':'team'}),dfdirtiest[['type','year','away_team_name']].\
           rename(columns={'away_team_name':'team'})])
dirt_map = dirt_map.groupby('team',as_index=False)['type'].sum().sort_values('type',ascending=False).reset_index(drop=True)

#Country name and initials

country_names = qu.dfwmall[['home_team_name',"home_team_initials"]].drop_duplicates().rename(columns={'home_team_initials':'team_initials'}).sort_values('home_team_name')

# Scorers ordered by # goals
dfscorers = dfevents[dfevents['type'] == 'G'].groupby(['player_name','team_initials'],as_index=False)['type'].\
            count().sort_values('type',ascending=False).reset_index(drop=True)

dfscorers['type'] = dfscorers['type'].astype('int') 

dfscorers_complete = pd.merge(dfscorers,country_names).sort_values('type',ascending=False).reset_index(drop=True)

select_list = ['All']
select_list.extend(country_names['home_team_name'])


# Goals per half
dfgoalshalf = qu.dfgoalshalf[['year','total_first_half','second_half_goals']].\
                rename(columns={'total_first_half':"First Half",'second_half_goals':'Second Half'})


#Goals - Minutes detail

dfminutes = pd.merge(dfevents[dfevents['type'] == 'G'],qu.dfwmall[['year','matchid']])
dfminutes['event_minute'] = dfminutes['event_minute'].astype('int')
box_mins = define_plot(dfminutes.sort_values('year',ascending=True).reset_index(drop=True))
box_mins.boxplot('year','event_minute')

# Goals per round/group

#Correct groups
qu.dfwmall["stage"] = qu.dfwmall["stage"].replace("Group 1", "Group A")
qu.dfwmall["stage"] = qu.dfwmall["stage"].replace("Group 2", "Group B")
qu.dfwmall["stage"] = qu.dfwmall["stage"].replace("Group 3", "Group C")
qu.dfwmall["stage"] = qu.dfwmall["stage"].replace("Group 4", "Group D")
qu.dfwmall["stage"] = qu.dfwmall["stage"].replace("Group 5", "Group E")
qu.dfwmall["stage"] = qu.dfwmall["stage"].replace("Group 6", "Group F")
qu.dfwmall["stage"] = qu.dfwmall["stage"].replace("Play-off for third place", "Third place")
qu.dfwmall["stage"] = qu.dfwmall["stage"].replace("Match for third place", "Third place")
qu.dfwmall["stage"] = qu.dfwmall["stage"].replace("Preliminary round", "Round of 16")

qu.dfwmall['total_goals'] = qu.dfwmall['home_team_goals'] + qu.dfwmall['away_team_goals']

qu.dfwmall['home_result'] = np.where(qu.dfwmall['home_team_goals'] > qu.dfwmall['away_team_goals'], "Won",
                            np.where(qu.dfwmall['away_team_goals'] > qu.dfwmall['home_team_goals'], "Lost","Draw"))

qu.dfwmall['away_result'] = np.where(qu.dfwmall['home_team_goals'] > qu.dfwmall['away_team_goals'], "Lost",
                            np.where(qu.dfwmall['away_team_goals'] > qu.dfwmall['home_team_goals'], "Won","Draw"))

qu.dfwmall['stage']  = qu.dfwmall['stage'] .astype('category')  

qu.dfwmall['stage'].cat.reorder_categories([
 'Group A',
 'Group B',
 'Group C',
 'Group D',
 'Group E',
 'Group F',
 'Group G',
 'Group H',
 'First round',
 'Round of 16',
 'Quarter-finals',
 'Semi-finals',
  'Third place',
  'Final'
 ], ordered=True, inplace=True)

#Cleaned data
dfrounds = qu.dfwmall.groupby("stage", as_index=False).agg({'total_goals':'sum',"home_team_name":'count'})
dfrounds['average_goals'] = round(dfrounds['total_goals']/dfrounds['home_team_name'],2)
dfrounds 


bar_rounds = define_plot(dfrounds)
bar_rounds.bar_rounds('stage','average_goals','average_goals','average_goals')
