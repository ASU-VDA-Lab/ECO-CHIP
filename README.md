# ECO-CHIP

Carbon footprint estimator for heterogenous chiplet-based systems. Integration with cost estimation and NoC modeling.
ECO-CHIP Chiplet based Carbon Foot Print (CFP) analysis tool to harness the potential of heterogeneous integration (HI). Tool estimates complete total CFP [design, manufacturing, operational and packaging]. The tool considers
complex HI packaging architectures. Supports following HI and packaging architectures : RDL fanout, Silicon bridge-based, passive and active interposer, and 3D-integration. The tool evaluates the crucial package/assembly carbon
emissions which are essential for HI systems, taking into consideration size, yeild and assembly process. Tool is also capable of computing design CFP, ie. the carbon cost for designing the chip. 


The architectures description is taken from config/design.json. 
Technology nodes for chiplets is taken from config/node_list.txt 
Scaling parameters used for exploring CFP across differnt nodes and combinations are defined under tech_params/* 


# Table of Contents

-   File Structure 
-   Requirments 
-   Commands 



# File Structure

> ├── config
> │   ├── design.json
> │   └── node_list.txt
> ├── README.md
> ├── src
> │   ├── CO2_func.py
> │   ├── ECO_chip.py
> │   └── tech_scaling.py
> └── tech_params
>     ├── analog_scaling.json
>     ├── beol_feol_scaling.json
>     ├── cpa_scaling.json
>     ├── defect_density.json
>     ├── dyn_pwr_scaling.json
>     ├── gates_perhr_scaling.json
>     ├── logic_scaling.json
>     ├── sram_scaling.json
>     └── transistors_scaling.json

# Config

> design.json

Add the design that is needed to explore chiplet based CFP analysis in config/design.json file. This file currently supports three design types : "logic", "analog" and "sram". Each of these types have thier dependent scaling factors,parameters under tech_params/* directory. To determine the embodied CFP for just one type the design.json can be modified with the desired type along with its respective area. The current desing.json file shows an example for a design with 3 chiplets : logic, analog and memory. The corresponding area of the chiplet needs to be given in the format as shows in design.json under the LOGIC/ANALOG/Memory component. Current desing.json example shows a case for 3 chiplets, this can be extended to any number of chiplets. Below is an example : 

>				example/design.json 
>					{
>						Logic
>						Analog 
>						Memory
>					{
				
>				example/ex_4chiplet.json 
>					{
>						logic 
>						logic 
>						analog 
>						memory
>					}

> node_list.txt
This file accepts the specifeid nodes required for exploring various chiplet combinations, generating CFP for each possible combinations based on the chiplets numbers and nodes of intereset. 
The current node_list.txt file contains [7,10,14] producing all feasible combinations for 7nm, 10nm and 14nm, based on the specified number of chiplets. 


# src

> tech_scaling 
			This file calls in all the parameters needed from tech_param/* directory for CFP analysis

> CO2_function 
			Contains all the functions needed for CFP analysis.

> ECO_chip
			Main file that takes in the desing.json, node_list.txt as input and runs the desing. 


# tech_params 

The tech param directors holds the scaling factors along with other additional parameters such as CPA, defect density, area scaling, and dynamic_power scaling values that are needed for computing CFP for a given chiplet type. 
From [3] it is very clear that older tech nodes have lower CFP compared to newer tech due to better yeild and defect density, we account for this in defect_density.json file.
Analog,logic and memory exhibit varying scaling rates [10][22]. Incorporating the transistor desnity scaling trends from [28][29] allows us to address distinct scaling factors for differnt deisng types. By factoring in scaling trends in analog, memory and logic, we obtain a comprehensice and accurate perspective for CFP analysis.

# To run ECO-CHIP

>   Requirments to input to the code

        Area(mm2) and type for each chiplet 
        #total power of the chip
        
>    Steps

```sh
git clone <MODULE PATH>
cd ECO-CHIP 
```    

Modify config/desing.json to the required design with area for each type (logic,analog and memory).
Modify config/nodes.txt to the desired nodes for with CFP needs to be explored across. 
    
Command for CFP exploration across nodes : 

```sh
python3 src/ECO_chip.py --design config/desing.json 
```

# Requirments 

