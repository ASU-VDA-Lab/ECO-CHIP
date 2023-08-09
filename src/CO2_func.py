import numpy as np
import itertools as it
from   matplotlib import pyplot as plt
from tech_scaling import *

#Yeild Calculation 
def yield_calc(area, defect_density):
    yield_val = (1+(defect_density*1e4)*(area*1e-6)/10)**-10
    return yield_val

###############################################
#TODO remove old commented codes

Trasistors_per_gate = 8 #TODO Where does these 3 lines go? 
Power_per_core = 10
Carbon_per_kWh = 700

def design_costs(areas, comb,scaling_factors):
    #transistors = areas * np.array([Transistors_per_mm2[x] for x in comb])
    transistors = areas * np.array([scaling_factors['transistors_per_mm2'].loc[x,'Transistors_per_mm2'] for x in comb])
    #print("comb:",comb)
    #print("transistors: ", transistors)
    gates = transistors/Trasistors_per_gate
    #print(gates)
    #CPU_core_hours = gates/np.array([Gates_per_hour_per_core[x] for x in comb])
    CPU_core_hours = gates/np.array([scaling_factors['gates_per_hr_per_core'].loc[x,'Gates_per_hr_per_core'] for x in comb])
    #print(CPU_core_hours)
    total_energy = Power_per_core*CPU_core_hours/1000 #in kWh
    design_carbon = Carbon_per_kWh * total_energy
    return design_carbon


################################################
#TODO : Remove unwanted prints and others

#  1 interface every 10mm length
def recursive_split(areas, axis=0):
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
        left, l_if = recursive_split(blocks[0], (axis+1)%2)
#         print("left",axis, left)
        right, r_if = recursive_split(blocks[1], (axis+1)%2)
#         print("right",axis, right)
        sizes = np.array((0.0,0.0))
        sizes[axis] = left[axis] + right[axis] + 0.5
        sizes[(axis+1)%2] = np.max((left[(axis+1)%2], right[(axis+1)%2]))
        t_if = l_if + r_if 
        t_if += np.ceil(np.min((left[(axis+1)%2], right[(axis+1)%2]))/10) # for overlap 1 interface per 10mm
        return sizes, t_if


################################################
#TODO : Remove comments 
# How to access scaling_factors ? I am addeing htis as gunction input 

def Si_chip(techs, types, areas,scaling_factors,packaging=False, always_chiplets=False):
    area = np.array(areas)
    cpa =  np.array([scaling_factors['cpa'].loc[c, 'cpa'] for c in techs])
#     delay =  np.array([scaling_factors[ty].loc[techs[i], 'delay'] for i, ty in enumerate(types)])
    if not packaging:
        area_scale = np.array([scaling_factors[ty].loc[techs[i], 'area'] for i, ty in enumerate(types)])
        design_carbon = design_costs(areas*area_scale, techs,scaling_factors)
        defect_den = scaling_factors['defect_den']
    else:
        design_carbon = 0
        defect_den = scaling_factors['defect_den']/4 # packaing has lower density 
        #Cost-effective design of scalable high-performance systems using active and passive interposers
        area_scale = np.ones_like(area)
    
    if (np.all(np.array(techs) == techs[0]) and  not always_chiplets):
        yields = yield_calc((area*area_scale).sum(), defect_den.loc[techs[0],'defect_density'])
    else:
        yields = np.zeros_like(techs,dtype=np.float)
        for i, c in enumerate(techs):   
            yields[i] = yield_calc(areas[i]*area_scale[i], scaling_factors['defect_den'].loc[c,'defect_density'])
#         print("yields:", yields)
    carbon = area_scale*cpa*area/yields
    return carbon, design_carbon, area_scale

###############################################
#TODO : Remove comments 
#where to put the below constants  ? numBEOL ? RDLLayers? I think these are pkg parameters right ?


numBEOL = 8 # even carbon distribution in  old nodes #DTCO
RDLLayers = 6 
EMIBLayers = 5 


