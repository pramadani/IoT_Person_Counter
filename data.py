import time
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go

last_temp_update = 0
last_person_update = 0
temperature_data = []
person_data = []
fig_temp = go.Figure()  
fig_person = go.Figure()
  
def update_temp_df(interval, temperature):
    global last_temp_update
    global temperature_data
    global fig_temp

    current_time = time.time()
    
    if current_time - last_temp_update >= interval:
        current_time_str = datetime.now().strftime("%H:%M:%S")
        temperature = float(temperature)
        
        temperature_data.append((current_time_str, temperature))
        
        df = pd.DataFrame(temperature_data, columns=["Time", "Temperature"])
        df.set_index("Time", inplace=True)
        
        df_last_10 = df.tail(10)
                
        min_temp = df_last_10["Temperature"].min()
        max_temp = df_last_10["Temperature"].max()
        y_min = min_temp - 1
        y_max = max_temp + 1
        
        fig_temp.data = []
        fig_temp.add_trace(go.Scatter(x=df_last_10.index, y=df_last_10["Temperature"], mode='lines+markers', name='Temperature'))
        fig_temp.update_layout(
            title='Linimasa Temperatur',
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            yaxis=dict(range=[y_min, y_max]),
            height=300
        )
        
        last_temp_update = current_time
        
    return fig_temp

def update_count_df(interval, person_count):
    global last_person_update
    global person_data
    global fig_person
    
    current_time = time.time()
    
    if current_time - last_person_update >= interval:
        current_time_str = datetime.now().strftime("%H:%M:%S")
        person_count = int(person_count)
        
        person_data.append((current_time_str, person_count))
        
        df = pd.DataFrame(person_data, columns=["Time", "Person Count"])
        df.set_index("Time", inplace=True)
        
        df_last_10 = df.tail(10)
                
        min_person = df_last_10["Person Count"].min()
        max_person = df_last_10["Person Count"].max()
        y_min = min_person - 1
        y_max = max_person + 1
        
        fig_person.data = []
        fig_person.add_trace(go.Scatter(x=df_last_10.index, y=df_last_10["Person Count"], mode='lines+markers', name='Person Count'))
        fig_person.update_layout(
            title='Linimasa Person',
            xaxis_title='Time',
            yaxis_title='Person Count',
            yaxis=dict(range=[y_min, y_max]),
            height=300
        )
        
        last_person_update = current_time
        
    return fig_person