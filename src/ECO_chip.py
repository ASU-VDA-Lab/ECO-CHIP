import numpy as np
from   tqdm import tqdm, trange
import pandas as pd 
import itertools as it 
from   matplotlib import pyplot as plt

#Importing all functions from CO2_func files
from CO2_func import * 
from tech_scaling import *

import argparse
import json
import ast


DEBUG = False #TODO Remove this and its internals
#DEBUG = True #TODO Remove this and its internals
#MAIN = False #TODO This will go into our git repo, remove DEBUG and internals before checkin
MAIN = True #TODO This will go into our git repo, remove DEBUG and internals before checkin


scaling_factors = load_tables()
#print(scaling_factors)

if DEBUG:
    #print(scaling_factors)
    #print(scaling_factors.type)
    print(type(scaling_factors))
    print(scaling_factors['sram'])
    #print(scaling_factors['sram']).loc area
    print(scaling_factors['transistors_per_mm2'])
    print(scaling_factors['gates_per_hr_per_core'])

    print("ccheck")
    print(scaling_factors['sram'].loc[22,'edp'])
    print(scaling_factors['sram'].loc[14,'area'])
    #print(scaling_factors['transistors_per_mm2'].loc[14,0])
    print(scaling_factors['transistors_per_mm2'].loc[14,'Transistors_per_mm2'])
    
    #print(scaling_factors['defect_den'].loc[7,0])
    print(scaling_factors['defect_den'].loc[7,'defect_density'])
#    print(scaling_factors['transistors_per_mm2'].loc[7,0])
    print(scaling_factors['transistors_per_mm2'])
    print(scaling_factors['sram'].loc[22,'edp'])
    
    print("testing design_cost")
    x = design_costs(100,[7,14],scaling_factors)
    x = design_costs(100,[7],scaling_factors)
    print(x)
    
    print("testing recursive_split")
    test = [12,12,12,12,]
    print(np.sum(test))        
    print(np.prod(recursive_split(test)[0]))
   
    print("power chip")
    power_val = power_chip([7],['logic'],scaling_factors,15,365,[0.2,0.667,0.1])
    print(power_val)

    print("beol")
    #print(scaling_factors['beolVfeol'].loc[:,0])
    tech = 14
    print(scaling_factors['beolVfeol'].loc[tech,'beolVfeol'])
    print(scaling_factors['beolVfeol'].loc[14,'beolVfeol'])
    
    print("testing Si_Chip Function")
    #int_C_test, _, _ = Si_chip([65], ["logic"], 65.33, scaling_factors ,True, False)
    int_C_test, y, z = Si_chip([14], ["logic"], 16.04, scaling_factors ,True, False)
    print(int_C_test)
    print(y)
    print(z)


###############################
if MAIN:
    parser = argparse.ArgumentParser(description='Provide a Carbon Foot Print(CFP) estimate ')
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--design',
            default=None,
            help='use existing template for design "--design config/design.js"'
        )
    
    
    args = parser.parse_args()
    
    with open(args.design) as json_file:
        config_json = json.load(json_file)

    with open('config/node_list.txt' , 'r') as file:
        nodes=file.readlines()
    nodes = [ast.literal_eval(node_item) for node_item in nodes]
    nodes = [data for inside_node in nodes for data in inside_node]
    #print("Nodes from node_list.txt file ",nodes)

    print(config_json)
    print(type(config_json))
    print("start") #TODO CCS remove
    design = pd.DataFrame(config_json).T
    print(type(design))
    print(design)
    print("done")   #TODO CCS remove

    power = 15
    powers = design.area.values * power / design.area.values.sum()

    design.insert(loc=2,column='power',value=powers)
    print(design)

    #result = calculate_CO2(design,scaling_factors, [10,14], 'Tiger Lake')
    result = calculate_CO2(design,scaling_factors, nodes, 'Tiger Lake')
    print("Tiger Lake example")
    print(" ---------------------------------------------------------")
    print("Manufacture Carbon in Kgs ")
    print(result[0])
    print(" ---------------------------------------------------------")
    print("Design Carbon in Kgs ")
    print(result[1])
    print(" ---------------------------------------------------------")
    print("Operational Carbon in Kgs ")
    print(result[3])
    print(" ---------------------------------------------------------")
    print("Total Carbon in Kgs ")
    print(result[2])
    print(" ---------------------------------------------------------")


    ##Working JSON
    #with open('config/test.json','r') as file:
    #    data = json.load(file)
    #print(data)
    #design = pd.DataFrame(data).T
    #print(design)

###############################

if DEBUG:
    ##
    techs = [7,10]
    packaging_techs =["passive","active","RDL","EMIB"]
    #combinations=list(it.product(techs, repeat=len(design.index)))
    combinations=list(it.product(techs, repeat=3))
    print("combinations = ",combinations)
    print("packaging_techs ",packaging_techs)
    
    carbon = np.zeros((len(combinations), len(packaging_techs)*2))
    print("carbon = ",len(carbon))
    print("carbon = ",carbon.shape)
    
    #for n,comb in enumerate(combinations):
    #    print(comb)
    #    for i,package in enumerate(packaging_techs):
    #        print("i , package ",i,package)
    #    carbon[n, 2*i], carbon[n, 2*i+1] = Interposer(areas=design.area.values, 
    #                                                  techs=comb, 
    #                                                  types = design.type.values, 
    #                                                  scaling_factors = scaling_factors,
    #                                                  interposer_type=package)

    print("New Interposer")
    interposer_techs = [7, 14, 22, 28, 65]
    active_carbon = np.zeros((len(interposer_techs), 2))
    areas = np.array(design['area']).astype(np.float64)
    techs = np.array([7]*len(areas))
    types = design['type']
    for n, interposer_tech in enumerate(interposer_techs):
        active_carbon[n,0], active_carbon[n,1], _ = Interposer(areas=areas,
                                                 techs=techs,
                                                 types = types,
                                                 scaling_factors=scaling_factors,
                                                 interposer_type='active',
                                                 always_chiplets=True,
                                                 interposer_node = interposer_tech
                                                )
    active_carbon = pd.DataFrame(data=active_carbon, index=interposer_techs, columns=['package', 'router'])
    print("ACTIVE")
    print(active_carbon)


    print("done with Interpose function")
    print(carbon)
    ##
    
    print("testing package_CO2")
    #package_CO2(design, scaling_factors, [7, 10, 14])
    
    print("testing calculate_co2")
    result = calculate_CO2(design,scaling_factors, [7,10,14], 'Tiger Lake')
    print(result[0])
    print(result[1])
    print(result[2])
