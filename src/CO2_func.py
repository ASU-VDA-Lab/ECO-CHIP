import numpy as np
import itertools as it
from   matplotlib import pyplot as plt
import math
from tech_scaling import *

debug = False

##############################################
#Yeild Calculation 
def yield_calc(area, defect_density):
    yield_val = (1+(defect_density*1e4)*(area*1e-6)/10)**-10
    #print(f"Yield is {yield_val} for area {area}") if debug else None
    return yield_val

###############################################
#TODO remove old commented codes
#TODO where does the below 3 constants go?

#Trasistors_per_gate = 8 
#Power_per_core = 10
#Carbon_per_kWh = 700

def design_costs(areas, comb,scaling_factors,Transistors_per_gate,Power_per_core,Carbon_per_kWh):
    transistors = areas * np.array([scaling_factors['transistors_per_mm2'].loc[x,'Transistors_per_mm2'] for x in comb])
    gates = transistors/Transistors_per_gate
    CPU_core_hours = gates/np.array([scaling_factors['gates_per_hr_per_core'].loc[x,'Gates_per_hr_per_core'] for x in comb])
    total_energy = Power_per_core*CPU_core_hours/1000 #in kWh
    design_carbon = Carbon_per_kWh * total_energy
    return design_carbon


################################################
#TODO : Remove unwanted prints and others


def recursive_split(areas, axis=0, emib_pitch=10):
    sorted_areas = np.sort(areas[::-1])
    if len(areas)<=1:
        v = (np.sum(areas)/2)**0.5
        size_2_1 = np.array((v + v*((axis+1)%2), v +axis*v))
#         print("single", axis, size_2_1)
        return size_2_1, 0
    else:
        sums = np.array((0.0,0.0))
        blocks= [[],[]]
        for i, area in enumerate(sorted_areas):
            blocks[np.argmin(sums)].append(area)
            sums[np.argmin(sums)] += area
#         print("blocks",axis, blocks)
        left, l_if = recursive_split(blocks[0], (axis+1)%2, emib_pitch)
#         print("left",axis, left)
        right, r_if = recursive_split(blocks[1], (axis+1)%2, emib_pitch)
#         print("right",axis, right)
        sizes = np.array((0.0,0.0))
        sizes[axis] = left[axis] + right[axis] + 0.5
        sizes[(axis+1)%2] = np.max((left[(axis+1)%2], right[(axis+1)%2]))
        t_if = l_if + r_if 
        t_if += np.ceil(np.min((left[(axis+1)%2], right[(axis+1)%2]))/emib_pitch) # for overlap 1 interface per 10mm
        return sizes, t_if


################################################
#TODO : Remove comments 
#wastage_add = will add extra si CFP wastage based on Formulae

def Si_chip(techs, types, areas,scaling_factors,Transistors_per_gate=8,Power_per_core=10,Carbon_per_kWh=700,packaging=False, always_chiplets=False,wastage_add = False,wafer_dia=450):
    area = np.array(areas)
    cpa =  np.array([scaling_factors['cpa'].loc[c, 'cpa'] for c in techs])
#     delay =  np.array([scaling_factors[ty].loc[techs[i], 'delay'] for i, ty in enumerate(types)])
    if not packaging:
        area_scale = np.array([scaling_factors[ty].loc[techs[i], 'area'] for i, ty in enumerate(types)])
        design_carbon = design_costs(areas*area_scale, techs,scaling_factors,Transistors_per_gate,Power_per_core,Carbon_per_kWh)
        defect_den = scaling_factors['defect_den']
        #print("CHIPS") if debug else None
    else:
        design_carbon = 0
        defect_den = scaling_factors['defect_den']/4 # packaing has lower density 
        #Cost-effective design of scalable high-performance systems using active and passive interposers
        area_scale = np.ones_like(area)
        #print("PACKAGING") if debug else None
    
    if (np.all(np.array(techs) == techs[0]) and  not always_chiplets):
        #print(f"MONOLITHIC with techs {techs}") if debug else None
        yields = yield_calc((area*area_scale).sum(), defect_den.loc[techs[0],'defect_density'])
        wastage_extra_cfp=0
        if wastage_add:
            wastage_extra_cfp = Si_wastage_accurate_t(wafer_dia=wafer_dia,chip_area=(area*area_scale).sum(),techs=techs,cpa_factors=scaling_factors['cpa'].loc[techs[0],'cpa'])
            wastage_extra_cfp = (wastage_extra_cfp * area) / area.sum()
    else:
        #print(f"CHIPLET with techs {techs}") if debug else None
        yields = np.zeros_like(techs,dtype=float)
        wastage_extra_cfp=np.zeros(len(techs))
        for i, c in enumerate(techs):   
            yields[i] = yield_calc(areas[i]*area_scale[i], scaling_factors['defect_den'].loc[c,'defect_density'])
