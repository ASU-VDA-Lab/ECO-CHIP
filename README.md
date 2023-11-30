# ECO-CHIP : Estimation of Carbon Footprint of Chiplet-based Architectures for Sustainable VLSI
[[paper](https://arxiv.org/pdf/2306.09434.pdf)]

Carbon footprint estimator for heterogenous chiplet-based systems. 
ECO-CHIP is an analysis tool that analyzes the operational and embodied CFP (design, manufacturing, and packaging). The tool supports the following HI and packaging architectures: RDL fanout, silicon bridge-based, passive and active interposer, and 3D integration. The tool evaluates the crucial package/assembly carbon emissions essential for HI systems, considering size, yield, and assembly process. In addition, it also estimates design CFP.  

<img src="eco-chip-top.png" alt="drawing" width="600"/>

## Abstract
Decades of progress in energy-efficient and lowpower design have successfully reduced the operational carbon footprint in the semiconductor industry. However, this has led to increased embodied emissions, arising from design, manufacturing, and packaging. While existing research has developed tools to analyze embodied carbon for traditional monolithic systems, these tools do not apply to near-mainstream heterogeneous integration (HI) technologies. HI systems offer significant potential for sustainable computing by minimizing carbon emissions through two key strategies: “reducing” computation by “reusing” pre-designed chiplet IP blocks and adopting hierarchical approaches to system design. The reuse of  chiplets across multiple designs, even spanning multiple generations of ICs, can substantially reduce carbon emissions throughout the lifespan. This paper introduces ECO-CHIP, a carbon analysis tool designed to assess the potential of HI systems toward sustainable computing by considering scaling, chiplet, and packaging yields, design complexity, and even overheads associated with advanced packaging techniques. Experimental results from ECO-CHIP demonstrate that HI can reduce embodied carbon emissions by up to 30% compared to traditional monolithic systems. ECOCHIP is integrated with other chiplet simulators and is applied to chiplet disaggregation considering other metrics such as power, area, and cost. ECO-CHIP suggests that HI can pave the way for sustainable computing practices.

## Table of Contents

-   [File structure](#file-structure)
-   [Getting started](#getting-started)
-   [Config and input definition](#input-definition-and-config)
-   [Running ECO-CHIP](#running-eco-chip)
-   [Outputs](#outputs)


## File structure

- **config/**
  - **example/**
    - [architecture.json](./config/example/architecture.json)
    - [designC.json](./config/example/designC.json)
    - [node_list.txt](./config/example/node_list.txt)
    - [operationalC.json](./config/example/operationalC.json)
    - [packageC.json](./config/example/packageC.json)
- [README.md](./README.md)
- [requirements.txt](./requirements.txt)
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
- **testcases/**
  - **A15/**
    - [architecture.json](./testcases/A15/architecture.json)
    - [designC.json](./testcases/A15/designC.json)
    - [node_list.txt](./testcases/A15/node_list.txt)
    - [operationalC.json](./testcases/A15/operationalC.json)
    - [packageC.json](./testcases/A15/packageC.json)
  - **EMR2/**
    - [architecture.json](./testcases/EMR2/architecture.json)
    - [designC.json](./testcases/EMR2/designC.json)
    - [node_list.txt](./testcases/EMR2/node_list.txt)
    - [operationalC.json](./testcases/EMR2/operationalC.json)
    - [packageC.json](./testcases/EMR2/packageC.json)
  - **GA102/**
    - [architecture.json](./testcases/GA102/architecture.json)
    - [designC.json](./testcases/GA102/designC.json)
    - [node_list.txt](./testcases/GA102/node_list.txt)
    - [operationalC.json](./testcases/GA102/operationalC.json)
    - [packageC.json](./testcases/GA102/packageC.json)
  - **TigerLake/**
    - [architecture.json](./testcases/TigerLake/architecture.json)
    - [designC.json](./testcases/TigerLake/designC.json)
    - [node_list.txt](./testcases/TigerLake/node_list.txt)
    - [operationalC.json](./testcases/TigerLake/operationalC.json)
    - [packageC.json](./testcases/TigerLake/packageC.json)

## Getting started

### Prerequisites

ECO-CHIP requires the following:

- python 3.8
- pip 20.0.2
- python3.8-venv

Additionally, please refer to the requirements.txt file in this repository. The packages in requirements.txt will be installed in a virtual environment.

### Download and install with bash

```
git clone https://github.com/ASU-VDA-Lab/ECO-CHIP.git
cd ECO-CHIP
python3 -m venv eco-chip
source eco-chip/bin/activate
pip3 install -r requirements.txt
```

## Input definition and config

ECO-CHIP has three inputs, including a design configuration file, a list of supported technology nodes, and technology/scaling parameter files which are all described below: 

### Architecture configuration

The input system architecture is specified in [architecture.json](config/example/architecture.json) file. The high-level details of each chiplet must be specified as shown below. In the example below, there are three chiplets named chiplet1, chiplet2, and chiplet3.  Each chiplet has its type, which currently includes one of three categories: logic, analog, or sram. To select from five distinct pacakging architectures, the parameter 'pkg_type' can be used with "RDL", "EMIB", "passive", "active" and "3D". The area of each chiplet is also specified in mm2, as shown below.  

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
       },
"pkg_type" : "RDL"
}
```
The above file can be extended to support any number of chiplets by adding more entries to the JSON file. 

### Design carbon parameters
The [designC.json](./config/example/designC.json) includes parameters such as the number of design iterations, volume (indicating the number of manufactured parts), and the overall architecture power. Additionally, it encompasses parameters like transistors_per_gate, power_per_core which is the power consumed by the compute resources used for design, as well as carbon_per_kWh, indicating the carbon footprint per kWh from the source. The transistor per gate is used to calculate the number of logic gates in the design which is further used to evaluate design effort. 

### Technology node list

The [node_list.txt](./config/node_list.txt) file specifies the possible combination of nodes each chiplet can be implemented in. The current node_list.txt file contains [7,10,14] and ECO-CHIP generates the CFP for  all feasible combinations for 7nm, 10nm and 14nm, for all the chiplets specified in design.json. ECO-CHIP currently supports the following nodes 7nm, 10nm, 14nm, 22nm, and 28nm. 

### Operational carbon parameters
In [operationalC.json](./config/example/operationalC.json) the lifetime value parameter is provided in hours as its unit of measurement. The current example file demonstrates a lifetime of 2 years (2*365*24 = 17520)

### Pacakge carbon parameters
The [packageC.json](./config/example/packageC.json) contains all the package-related parameters. The Interposer node defines the technology node for the interposer used, RDLLayer defines the number of RDL layers, TSV pitch (pitch per mm) and TSV size (per mm) used for 3D packaging architecture, EMIB bridge range value is defined with emib_pitch parameter and the numBEOL for number of BEOL layers. 

### Technology/scaling parameters 

The [tech params directory](./tech_params/.) holds the scaling factors along with other additional parameters such as CPA, defect density, area scaling, and dynamic_power scaling values  needed for computing CFP for a given chiplet type. 
Analog, logic, and memory exhibit varying scaling rates [[1]][AMD-scaling] [[2]][Intel-Scaling]. Incorporating the transistor density scaling trends from [[3]][TSMC-scaling] [[4]][SRAM-scaling] allows us to address distinct scaling factors for different design types. By factoring in scaling trends in analog, memory, and logic, ECO-CHIP computes CFP.


## Running ECO-CHIP

Modify config/desing.json to the required design with an area for each type (logic, analog and memory). Modify config/nodes.txt to the desired nodes for which CFP needs to be explored across. 
    
The command for CFP exploration across nodes : 

```sh
python3 src/ECO_chip.py --design_dir config/example/
```

To run one of the testcases :
```sh
python3 src/ECO_chip.py --design_dir testcases/TigerLake/
python3 src/ECO_chip.py --design_dir testcases/GA102/
```

## Outputs

Example output for Tiger Lake test case with 7nm and 10nm nodes in node_list.txt file. 

```
 ---------------------------------------------------------
Using below files for CFP estimations : 

testcases/TigerLake/architecture.json
testcases/TigerLake/node_list.txt
testcases/TigerLake/designC.json
testcases/TigerLake/operationalC.json
testcases/TigerLake/packageC.json
 ---------------------------------------------------------
 
'testcases/TigerLake/' Example testcase
 ---------------------------------------------------------
Total Carbon in Kgs 
                   CPU    Analog    Memory  Packaging
(7, 7, 7)     4.169723  6.361167  2.817943   0.000000
(7, 7, 10)    4.123481  6.307968  2.394593   0.252043
(7, 10, 7)    4.123481  5.419826  2.781703   0.249348
(7, 10, 10)   4.123481  5.419826  2.394593   0.246365
(10, 7, 7)    4.770286  6.307968  2.781703   0.319030
(10, 7, 10)   4.770286  6.307968  2.394593   0.316047
(10, 10, 7)   4.770286  5.419826  2.781703   0.313353
(10, 10, 10)  4.798368  5.466991  2.421830   0.000000
 ---------------------------------------------------------
```

Example output for GA102 testcase with 7nm,10nm and 14nm in the node_list.txt file.


```
 ---------------------------------------------------------
Using below files for CFP estimations : 

testcases/GA102/architecture.json
testcases/GA102/node_list.txt
testcases/GA102/designC.json
testcases/GA102/operationalC.json
testcases/GA102/packageC.json
 ---------------------------------------------------------
 
'testcases/GA102/' Example testcase
 ---------------------------------------------------------
Total Carbon in Kgs 
                   GPU_1     Analog     Memory  Packaging
(7, 7, 7)     166.492242  36.051578  23.026315   0.000000
(7, 7, 10)    157.072901  30.858934  16.911125   2.845736
(7, 7, 14)    157.072901  30.858934  19.615335   3.117421
(7, 10, 7)    157.072901  26.586697  19.551602   2.842875
(7, 10, 10)   157.072901  26.586697  16.911125   2.839708
(7, 10, 14)   157.072901  26.586697  19.615335   3.111394
(7, 14, 7)    157.072901  23.534043  19.551602   2.840229
(7, 14, 10)   157.072901  23.534043  16.911125   2.837062
(7, 14, 14)   157.072901  23.534043  19.615335   3.108748
(10, 7, 7)    189.316945  30.858934  19.551602   5.102011
(10, 7, 10)   189.316945  30.858934  16.911125   5.098844
(10, 7, 14)   189.316945  30.858934  19.615335   5.497888
(10, 10, 7)   189.316945  26.586697  19.551602   5.095984
(10, 10, 10)  196.405500  30.756347  19.644226   0.000000
(10, 10, 14)  189.316945  26.586697  19.615335   5.491861
(10, 14, 7)   189.316945  23.534043  19.551602   5.093338
(10, 14, 10)  189.316945  23.534043  16.911125   5.090171
(10, 14, 14)  189.316945  23.534043  19.615335   5.489215
(14, 7, 7)    280.104180  30.858934  19.551602   9.711567
(14, 7, 10)   280.104180  30.858934  16.911125   9.708401
(14, 7, 14)   280.104180  30.858934  19.615335  10.347061
(14, 10, 7)   280.104180  26.586697  19.551602   9.705540
(14, 10, 10)  280.104180  26.586697  16.911125   9.702373
(14, 10, 14)  280.104180  26.586697  19.615335  10.341034
(14, 14, 7)   280.104180  23.534043  19.551602   9.702894
(14, 14, 10)  280.104180  23.534043  16.911125   9.699727
(14, 14, 14)  298.871352  31.355502  27.894171   0.000000
 ---------------------------------------------------------

```

## Citation

If you find ECO-CHIP useful or relavent to your research, please kindly cite our paper:

```bibtex
@misc{sudarshan2023ecochip,
      title={ECO-CHIP: Estimation of Carbon Footprint of Chiplet-based Architectures for Sustainable VLSI}, 
      author={Chetan Choppali Sudarshan and Nikhil Matkar and Sarma Vrudhula and Sachin S. Sapatnekar and Vidya A. Chhabria},
      year={2023},
      eprint={2306.09434},
      archivePrefix={arXiv},
      primaryClass={cs.AR}
}
```


  [AMD-scaling]: <https://ieeexplore.ieee.org/document/9063103>
  [Intel-scaling]: <https://www.computer.org/csdl/proceedings-article/hcs/2022/09895532/1GZiGKCWYMw>
  [TSMC-scaling]: <https://www.angstronomics.com/p/the-truth-of-tsmc-5nm>
  [SRAM-scaling]: <https://fuse.wikichip.org/news/7343/iedm-2022-did-we-just-witness-the-death-of-sram/#google_vignette>


