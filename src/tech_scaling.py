import pandas as pd
import json

OLD=False
#OLD=True
#NEW=False
NEW=True

tech_indices = [  7,  10,  14,  22,  28]#,  32,  45]
def load_tables():

    if OLD:
        print("OLD")
        LOGIC_scaling_table =   {
        "area":       [ 1, 1.949555068, 3.709574145, 7.325456759, 8.453656378],  #, 8.522856474,  17.04571295],
        #"delay":      [ 1, 1.075268817, 1.132502831, 1.169590643, 1.264222503],  #, 1.321003963,  1.529051988],
        "delay":      [ 1, 1.25268817, 1.562502831,  1.959590643,  2.464222503],
        "energy":     [ 1, 1.36425648,  1.727115717, 2.72479564,  3.367003367],  #, 4,            5.714285714],
        "edp":        [ 1, 1.333333333, 2,           3.164556962, 4.166666667],  #, 5.154639175,  8.474576271],
        "power":      [ 1, 1.237623762, 1.524390244, 2.283105023, 2.666666667],  #, 3.003003003,  3.717472119],
        "throughput": [ 1, 0.925925926, 0.883392226, 0.851788756, 0.788643533],  #, 0.756429652,  0.650618087]
        }
        logic_scaling = pd.DataFrame(data=LOGIC_scaling_table, index=tech_indices) 
    
    
    if OLD:
        print("OLD")
        analog_scaling_table =   {
        "area":       [ 1,  1,  1,  1.974743319,  2.278875162],
        #"delay":      [ 1, 1.075268817, 1.132502831, 1.169590643, 1.264222503],
        "delay":      [ 1, 1.25268817, 1.562502831,  1.959590643,  2.464222503],
        "energy":     [ 1,  1,  1,  1.577656676,  1.949494949],
        "edp":        [ 1, 1.075268817, 1.132502831, 1.845212486, 2.464595385],
        "power":      [ 1,  1,  1,  1.497716895,  1.749333333],
        "throughput": [ 1, 0.925925926, 0.883392226, 0.851788756, 0.788643533]
        }
        analog_scaling = pd.DataFrame(data=analog_scaling_table, index=tech_indices)    
    
    if OLD:
        print("OLD")
        SRAM_scaling_table =   {
        "area":       [ 1,  1,  1.902779873,  3.757501843,  4.336197791],
        #"delay":      [ 1, 1.075268817, 1.132502831, 1.169590643, 1.264222503],
        "delay":      [ 1, 1.25268817, 1.562502831,  1.959590643,  2.464222503],
        "energy":     [ 1,  1,  1.26597582,  1.997275204,  2.468013468],
        "edp":        [ 1,  1.075268817,  1.433721201,  2.335994391,  3.120118164],
        "power":      [ 1,  1,  1.231707317,  1.844748858,  2.154666667],
        "throughput": [ 1, 0.925925926, 0.883392226, 0.851788756, 0.788643533]
        }
        # TBD handle 65nm values for all elements
    #     passive_pakaging_scaling_table =   {
    #     "area":       [ 1,  1,  1, 1, 1, 1],
    #     "delay":      [ 1, 1.25268817, 1.562502831,  1.959590643,  2.464222503, np.float('inf')],
    #     "energy":     [ 1,  1,  1.26597582,  1.997275204,  2.468013468, np.float('inf')],
    #     "edp":        [ 1,  1.075268817,  1.433721201,  2.335994391,  3.120118164, np.float('inf')],
    #     "power":      [ 1,  1,  1.231707317,  1.844748858,  2.154666667, np.float('inf')],
    #     "throughput": [ 1, 0.925925926, 0.883392226, 0.851788756, 0.788643533, np.float('inf')]
    #     }
        
        tech_indices_package = tech_indices + [65]
        #TBD 65 nm defect density and cpa
        sram_scaling = pd.DataFrame(data=SRAM_scaling_table, index=tech_indices)
    
    if OLD:
        print("OLD")
        defect_density = pd.DataFrame([0.2, 0.11, 0.09, 0.08, 0.07, 0.05], index=tech_indices_package)
        cpa = pd.DataFrame([29.86285714, 22.28, 19.24571429, 19.13142857, 16.14857143, 8], index=tech_indices_package)
    #     passive_package_scaling = pd.DataFrame(data=passive_pakaging_scaling_table, index=tech_indices_package)
    
    #chetan 
        Transistors_per_mm2 = pd.DataFrame([82.86e6, 38.72e6, 18.09e6, 8.45e6, 3.95e6], index = tech_indices) #, 1.85e6]) #TODO do we need 45nm numbers? or just remove? 
        Gates_per_hr_per_core = pd.DataFrame([(700e3/ 24)/ 8, (700e3/ 24) /8, (700e3/ 24)/ 8, (700e3/ 24) /8, (700e3/ 24)/ 8] , index = tech_indices) #TODO do we need 45nm case? or just remove?
    
    
    
        beolVfeol = pd.DataFrame([452/(452+126+310), 304/(304+61+257),235/(235+56+187), 235/(235+56+193), 227/(227+173), 227/(227+173)],index = tech_indices_package )
    
    
    if NEW:
        print("new")
        with open("tech_params/logic_scaling.json",'r') as logic_sc:
            LOGIC_scaling_table = json.load(logic_sc)
        logic_scaling = pd.DataFrame(data=LOGIC_scaling_table, index=tech_indices) 
    
        with open("tech_params/analog_scaling.json",'r') as analog_sc:
            analog_scaling_table = json.load(analog_sc)
        analog_scaling = pd.DataFrame(data=analog_scaling_table, index=tech_indices)
    
        with open("tech_params/sram_scaling.json",'r') as sram_sc:
            sram_scaling_table = json.load(sram_sc)
        sram_scaling = pd.DataFrame(data=sram_scaling_table, index=tech_indices)
    
        tech_indices_package = tech_indices + [65]
        with open("tech_params/defect_density.json",'r') as def_sc:
            def_scaling_table = json.load(def_sc)
        defect_density = pd.DataFrame(data=def_scaling_table,index=tech_indices_package)
    
        with open("tech_params/cpa_scaling.json",'r') as cpa_sc:
            cpa_scaling_table = json.load(cpa_sc)
        cpa = pd.DataFrame(data=cpa_scaling_table,index=tech_indices_package)
    
        with open("tech_params/transistors_scaling.json",'r') as transistors_sc:
            transistors_scaling_table = json.load(transistors_sc)
        Transistors_per_mm2 = pd.DataFrame(data=transistors_scaling_table,index=tech_indices)
    
        with open("tech_params/gates_perhr_scaling.json",'r') as gph_sc:
            gph_scaling_table = json.load(gph_sc)
        Gates_per_hr_per_core = pd.DataFrame(data=gph_scaling_table,index=tech_indices)
    
        with open("tech_params/beol_feol_scaling.json",'r') as beolfeol_sc:
            beolfeol_scaling_table = json.load(beolfeol_sc)
        beolVfeol = pd.DataFrame(data=beolfeol_scaling_table,index=tech_indices_package)
    
    
    return {
            "logic": logic_scaling,
            "analog": analog_scaling,
            "sram": sram_scaling, 
            "cpa" : cpa,
            "defect_den": defect_density,
    #         "passive_package": passive_package_scaling
            "transistors_per_mm2" : Transistors_per_mm2,
            "gates_per_hr_per_core" : Gates_per_hr_per_core,
            "beolVfeol" : beolVfeol
        }
    
    
    
