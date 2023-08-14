# ECO-CHIP

Carbon footprint estimator for heterogenous chiplet-based systems. 
ECO-CHIP is an analysis tool that analyzes the operational and embodied CFP (design, manufacturing, and packaging). The tool supports the following HI and packaging architectures: RDL fanout, silicon bridge-based, passive and active interposer, and 3D integration. The tool evaluates the crucial package/assembly carbon emissions essential for HI systems, considering size, yield, and assembly process. In addition, it also estimates design CFP.  

<img src="eco-chip-top.png" alt="drawing" width="600"/>


## Table of Contents

-   [File structure](#file-structure)
-   [Getting started](#getting-started)
-   [Config and input definition](#input-definition-and-config)
-   [Running ECO-CHIP](#running-eco-chip)
-   [Outputs](#outputs)


## File structure

- **config/**
  - [design.json](./config/design.json)
  - [node_list.txt](./config/node_list.txt)
- **examples**
  - [a15.json](./examples/a15.json)
  - [emr2.json](.examples/emr2.json)
  - [ga102.json](./examples/ga102.json)
  - [tigerlake.json](./examples/tigerlake.json)
- [README.md](./README.md)
- **src/**
  - [CO2_func.py](./src/CO2_func.py)
  - [ECO_chip.py](./src/ECO_chip.py)
  - [tech_scaling.py](./src/tech_scaling.py)
- **tech_params/**
  - [analog_scaling.json](./tech_params/analog_scaling.json)
  - [beol_feol_scaling.json](./tech_params/beol_feol_scaling.json)
  - [cpa_scaling.json](./tech_params/cpa_scaling.json)
  - [defect_density.json](./tech_params/defect_density.json)
  - [dyn_pwr_scaling.json](./tech_params/dyn_pwr_scaling.json)
  - [gates_perhr_scaling.json](./tech_params/gates_perhr_scaling.json)
  - [logic_scaling.json](./tech_params/logic_scaling.json)
  - [sram_scaling.json](./tech_params/sram_scaling.json)
  - [transistors_scaling.json](./tech_params/transistors_scaling.json)

## Getting started

### Prerequisites

ECO-CHIP requires the following:

- python 3.6
- pip 18.1
- python3-venv

Additionally, please refer to the requirements.txt file in this repository. The packages in requirements.txt will be installed in a virtual environment.

### Download and install with bash

```
git clone <path>
cd ECO-CHIP
python3 -m venv eco-chip
source eco-chip/bin/activate
pip3 install -r requirements.txt
```

## Input definition and config

ECO-CHIP has three inputs, including a design configuration file, a list of supported technology nodes, and technology/scaling parameter files which are all described below: 

### Design configuration

The input system architecture is specified in [design.json!](config/design.json) file. The high-level details of each chiplet must be specified as shown below. In the example below, there are three chiplets named chiplet1, chiplet2, and chiplet3.  Each chiplet has its type, which currently includes one of three categories: logic, analog, or sram. The area of each chiplet is also specified, as shown below.  

```
{
"chiplet1" : {
          "type" : "logic",
          "area" : 16.04
        },
"chiplet2" : {
          "type" : "analog",
          "area" : 24.47
        },
"chiplet3" : {
          "type" : "sram",
          "area" : 10.84
       }
}
```
The above file can be extended to support any number of chiplets by adding more entries to the JSON file. 

### Technology node list

The [node_list.txt!](./config/node_list.txt) file specifies the possible combination of nodes each chiplet can be implemented in. The current node_list.txt file contains [7,10,14] and ECO-CHIP generates the CFP for  all feasible combinations for 7nm, 10nm and 14nm, for all the chiplets specified in design.json. ECO-CHIP currently supports the following nodes 7nm, 10nm, 14nm, 22nm, and 28nm. 


### Technology/scaling parameters 

The [tech params directory!](./tech_params/.) holds the scaling factors along with other additional parameters such as CPA, defect density, area scaling, and dynamic_power scaling values  needed for computing CFP for a given chiplet type. 
Analog, logic, and memory exhibit varying scaling rates [10][22]. Incorporating the transistor density scaling trends from [28][29] allows us to address distinct scaling factors for different design types. By factoring in scaling trends in analog, memory and logic, ECO-CHIP computes CFP.


## Running ECO-CHIP

Modify config/desing.json to the required design with an area for each type (logic, analog and memory). Modify config/nodes.txt to the desired nodes for which CFP needs to be explored across. 
    
The command for CFP exploration across nodes : 

```sh
python3 src/ECO_chip.py --design config/desing.json 
```

## Outputs

Example output for Tiger Lake test case with 7nm and 10nm nodes in node_list.txt file. 

```
Tiger Lake example
 ---------------------------------------------------------
Manufacture Carbon in Kgs 
                     CPU      Analog      Memory   packaging
(7, 7, 7)     464.214115  708.186995  313.720761    0.000000
(7, 7, 10)    432.766506  671.391611  213.804363  241.024435
(7, 10, 7)    432.766506  489.914178  289.450300  239.971857
(7, 10, 10)   432.766506  489.914178  213.804363  238.807710
(10, 7, 7)    630.761119  671.391611  289.450300  306.181434
(10, 7, 10)   630.761119  671.391611  213.804363  305.017287
(10, 10, 7)   630.761119  489.914178  289.450300  303.964709
(10, 10, 10)  655.606228  513.023394  227.264961    0.000000
 ---------------------------------------------------------
Design Carbon in Kgs 
                     CPU      Analog      Memory  packaging
(7, 7, 7)     287.080073  437.958191  194.011720   0.000000
(7, 7, 10)    287.080073  437.958191   90.660565   8.948917
(7, 10, 7)    287.080073  204.655353  194.011720   7.456146
(7, 10, 10)   287.080073  204.655353   90.660565   5.802618
(10, 7, 7)    261.534514  437.958191  194.011720  10.460767
(10, 7, 10)   261.534514  437.958191   90.660565   8.807239
(10, 10, 7)   261.534514  204.655353  194.011720   7.314468
(10, 10, 10)  261.534514  204.655353   90.660565   0.000000
 ---------------------------------------------------------
Operational Carbon in Kgs 
                      CPU       Analog       Memory  packaging
(7, 7, 7)     3329.401525  5079.205444  2250.044422        0.0
(7, 7, 10)    3329.401525  5079.205444  2054.413792        0.0
(7, 10, 7)    3329.401525  4637.592758  2250.044422        0.0
(7, 10, 10)   3329.401525  4637.592758  2054.413792        0.0
(10, 7, 7)    3762.284583  5079.205444  2250.044422        0.0
(10, 7, 10)   3762.284583  5079.205444  2054.413792        0.0
(10, 10, 7)   3762.284583  4637.592758  2250.044422        0.0
(10, 10, 10)  3762.284583  4637.592758  2054.413792        0.0
 ---------------------------------------------------------
Total Carbon in Kgs 
                      CPU       Analog       Memory   packaging
(7, 7, 7)     4080.695713  6225.350630  2757.776904    0.000000
(7, 7, 10)    4049.248104  6188.555247  2358.878721  249.973352
(7, 10, 7)    4049.248104  5332.162290  2733.506443  247.428002
(7, 10, 10)   4049.248104  5332.162290  2358.878721  244.610328
(10, 7, 7)    4654.580217  6188.555247  2733.506443  316.642201
(10, 7, 10)   4654.580217  6188.555247  2358.878721  313.824527
(10, 10, 7)   4654.580217  5332.162290  2733.506443  311.279177
(10, 10, 10)  4679.425325  5355.271505  2372.339318    0.000000
```