#         print("yields:", yields)
            if wastage_add:
                wastage_extra_cfp[i] = Si_wastage_accurate_t(wafer_dia=wafer_dia,chip_area=areas[i]*area_scale[i],techs=techs[i],cpa_factors=scaling_factors['cpa'].loc[techs[i],'cpa'])
    
    mfg_carbon = area_scale*cpa*area / yields
    mfg_wst_carbon = mfg_carbon+wastage_extra_cfp
    if wastage_add:
        carbon = mfg_wst_carbon
    else:
        carbon = mfg_carbon
    return carbon, design_carbon, area_scale

###############################################
#TODO 

def power_chip(techs, types, scaling_factors,powers, lifetime, activity,Carbon_per_kWh):
    active = activity[0]
    on = activity[1]
    avg_pwr = activity[2]
    powers_in = np.array(powers)
    dyn_ratio =  np.array([scaling_factors['dyn_pwr_ratio'].loc[c, 'dyn_pwr_ratio'] for c in techs])
    pwr_scale = np.array([scaling_factors[ty].loc[techs[i], 'power'] for i, ty in enumerate(types)])
    powers_tech_scaled = powers_in * pwr_scale
    powers_scaled = powers_tech_scaled*on*avg_pwr*(dyn_ratio*active + (1-dyn_ratio))
    energy = lifetime*powers_scaled/1000
    op_carbon = Carbon_per_kWh * energy
    return op_carbon,powers_scaled 

###############################################
#TODO : Remove comments 



def Interposer(areas, techs, types, scaling_factors, package_type="passive", always_chiplets=False,
               interposer_node=65, tsv_pitch=0.025, tsv_size=0.005, RDLLayers=6, EMIBLayers=5, 
               emib_pitch=10, numBEOL=8, transistors_per_gate=8, power_per_core=10,
               carbon_per_kWh=700, return_router_area=False
              ):
    #TBD 
    # passive interposer
    #1. Bonding yield  - 99% from "Cost-effective design of scalable high-performance systems using active and passive interposers"
    #2. Router overhead
    #3. Area overhead  -10% from "Cost-effective design of scalable high-performance systems using active and passive interposers"
    #4. 65 nm defect density, 
    #5. pacage defect density
    #6. 65nm carbon per area
    #7. packaging yield adjustments
    package_carbon = 0 
    router_carbon = 0 
    router_design = 0
    bonding_yield = 0.99
    router_area =0
    if(~np.all(np.array(techs) == techs[0]) or always_chiplets):
        num_chiplets = len(areas)
        interposer_area, num_if = recursive_split(areas, emib_pitch=emib_pitch)
        num_if = int(np.ceil(num_if))
        interposer_area = np.prod(interposer_area) 
#         print(interposer_area, np.sum(areas))
        interposer_carbon, _, _ = Si_chip([interposer_node], ["logic"], [interposer_area],scaling_factors,
                                          transistors_per_gate, power_per_core,carbon_per_kWh, True, always_chiplets)
        if (package_type == "active"):
            router_area = 4.47 * num_chiplets
            router_carbon = interposer_carbon * router_area / interposer_area
            _, router_design, _ = Si_chip([interposer_node], ["logic"], [router_area],scaling_factors, 
                                          transistors_per_gate, power_per_core,carbon_per_kWh, True, always_chiplets)
            router_design = np.sum(router_design)
            #package_carbon = (interposer_carbon-router_carbon)* beolVfeol[65] 
            package_carbon = (interposer_carbon-router_carbon)* scaling_factors['beolVfeol'].loc[65,'beolVfeol'] 
        elif (package_type == "3D"):
            dims = np.sqrt(np.array(areas, dtype=np.float64))
            num_tsv_1d = np.floor(dims/tsv_pitch)
            overhead_3d = (num_tsv_1d**2) * (tsv_size**2)
            area_3d = areas + overhead_3d
            carbon3d, _, _ = Si_chip(techs, types, area_3d,scaling_factors,transistors_per_gate,
                                     power_per_core,carbon_per_kWh,False, always_chiplets)
            carbon2d, _, _ = Si_chip(techs, types, areas,scaling_factors,transistors_per_gate,
                                     power_per_core,carbon_per_kWh,False, always_chiplets)
            package_carbon = np.sum(carbon3d-carbon2d)
            router_area = 0.33/np.array([scaling_factors[ty].loc[14, 'area'] for ty in types])
            router_carbon, router_design, _ = Si_chip(techs, types, router_area,scaling_factors,transistors_per_gate,
                                                      power_per_core,carbon_per_kWh,False)
            router_carbon, router_design = np.sum(router_carbon), np.sum(router_design) 
            bonding_yield = bonding_yield**num_chiplets
        elif package_type in ['passive', 'RDL', 'EMIB'] :
