'''
Created on 18 Dec 2017

@author: Gary
'''

#import urllib2

# for Python3
from urllib.request import urlopen
import json

import time
import datetime
import threading

import random

# for plotting
import plotly
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

PLOTLY_USERNAME = "hin88188"
PLOTLY_API_KEY = "u9IGnJ6pG6turnBBDlFu"
stream_ids = ['z9dznl0v17','b0xk8acqiz','rloieh2f0y','0qjuathf8j','tzykodmze5','8trsk95zq1',
              '1x6mw67ly8','4w7pfr1y9d','r615jrbvre','haylsh3mt6','t01giiv19i','92dydtkis4']

WU_API_KEY = "3e808ecf31b77d08"
WU_API_URL = "http://api.wunderground.com/api/" + WU_API_KEY + "/"

pws_location = [WU_API_URL + 'conditions/hourly/q/CA/Hsin-chu.json',
                WU_API_URL + 'forecast10day/q/CA/Hsin-chu.json',
                WU_API_URL + 'conditions/hourly/q/CA/Taipei.json',
                WU_API_URL + 'forecast10day/q/CA/Taipei.json',
                WU_API_URL + 'conditions/hourly/q/CA/Taichung.json',
                WU_API_URL + 'forecast10day/q/CA/Taichung.json',
                WU_API_URL + 'conditions/hourly/q/CA/Kao-hsiung.json',
                WU_API_URL + 'forecast10day/q/CA/Kao-hsiung.json']

# temp_cedarrapid = []
# temp_sanfrancisco = []
# high_temp_list = []
# low_temp_list = []
# cur_temp_list = []
# date = []

#def display(pws_location):
#    print("[%s] PWS Location" % (time.ctime(), pws_location, temp_c)) 
#    
#    # print historical record
#    day_id = 0;
#    for day_id in range(0,9):
#        print (date[day_id], "\t", high_temp[day_id], "\t", low_temp[day_id], "\t\n")
    

def queryPWS(pws_url, high_stream, low_stream):    
    print("------------------")
#     print("Querying pws in %s" % pws_url)
    json_str = urlopen(pws_url).read()
    
#     print(json_str)
    parsed_json = json.loads(json_str);
    pws_location = parsed_json['forecast']['simpleforecast']['forecastday'][0]['date']['tz_long']
    print (pws_location, "\t\t\t\thigh\tlow\n")
    for day_id in range(0,10):
        year = parsed_json['forecast']['simpleforecast']['forecastday'][day_id]['date']['year']
        month = parsed_json['forecast']['simpleforecast']['forecastday'][day_id]['date']['month']
        day = parsed_json['forecast']['simpleforecast']['forecastday'][day_id]['date']['day']
        date = parsed_json['forecast']['simpleforecast']['forecastday'][day_id]['date']['pretty']
        high_temp = parsed_json['forecast']['simpleforecast']['forecastday'][day_id]['high']['celsius']
        low_temp = parsed_json['forecast']['simpleforecast']['forecastday'][day_id]['low']['celsius']
        # print (date, "\t", high_temp, "\t", low_temp, "\t\n")
        print("%s \t %s \t %s" % (date, high_temp, low_temp))  
        #plot_init
        # Current time on x-axis, random numbers on y-axis
        x = str(year)+"/"+str(month)+"/"+str(day)
        y = high_temp

        # Send data to your plot_init
        high_stream.write(dict(x=x, y=y, text=(str(y)+"°"), textposition='top'))
        
        x = str(year)+"/"+str(month)+"/"+str(day)
        y = low_temp

        low_stream.write(dict(x=x, y=y, text=(str(y)+"°"), textposition='bottom'))
        #time.sleep(0.1)
    print("------------------")
    #display(high_temp_list,low_temp_list)

def queryPWS2(pws_url, high_stream):    
    print("------------------")
#     print("Querying pws in %s" % pws_url)
    json_str = urlopen(pws_url).read()
    
