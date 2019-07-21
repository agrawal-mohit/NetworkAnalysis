# cython: language_level=3

import datetime
import time
import json
import random
import traceback
import difflib

from igraph import *
from numba import vectorize

from numba import jitclass          # import the decorator
from numba import int32, float32    # import the types

spec = [
    ('value', int32),               # a simple scalar field
    ('array', float32[:]),          # an array field
]

@jitclass(spec)
class UndirectedNetworkAnalysis:
    def __init__(self):
        self.g = Graph()

    # read data of employees from file
    # expected file ------ id, name, sex, designation, location, department, email
    def add_nodes(self, file="nodes.csv"):
        ret = False
        # noinspection PyBroadException,PyBroadException
        try:
            emp_id = []
            emp_name = []
            emp_sex = []
            emp_designation = []
            emp_dep = []
            emp_loc = []
            emp_email = []

            with open(file, "r") as node_file:
                for line in node_file:
                    x = line.split(",")
                    emp_id.append((x[0]).strip())
                    emp_name.append(x[1].strip())
                    emp_sex.append(x[2].strip())
                    emp_designation.append(x[3].strip())
                    emp_loc.append(x[4].strip())
                    emp_dep.append(x[5].strip())
                    emp_email.append(x[6].strip())

            self.g.add_vertices(emp_email)
            self.g.vs["Empname"] = emp_name
            self.g.vs["Sex"] = emp_sex
            self.g.vs["Designation"] = emp_designation
            self.g.vs["Department"] = emp_dep
            self.g.vs["Location"] = emp_loc
            self.g.vs["Email"] = emp_email
            self.g.vs[
                "Type"] = "Internal"  # Nodes that are input by the company are by default considered as "Internal"
            self.g.vs["display_details"] = False  # Whether details of node or only email ID should be displayed

            ret = True
        except Exception as e:
            print("add players", e)
            ret = False

        finally:
            return ret

    # add edges to the graph
    def add_edges(self, file="edges.csv"):
        ret = False
        # noinspection PyBroadException,PyBroadException
        try:
            ed = []
            dates = []
            sent = {}
            rec = {}
            # Initialize the mappings (to avoid errors for people
            # who have either not received or sent a single mail)
            for vertex in self.g.vs:
                sent[vertex["name"]] = 0
                rec[vertex["name"]] = 0
                # dates[vertex["name"]] = []

            with open(file, "r") as edge_file:
                for line in edge_file:
                    x = line.split(",")
                    for i in range(2):
                        if x[i].strip() not in self.g.vs["name"]:
                            self.g.add_vertex(x[i].strip(), Type="External", Empname="-", Sex="-", Department="-",
                                              Designation="-", Location="-", Email=x[i].strip(), display_details=False)

                            sent[x[i].strip()] = 0  # Initialize the sent mapping for this external email ID
                            rec[x[i].strip()] = 0  # Initialize the rec mapping for this external email ID

                    ed.append((x[0].strip(), x[1].strip()))
                    sent[x[0].strip()] += 1
                    rec[x[1].strip()] += 1

                    # making pair of date and from for counting wt and sent recv
                    # all datetime will be in the for of UNIX timestamps
                    _date = UndirectedNetworkAnalysis.get_unix_from_date(x[2].replace('"', "").replace("\n", ""))
                    # print("date",_date)
                    dates.append((_date, x[0].strip())) # Store the date/time of the interaction along with the sender of the message
                    
            final_edges = []
            wt = {}
            date = {}

            # We add the edges to both, the undirected as well as the directed graph.
            # Directed Graph will be used to obtain Flow Indices
            # Undirected Graph will be used to obtain Key Player (entropy) and other parameters

            # For Directed Graph
           
            # For Undirected Graph
            for i in range(len(ed)):
                flag = 0
                for j in range(len(final_edges)):
                    if final_edges[j][0] == ed[i][0] and final_edges[j][1] == ed[i][1]:
                        flag = 1
                        wt[final_edges[j]] += 1
                        date[final_edges[j]].append(dates[i])

                    elif final_edges[j][0] == ed[i][1] and final_edges[j][1] == ed[i][0]:
                        wt[final_edges[j]] += 1
                        flag = 1
                        date[final_edges[j]].append(dates[i])

                    if flag == 1:
                        break

                if flag != 1:
                    final_edges.append(ed[i])
                    wt[final_edges[final_edges.index(ed[i])]] = 1
                    date[final_edges[final_edges.index(ed[i])]] = [dates[i]]
                    # print(final_edges.index(ed[i]))

            # for edge in final_edges:
            #     self.g.add_edge(edge[0], edge[1], weight=wt[edge], dates=date[edge])
            # #
            wt_final=[None]*len(wt)
            for i,j in wt:
                wt_final[final_edges.index((i,j))]=wt[(i,j)]

            date_final=[None]*len(date)
            for i,j in date:
                date_final[final_edges.index((i,j))]=date[(i,j)]

            self.g.add_edges(final_edges)
            self.g.es["weight"]=wt_final
            self.g.es["dates"]=date_final

           
        except Exception as e:
            print("add_edges failed!", e)
            ret = False
        finally:
            return ret


    # API Function to get Overall Analysis
    def get_result(self, s, l, dep, des, per, start_date, start_time, end_date, end_time):
        try:
            new_graph = self.g


            d=UndirectedNetworkAnalysis.sample(new_graph)
            print(d)
        except Exception as e:
           print("get res",e)



    @staticmethod
    def get_unix_from_date(date_string):

        # list of accepted date-time formats
        # To accept any other date/time format, just add it to this list
        datetime_formats = ["%Y/%m/%d %H:%M:%S %Z", "%b %d %Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"]
        for datetime_format in datetime_formats:
            try:
                return int(time.mktime(datetime.datetime.strptime(date_string, datetime_format).timetuple()))
            except ValueError:
                pass

        raise ValueError(date_string + " is not a recognized date/time")

    @staticmethod
    def get_unix_from_datetime(d):
        # epoch = datetime.datetime(1970, 1, 1)
        # seconds = (d - epoch).total_seconds()
        milliseconds = int(round(d.timestamp() * 1000))

        return int(milliseconds / 1000)


    @staticmethod
    def avg(li):
        x = 0
        for i in li:
            x += len(i)
        return x / len(li)

    
    @staticmethod
    @vectorize(['float32(float32, float32)'], target='cuda')
    def sample(gr):
        eff = []
        num_nodes = len(gr.vs)
        components = UndirectedNetworkAnalysis.avg((gr.clusters()))
        old = (gr.clusters())
        c = len(gr.clusters())
        for v in gr.vs:
            g = deepcopy(gr)
            g.delete_vertices([v.index])
            eff.append(0)
        return eff

if __name__ == '__main__':
    start_date_default = datetime.date(2000, 1, 1)
    end_date_default = datetime.date(2050, 12, 12)
    start_time_default = datetime.time(10, 0, 0)
    end_time_default = datetime.time(16, 0, 0)

    x=UndirectedNetworkAnalysis()
    x.add_nodes()
    x.add_edges()
    #print(x.individual_analysis("ivy.rich@xyz.com",start_date_default,start_time_default,end_date_default,end_time_default))
    res = x.get_result([],[],[],[],100,start_date_default, start_time_default, end_date_default, end_time_default)
    # print(res)