#             interposer_area = np.sum(areas)*1.1
            #0.33 in 16 convert to 7nm
            router_area = 0.33/np.array([scaling_factors[ty].loc[14, 'area'] for ty in types])
            router_carbon, router_design, _ = Si_chip(techs, types, router_area,scaling_factors,transistors_per_gate,
                                                      power_per_core,carbon_per_kWh,False)
            router_carbon, router_design = np.sum(router_carbon), np.sum(router_design)
            if package_type == 'passive':
                package_carbon = interposer_carbon* scaling_factors['beolVfeol'].loc[interposer_node,'beolVfeol']
            elif package_type == 'RDL':
                package_carbon = interposer_carbon* scaling_factors['beolVfeol'].loc[interposer_node,'beolVfeol']
                package_carbon *= RDLLayers/numBEOL    
            elif (package_type == 'EMIB'):
                emib_area =  [5*5]*num_if
#                 print("NUMBER OF INTERFACES",num_if)
                emib_carbon, _, _ = Si_chip([22]*num_if, ["logic"]*num_if, emib_area, scaling_factors,transistors_per_gate,
                                            power_per_core,carbon_per_kWh,True)
                package_carbon = np.sum(emib_carbon)* scaling_factors['beolVfeol'].loc[22,'beolVfeol'] 
        else:
            raise NotImplemented
            
    package_carbon /= bonding_yield 
    router_carbon /= bonding_yield 
    if return_router_area:
        return package_carbon, router_carbon, router_design, router_area
    else:
        return package_carbon, router_carbon, router_design


###############################################
#TODO : Remove comments 

def plot_packaging_carbon(carbon,labels):
    carbon.plot(kind='bar', stacked=False, figsize = (21,7),
        title='Packaging CO2 overhead manufacturing')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    
    plt.figure()
    ax = carbon[[x for x in labels if 'passive' in x]].plot.bar(
            stacked=True, figsize=(21,7), color=['tab:blue','tab:orange'], position=0, width=0.2)
    carbon[[x for x in labels if 'active' in x]].plot.bar(
            stacked=True, sharex=True, ax=ax, position=1, width=0.2, color=['tab:green','tab:red'])
    carbon[[x for x in labels if 'RDL' in x]].plot.bar(
            stacked=True, sharex=True, ax=ax, position=2, width=0.2, color=['tab:purple','tab:brown'])
    carbon[[x for x in labels if 'EMIB' in x]].plot.bar(
            stacked=True, sharex=True, ax=ax, position=3, width=0.2, color=['tab:pink','tab:cyan'])
    legend = ax.legend(labels, fontsize=12)#, loc='center left', bbox_to_anchor=(1.0, 0.93))
    plt.show()

def package_CO2(design, scaling_factors, techs):
    combinations=list(it.product(techs, repeat=len(design.index)))
    packaging_techs = ["passive","active","RDL","EMIB"]
    carbon = np.zeros((len(combinations), len(packaging_techs)*2))

    for n, comb in enumerate(combinations):
        _, _, area_scale = Si_chip(techs=comb, types=design.type.values, areas=design.area.values,scaling_factors=scaling_factors )
        for i, package in enumerate(packaging_techs):
            carbon[n, 2*i], carbon[n, 2*i+1] = Interposer(areas=design.area.values*area_scale, techs=comb, 
                                                           types = design.type.values,scaling_factors=scaling_factors, package_type=package)
    
    labels = [x+y for x in packaging_techs for y in [" package", " router"]]
    carbon = pd.DataFrame(data=carbon, index=combinations, columns=labels)
    plot_packaging_carbon(carbon,labels)
#     plt.xlim([-1, 1])
    
#package_CO2(design, scaling_factors, [7, 10, 14])


###############################################
#Wastage calculation 

def Si_wastage_accurate_t(wafer_dia,chip_area,techs,cpa_factors):
    si_area = (math.pi * (wafer_dia ** 2))/4
    dpw = math.pi * wafer_dia * ((wafer_dia/(4*chip_area)) - (1/math.sqrt(2*chip_area)))
    area_wastage = si_area - (math.floor(dpw)*chip_area)
    #unused_si_cfp = wastage_cfp(area_wastage,techs,scaling_factors)
    unused_si_cfp = area_wastage*cpa_factors
    wastage_si_cfp_pdie = unused_si_cfp/dpw
    return wastage_si_cfp_pdie

