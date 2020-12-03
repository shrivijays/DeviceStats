import mysql.connector
import pandas as pd
#import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Sets default chart renderer as the default browser
#pio.renderers.default = "browser"

class mydb_connect():
    def __init__(self):
        mydb = mysql.connector.connect(host = 'localhost', user = "root", password = "11GITIndia**", database = 'devicelogdb')
        print ("db connected")

class get_data():
    def __init__ (self, start_time, end_time, machine_id, job_number):
# set default date inputs. CHnage this as user entered input
        self.start_time = start_time
        self.end_time = end_time
        self.machine_id = machine_id
        self.job_number =job_number

# Setup MySQL connection
    def get_data(self):
        start_time = self.start_time + "00:00:00"
        end_time = self.end_time + "00:00:00"
        machine_id = self.machine_id
        job_number = self.job_number

        #Create SQL query to run
#        query = "Select timestamp, field1, field2, field3, field4 from machine_event_data"
#        " where timestamp between timestamp(%s) and timestamp(%s) and machine_id in (%s)"
#        " and job_number in (%s)" % (start_time, end_time, machine_id, job_number)


        query = "Select timestamp, field1, field2, field3, field4 from machine_event_data"
        " where timestamp between %s and %s" %(start_time, end_time)


        print ("Does db connect")
        # put data in pandas frame
#        mydb = mydb_connect()
        mydb = mysql.connector.connect(host = 'localhost', user = "root", password = "11GITIndia**", database = 'devicelogdb')
        frame = pd.read_sql(query, mydb)
        print(frame)

        # Close the db connection
        mydb.close()
        return frame

# Class to plot the scattered chart with pandas frame as input and chart as output
class Scattered_Chart_Four_Axis():
    def __init__(self, data):
        self.data = data

    def plot_scattered_chart_four_axis(self):
        frame = self.data

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": False}]])

        # Add traces (Create additional charts with different values on same axis)
        fig.add_trace(
            go.Scatter(x=frame['timestamp'], y=(frame['field1'] + 6), name="Emergency",
            mode = 'lines+markers', marker = dict(color = 'rgb(255,0,0)', size =20)),
            secondary_y=False)

        fig.add_trace(
            go.Scatter(x=frame['timestamp'], y=(frame['field2']+4), name="Power",
            mode = 'lines+markers', marker = dict(color = 'rgb(0,0,255)', size =20)),
            secondary_y=False)

        fig.add_trace(
            go.Scatter(x=frame['timestamp'], y=(frame['field3']+2), name="Loading",
            mode = 'lines+markers', marker = dict(color = 'rgb(0,255,0)', size =20)),
            secondary_y=False)

        fig.add_trace(
            go.Scatter(x=frame['timestamp'], y=frame['field4'], name="Processing",
            mode = 'lines+markers', marker = dict(color = 'rgb(0,0,0)', size =20)),
            secondary_y=False)

        # Update the chart layout to modify the layout. In this case hide the yaxis.
        fig.update_layout(yaxis = dict(showticklabels = False))
        return fig

# fig.show()


# call get data class and rturn data in frame
frame = get_data("1989-10-10 00:00:00", "2021-10-10 00:00:00","AKL3483748","JB1234").get_data()
fig = Scattered_Chart_Four_Axis(frame).plot_scattered_chart_four_axis()
#fig.show()
# Create a html page in localhost
pio.write_html(fig, file='index.html', auto_open=True)