#     print(json_str)
    
    parsed_json = json.loads(json_str);
    pws_location = parsed_json['current_observation']['local_tz_long']
    print (pws_location, "\n")
    for hour_id in range(0,24):
        year = parsed_json['hourly_forecast'][hour_id]['FCTTIME']['year']
        month = parsed_json['hourly_forecast'][hour_id]['FCTTIME']['mon']
        day = parsed_json['hourly_forecast'][hour_id]['FCTTIME']['mday']
        hour = parsed_json['hourly_forecast'][hour_id]['FCTTIME']['hour']
        date = parsed_json['hourly_forecast'][hour_id]['FCTTIME']['pretty']
        temp = parsed_json['hourly_forecast'][hour_id]['temp']['metric']
        # print (date, "\t", high_temp, "\t", low_temp, "\t\n")
        print("%s \t %s" % (date, temp)) 
        #plot_init
        # Current time on x-axis, random numbers on y-axis
        x = str(hour)+":00"
        y = temp
    
        # Send data to your plot_init
        high_stream.write(dict(x=x, y=y, text=(str(y)+"°"), textposition='top'))
        #time.sleep(0.1)
    print("------------------")

def initPlot(stream_id1, stream_id2, graph_title, max_points=8000):
    print("Plotly Version=" + plotly.__version__)
    print("Setting plotly credentials...")
    tls.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
    #stream_ids = tls.get_credentials_file()['stream_ids']
        
    ## 1. SETUP STREAM_ID OBJECT
    # Make instance of stream id object 
    stream_1 = go.Stream(
        token=stream_id1,  # link stream id to 'token' key
        #maxpoints=max_points      # keep a max of 80 pts on screen
    )
    
    stream_2 = go.Stream(
        token=stream_id2,  # link stream id to 'token' key
        #maxpoints=max_points      # keep a max of 80 pts on screen
    )
    
    # Initialize trace of streaming plot_init by embedding the unique stream_id
    trace1 = go.Scatter(
        x=[],
        y=[],
        name='高溫',
        mode='lines+markers+text',
        line=dict(
            shape='spline',
            color='rgb(255, 128, 0)'
        ),
        stream=stream_1         # (!) embed stream id, 1 per trace
    )
    
    trace2 = go.Scatter(
        x=[],
        y=[],
        name='低溫',
        mode='lines+markers+text',
        line=dict(
            shape='spline',
            color='rgb(102, 178, 255)'
        ),
        stream=stream_2         # (!) embed stream id, 1 per trace
    )
    
    data = go.Data([trace1, trace2])
    
    # Add title to layout object
    layout = go.Layout(
        title=graph_title, 
        xaxis=dict(
            title='日期 (年/月/日)', 
            showgrid=False,
            showline=True,
            linewidth=2,
            tickwidth=2
        ),
        yaxis=dict(
            title='溫度 (°C)', 
            showgrid=True,
            showline=False,
        )
    )
    
    # Make a figure object
    fig = go.Figure(data=data, layout=layout)
    
    # Send fig to Plotly, initialize streaming plot_init, open new tab
    py.plot(fig, filename=graph_title)

def initPlot2(stream_id, graph_title, max_points=8000):
    print("Plotly Version=" + plotly.__version__)
    print("Setting plotly credentials...")
    tls.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
    #stream_ids = tls.get_credentials_file()['stream_ids']
        
    ## 1. SETUP STREAM_ID OBJECT
    # Make instance of stream id object 
    stream_1 = go.Stream(
        token=stream_id,  # link stream id to 'token' key
        #maxpoints=max_points      # keep a max of 80 pts on screen
    )

    # Initialize trace of streaming plot_init by embedding the unique stream_id
    trace1 = go.Scatter(
        x=[],
        y=[],
        name='溫度',
        mode='lines+markers+text',
        textposition='top',
        line=dict(
            shape='spline',
            color='rgb(255, 128, 0)'
        ),
        stream=stream_1         # (!) embed stream id, 1 per trace
    )
    
    data = go.Data([trace1])
    
    # Add title to layout object
    layout = go.Layout(
        title=graph_title, 
        xaxis=dict(
            title='時間 (小時)', 
            showgrid=False,
            showline=True,
            linewidth=2,
            tickwidth=2
        ),
        yaxis=dict(
            title='溫度 (°C)', 
            showgrid=True,
            showline=False,
        )
    )

    # Make a figure object
    fig = go.Figure(data=data, layout=layout)
    
    # Send fig to Plotly, initialize streaming plot_init, open new tab
    py.plot(fig, filename=graph_title)
        
