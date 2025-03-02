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

debug = False


scaling_factors = load_tables()
#print(scaling_factors)


parser = argparse.ArgumentParser(description='Provide a Carbon Foot Print(CFP) estimate ')
parser = argparse.ArgumentParser()
parser.add_argument(
        '--design_dir',
        default=None,
        help='use existing template for design_dir "--design_dir config/example/architecture.json"'
        )
    
args = parser.parse_args()
design_dir = args.design_dir
    
architecture_file = design_dir+'architecture.json'
node_list_file = design_dir+'node_list.txt'
designC_file = design_dir+'designC.json'
operationalC_file = design_dir+'operationalC.json'
packageC_file = design_dir+'packageC.json'
print(" ---------------------------------------------------------")
print("Using below files for CFP estimations : \n")
print(architecture_file)
print(node_list_file)
print(designC_file)
print(operationalC_file)
print(packageC_file)
print(" ---------------------------------------------------------")


with open(architecture_file,'r') as json_file:
    config_json = json.load(json_file)

with open(node_list_file , 'r') as file:
    nodes=file.readlines()
nodes = [ast.literal_eval(node_item) for node_item in nodes]
nodes = [data for inside_node in nodes for data in inside_node]
#print("Nodes from node_list.txt file ",nodes) if debug else None

#print(config_json)
#print(type(config_json))
#print("start") #TODO CCS remove
design = pd.DataFrame(config_json).T
#print(type(design))
#print(design) if debug else None
#print("done")   #TODO CCS remove
package_type = design.loc['pkg_type']
package_type = package_type[0]
    
design = design.drop(index='pkg_type')
#print(design)

#power = 450
#powers = design.area.values * power / design.area.values.sum()
#design.insert(loc=2,column='power',value=powers)
#print(design)

with open(designC_file, 'r') as f:
    designC_values = json.load(f)
power = float(designC_values['power'])
powers = design.area.values * power / design.area.values.sum()
num_iter = designC_values['num_iter']
num_prt_mfg = designC_values['num_prt_mfg']
transistors_per_gate = designC_values['Transistors_per_gate']
power_per_core = designC_values['Power_per_core']
carbon_per_kWh = designC_values['Carbon_per_kWh']

design.insert(loc=2,column='power',value=powers)
#print(design)
print(" ")

with open(operationalC_file,'r') as f:
    operationalC_values = json.load(f)
lifetime = operationalC_values['lifetime']
    
    
with open(packageC_file,'r') as f:
    packageC_values = json.load(f)
interposer_node = packageC_values['interposer_node']
rdl_layer = packageC_values['rdl_layers']
emib_layers = packageC_values['emib_layers']
emib_pitch = packageC_values['emib_pitch']
tsv_pitch = packageC_values['tsv_pitch']
tsv_size = packageC_values['tsv_size']
numBEOL = packageC_values['num_beol']

    
#result = calculate_CO2(design,scaling_factors, nodes, 'Tiger Lake')
#C result = calculate_CO2(design,scaling_factors, nodes, 'Tiger Lake',
result = calculate_CO2(design,scaling_factors, 'Tiger Lake',
                       num_iter,package_type=package_type ,Ns=num_prt_mfg,lifetime=lifetime,
                       carbon_per_kWh=carbon_per_kWh,transistors_per_gate=transistors_per_gate,
                       power_per_core=power_per_core,interposer_node = interposer_node, rdl_layer=rdl_layer, emib_layers=emib_layers,
                       emib_pitch=emib_pitch, tsv_pitch=tsv_pitch, tsv_size=tsv_size, num_beol=numBEOL)
print("'"+design_dir+"' Example testcase")
print(" ---------------------------------------------------------")
print("Manufacture Carbon in Kgs ")
print(result[0]/1000) #Converting to Kgs
print(" ---------------------------------------------------------")
print("Design Carbon in Kgs ")
print(result[1]/1000) #Converting to Kgs
print(" ---------------------------------------------------------")
print("Operational Carbon in Kgs ")
print(result[3]/1000) #Converting to Kgs
print(" ---------------------------------------------------------")
print("Total Carbon in Kgs ")
print(result[2]/1000) #Converting to Kgs
print(" ---------------------------------------------------------")

###############################

