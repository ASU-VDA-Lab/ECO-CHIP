import pandas as pd
import json



tech_indices = [  7,  10,  14,  22,  28]
def load_tables():

   
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

    with open("tech_params/dyn_pwr_scaling.json",'r') as dyn_sc:
        dyn_scaling_table = json.load(dyn_sc)
    dyn_pwr_ratio = pd.DataFrame(data=dyn_scaling_table,index=tech_indices_package)
    
    
    return {
            "logic": logic_scaling,
            "analog": analog_scaling,
            "sram": sram_scaling, 
            "cpa" : cpa,
            "defect_den": defect_density,
            "transistors_per_mm2" : Transistors_per_mm2,
            "gates_per_hr_per_core" : Gates_per_hr_per_core,
            "beolVfeol" : beolVfeol,
            "dyn_pwr_ratio" : dyn_pwr_ratio
        }
    
    
    