def getGraphStream(stream_id):
    ## 2. Setup Stream Link Object
    # We will provide the stream link object the same token that's associated with the trace we wish to stream to
    graph_stream = py.Stream(stream_id)
    
    # We then open a connection
    graph_stream.open()
    
    return graph_stream

def plot_test(graph_stream):
            # Plot test
    i = 0    # a counter
    k = 5    # some shape parameter
    while True:
    
        # Current time on x-axis, random numbers on y-axis
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        y = (np.cos(k*i/50.)*np.cos(i/50.)+np.random.randn(1))[0]
    
        # Send data to your plot_init
        graph_stream.write(dict(x=x, y=y))
    
        #     Write numbers to stream to append current data on plot_init,
        #     write lists to overwrite existing data on plot_init
    
        time.sleep(1)  # plot_init a point every second   
         
    # Close the stream when done plotting
    graph_stream.close()

if __name__ == '__main__':
    print("WU API KEY = %s" % WU_API_KEY)
    print("WU API PREFIX = %s" % WU_API_URL)
 
     
    #print("pws location %s" % pws_location[0])
     
    # Initialize plot and send the figure to Plot.ly server
    initPlot2(stream_ids[0], "新竹市未來 24 小時預報")
    initPlot(stream_ids[1], stream_ids[2], "新竹市未來 10 天預報")
    initPlot2(stream_ids[3], "台北市未來 24 小時預報")
    initPlot(stream_ids[4], stream_ids[5], "台北市未來 10 天預報")
    initPlot2(stream_ids[6], "台中市未來 24 小時預報")
    initPlot(stream_ids[7], stream_ids[8], "台中市未來 10 天預報")
    initPlot2(stream_ids[9], "高雄市未來 24 小時預報")
    initPlot(stream_ids[10], stream_ids[11], "高雄市未來 10 天預報")
    
    graph_stream_1 = getGraphStream(stream_ids[0])
    graph_stream_2 = getGraphStream(stream_ids[1])
    graph_stream_3 = getGraphStream(stream_ids[2])
    graph_stream_4 = getGraphStream(stream_ids[3])
    graph_stream_5 = getGraphStream(stream_ids[4])
    graph_stream_6 = getGraphStream(stream_ids[5])
    graph_stream_7 = getGraphStream(stream_ids[6])
    graph_stream_8 = getGraphStream(stream_ids[7])
    graph_stream_9 = getGraphStream(stream_ids[8])
    graph_stream_10 = getGraphStream(stream_ids[9])
    graph_stream_11 = getGraphStream(stream_ids[10])
    graph_stream_12 = getGraphStream(stream_ids[11])
    
    queryPWS2(pws_location[0], graph_stream_1)
    queryPWS(pws_location[1], graph_stream_2, graph_stream_3)
    queryPWS2(pws_location[2], graph_stream_4)
    queryPWS(pws_location[3], graph_stream_5, graph_stream_6)
    queryPWS2(pws_location[4], graph_stream_7)
    queryPWS(pws_location[5], graph_stream_8, graph_stream_9)
    queryPWS2(pws_location[6], graph_stream_10)
    queryPWS(pws_location[7], graph_stream_11, graph_stream_12)