def Interposer(areas, techs, types, scaling_factors,  interposer_type="passive", always_chiplets=False):
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
    bonding_yield = 0.99
    if(~np.all(np.array(techs) == techs[0]) or always_chiplets):
        #print("hi")
        num_chiplets = len(areas)
        #print("num_chiplets ",num_chiplets)
        interposer_area, num_if = recursive_split(areas)
        num_if = np.int(np.ceil(num_if))
        interposer_area = np.prod(interposer_area) 
#         print(interposer_area, np.sum(areas))
        interposer_carbon, _, _ = Si_chip([65], ["logic"], [interposer_area],scaling_factors, True, always_chiplets)
        if (interposer_type == "active"):
            router_area = 4.47 * num_chiplets
            router_carbon = interposer_carbon * router_area / interposer_area
            package_carbon = (interposer_carbon-router_carbon)* scaling_factors['beolVfeol'].loc[65,'beolVfeol'] 
        else:
#             interposer_area = np.sum(areas)*1.1
            #0.33 in 16 convert to 7nm
            router_area = 0.33/np.array([scaling_factors[ty].loc[14, 'area'] for ty in types])
            router_carbon, _, _ = Si_chip(techs, types, router_area, scaling_factors,False)
            router_carbon = np.sum(router_carbon)
            if interposer_type == 'passive':
                package_carbon = interposer_carbon* scaling_factors['beolVfeol'].loc[65,'beolVfeol']
            elif interposer_type == 'RDL':
                package_carbon = interposer_carbon* scaling_factors['beolVfeol'].loc[65,'beolVfeol']
                package_carbon *= RDLLayers/numBEOL    
            elif (interposer_type == 'EMIB'):
                emib_area =  [5*5]*num_if
#                 print("NUMBER OF INTERFACES",num_if)
                emib_carbon, _, _ = Si_chip([22]*num_if, ["logic"]*num_if, emib_area,scaling_factors, True)
                package_carbon = np.sum(emib_carbon)*scaling_factors['beolVfeol'].loc[22,'beolVfeol'] 

    package_carbon /= bonding_yield 
    router_carbon /= bonding_yield 
    return package_carbon, router_carbon


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
                                                           types = design.type.values,scaling_factors=scaling_factors, interposer_type=package)
    
    labels = [x+y for x in packaging_techs for y in [" package", " router"]]
    carbon = pd.DataFrame(data=carbon, index=combinations, columns=labels)
    plot_packaging_carbon(carbon,labels)
#     plt.xlim([-1, 1])
    
#package_CO2(design, scaling_factors, [7, 10, 14])

###############################################
#TODO : remove comments 
#Do we need to add plots for this func? We could remove these lines  

def calculate_CO2(design, scaling_factors, techs, design_name='', interposer_type='RDL', always_chiplets=False):
    combinations=list(it.product(techs, repeat=len(design.index)))
    design_carbon = np.zeros((len(combinations), len(design.index)+1))
    carbon = np.zeros((len(combinations), len(design.index)+1))

    for n, comb in enumerate(combinations):
        carbon[n,:-1], design_carbon[n,:-1], area_scale = Si_chip(techs=comb, types=design.type.values,
                                                                  areas=design.area.values, scaling_factors=scaling_factors, always_chiplets=always_chiplets )
        carbon[n, -1] = np.sum(Interposer(areas=design.area.values*area_scale, techs=comb, types=design.type.values, scaling_factors=scaling_factors,
                                          interposer_type=interposer_type, always_chiplets=always_chiplets))
    carbon = pd.DataFrame(data=carbon, index=combinations, columns=(list(design.index) + ["packaging"]))
    carbon.plot(kind='bar', stacked=True, figsize = (21,7),
        title=f'Stacked CO2 manufacturing: {design_name}')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    
    design_carbon = pd.DataFrame(data=design_carbon, index=combinations, columns=(list(design.index) + ["packaging"]))
    design_carbon.plot(kind='bar', stacked=True, figsize = (21,7),
        title=f'Stacked CO2 design: {design_name}')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    total_carbon =  carbon + (design_carbon*10/1e5)+ 0.8*(design_carbon*100/1e5)
    total_carbon.plot(kind='bar', stacked=True, figsize = (10,7),
        title=f'Total C02 manufacturing+design: {design_name}')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    return carbon, design_carbon, total_carbon