###############################################
#TODO : remove comments 
 


def calculate_CO2(design, scaling_factors, techs, design_name='', num_iter=90, package_type='RDL', always_chiplets=False,
                  lifetime = 2*365*24, activity=[0.2, 0.667, 0.1], Ns = 1e5, Nc=None, plot=False,package_factor=1,
                  return_ap=False, in_combinations=None, transistors_per_gate=8, power_per_core=10, carbon_per_kWh=700,
                  interposer_node=65, rdl_layer = 6, emib_layers = 5, emib_pitch=10, tsv_pitch = 0.025,
                  tsv_size = 0.005, num_beol = 8
                 ):
    #num_iter = 90
    
    #C if in_combinations is None:
    #C     combinations = list(it.product(techs, repeat=len(design.index)))
    #C else:
    #C     combinations = in_combinations
    combinations = design.node.values
    combinations = [tuple(combinations)] 
    
    if len(design.index) == 1: #Monolithic
        always_chiplets = False
    else:
        always_chiplets = True
    
    design_carbon = np.zeros((len(combinations), len(design.index)+1))
    op_carbon = np.zeros((len(combinations), len(design.index)+1))
    carbon = np.zeros((len(combinations), len(design.index)+1))
    
    areas=  np.zeros((len(combinations), len(design.index)))
    powers =  np.zeros((len(combinations), len(design.index)))

    
    for n, comb in enumerate(combinations):
        print("######################### ") if debug else None
        print(f"Running combination {comb} with number {n}") if debug else None
        carbon[n,:-1], design_carbon[n,:-1], area_scale = Si_chip(techs=comb, types=design.type.values,
                                                                  areas=design.area.values,scaling_factors=scaling_factors, Transistors_per_gate=transistors_per_gate,
                                                                  Power_per_core=power_per_core,Carbon_per_kWh=carbon_per_kWh, always_chiplets=always_chiplets,wastage_add=True )
        package_c, router_c, design_carbon[n,-1], router_a =Interposer(areas=design.area.values*area_scale, techs=comb, types=design.type.values,scaling_factors=scaling_factors,
                                          package_type=package_type, always_chiplets=always_chiplets, interposer_node=interposer_node,
                                          tsv_pitch=tsv_pitch, tsv_size=tsv_size, RDLLayers=rdl_layer, EMIBLayers=emib_layers, emib_pitch=emib_pitch, numBEOL=num_beol, 
                                          transistors_per_gate=transistors_per_gate,power_per_core=power_per_core,carbon_per_kWh=carbon_per_kWh,return_router_area=True)
        carbon[n, -1] = package_c*package_factor + router_c
        
        op_carbon[n,:-1], powers[n, :] = power_chip(comb, design.type.values,scaling_factors, design.power.values, lifetime, activity,Carbon_per_kWh=carbon_per_kWh)
        areas[n] =  design.area.values*area_scale +router_a
    if Nc is None:
        design_carbon *= num_iter/Ns
        total_carbon = carbon + design_carbon + op_carbon
    else:
        design_carbon *= num_iter/Nc[None,:]
        total_carbon = carbon + design_carbon + op_carbon
    carbon = pd.DataFrame(data=carbon, index=combinations, columns=(list(design.index) + ["Packaging"]))
    design_carbon = pd.DataFrame(data=design_carbon, index=combinations, columns=(list(design.index) + ["Packaging"]))
    op_carbon = pd.DataFrame(data=op_carbon, index=combinations, columns=(list(design.index) + ["Packaging"]))
    #     total_carbon =  carbon + (design_carbon*10/1e5)+ 0.8*(design_carbon*100/1e5)
    total_carbon = pd.DataFrame(data=total_carbon, index=combinations, columns=(list(design.index) + ["Packaging"]))
    
        
    if plot:
        carbon.plot(kind='bar', stacked=True, figsize = (21,7),
            title=f'Stacked CO2 manufacturing: {design_name}')
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        design_carbon.plot(kind='bar', stacked=True, figsize = (21,7),
            title=f'Stacked CO2 design: {design_name}')
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        op_carbon.plot(kind='bar', stacked=True, figsize = (21,7),
            title=f'Stacked CO2 operations: {design_name}')
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
    
        total_carbon.plot(kind='bar', stacked=True, figsize = (10,7),
            title=f'Total C02 manufacturing+design: {design_name}')
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
    
    if not return_ap:
        return carbon, design_carbon, total_carbon, op_carbon
    else:
        return carbon, design_carbon, total_carbon, op_carbon, areas, powers
    
