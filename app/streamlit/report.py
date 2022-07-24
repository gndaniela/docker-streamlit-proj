#Libraries
import psycopg2
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify
import base64


#Local
import textcontent
import queries as qu
import plots

#Screen size config
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

file_ = open("./images/worldcup.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


def main():
    text = st.sidebar.title("Menu")
    page = st.sidebar.selectbox("Choose a page", ["Homepage", "Data Analysis"]) 
    scol1, scol2, scol3 = st.sidebar.columns(3)
    with scol1:
         st.write(' ')
    with scol2:
          st.sidebar.markdown(f"""<p align="center">
                              <img src="data:image/gif;base64,{data_url}" />
                              </p>""", unsafe_allow_html=True)
    with scol3:
         st.write(' ') 
                 

    if page == "Homepage":
        st.title("Welcome to the World Cups' DB Analysis!")
        st.header("About the database:")
        st.write(textcontent.about_db)
        st.markdown(textcontent.schema_details)
        st.markdown(textcontent.tables_title)
        with st.expander("World Cups 👉"):
             st.write(qu.dfwc)
        with st.expander("World Cup Matches 👉"):
             st.write(qu.dfwm)
        with st.expander("World Cup Players 👉"):
             st.write(qu.dfwp)   

    elif page == "Data Analysis":
        st.title("Data Analysis")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        col1, col2 = st.columns(2)
        with col1:
          st.markdown("#### Which top N national teams have more appearances in a World Cup?:")
          n_value = st.selectbox("Choose the N value:", (5,10,15,20,25,30))
          pie_app = plots.define_plot(qu.dfparticipations.rename(columns={'home_team_name':"Team"}).head(n_value))
          pie_app.pie_sequential("count","Team")
          pie_app.plot()
        with col2:  
          st.markdown("#### Which hosts have the highest average attendace?:")
          st.write("          ")
          st.write("          ")
          st.write("          ")
          st.write("          ")
          plots.bar_att.plot()
        col3, colnew ,col4, =  st.columns([3,0.8,3])
        with col3:
          st.markdown("#### Which national team scored more goals in each Cup?:")
          plots.map_goals.plot()
        with col4:
          st.markdown("#### Are most goals scored in the first or in the second half?")
          yearval = st.slider("Select a period to analyze:", min_value=1930, max_value=2014, value=(1930,2014),step=4)
          pivot_half = plots.dfgoalshalf[plots.dfgoalshalf['year'].between(yearval[0],yearval[1])]\
                      .melt(id_vars=['year'], var_name='Half', value_name='Goals')
          bar_grp = plots.define_plot(pivot_half)
          bar_grp.bar_group('Half','Goals','Half')
          bar_grp.plot()   

        col5, col6 =  st.columns(2)
        with col5:
          st.markdown("#### In which round/group are most goals scored?:")
          st.markdown("*'First round' was the entire groups phase in 1938's WC")
          plots.bar_rounds.plot()
        with col6:
          st.markdown("#### When are most goals scored within match minutes?:")
          st.markdown(" ")
          st.markdown(" ")
          plots.box_mins.plot()
        col9, col10, col11 =  st.columns([3,1,3])           
        col10.markdown("#### All-time scorers")
        nac_team = st.selectbox("Choose a team:", plots.select_list)
        if nac_team == 'All':
             data_scorers = plots.dfscorers_complete.head(5)
        else:
             data_scorers = plots.dfscorers_complete[plots.dfscorers_complete['home_team_name']==nac_team].head(5).reset_index(drop=True)    
        col12, col13, col14, col15, col16 =  st.columns(5)
        col12.metric(data_scorers.iloc[0]['team_initials'], data_scorers.iloc[0]['player_name'], data_scorers.iloc[0]['type'].astype('str'))
        col13.metric(data_scorers.iloc[1]['team_initials'], data_scorers.iloc[1]['player_name'], data_scorers.iloc[1]['type'].astype('str'))
        col14.metric(data_scorers.iloc[2]['team_initials'], data_scorers.iloc[2]['player_name'], data_scorers.iloc[2]['type'].astype('str'))
        col15.metric(data_scorers.iloc[3]['team_initials'], data_scorers.iloc[3]['player_name'], data_scorers.iloc[3]['type'].astype('str'))
        col16.metric(data_scorers.iloc[4]['team_initials'], data_scorers.iloc[4]['player_name'], data_scorers.iloc[4]['type'].astype('str'))  
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        col7, col8 =  st.columns(2)
        with col7:
          st.markdown("#### Which are the dirties N-teams of all time (sum of red and yellow cards)?:")
          n_value2 = st.selectbox("Choose the N value:", (3,4,5,6,7,8,9,10))
          data = (plots.dirt_map.head(n_value2))
          squarify.plot(sizes=data['type'], label=data['team'], alpha=.8)
          plt.axis('off')
          st.pyplot()  
          
        with col8:
          st.markdown("#### Which were the dirtiest 10 matches on the competition?:")
          st.table(plots.dfdirtiest[['year','type','home_team_name',"away_team_name"]].\
                    rename(columns={'year':'Year','home_team_name':'Home Team',"away_team_name":'Away Team','type':'Cards'}).\
                    head(10))
        col17, col18, col19, col20 =  st.columns([0.5,0.1,0.3,0.1])  
        with col17: 
          st.markdown("#### Which national teams won more matches historically?:")
          plots.bar_won.plot()   
        with col19: 
          st.markdown("#### World Cup Champions - summary:")      
          st.markdown("""| Team      | World Cups |
| ----------- | ----------- |
| 	![Brazil](https://api.fifa.com/api/v1/picture/flags-sq-2/bra)   | 5       |
| ![Italy](https://api.fifa.com/api/v1/picture/flags-sq-2/ita)   | 4        |
| ![Germany](https://api.fifa.com/api/v1/picture/flags-sq-2/ger)   | 4        |
| ![Argentina](https://api.fifa.com/api/v1/picture/flags-sq-2/arg)   | 2        |
| ![Uruguay](https://api.fifa.com/api/v1/picture/flags-sq-2/uru)   | 2        |
| ![Engand](https://api.fifa.com/api/v1/picture/flags-sq-2/eng)   | 1       |
| ![France](https://api.fifa.com/api/v1/picture/flags-sq-2/fra)   | 1        |
| ![Spain](https://api.fifa.com/api/v1/picture/flags-sq-2/esp)   | 1        |""")     
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.markdown("""<div style="text-align: right"> <em>ITBA - Cloud Data Engineering | TP1 | Daniela García Nistor</em> </div>""", unsafe_allow_html=True)
         
if __name__ == "__main__":
    main()
