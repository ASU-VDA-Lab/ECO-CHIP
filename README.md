# ECO-CHIP : Estimation of Carbon Footprint of Chiplet-based Architectures for Sustainable VLSI [[paper](https://arxiv.org/pdf/2306.09434.pdf)] [[artifact](https://zenodo.org/records/10223759)] [[Slides](./uploads/ECO-CHIP-Chetan-HPCA2024.pdf)] [[Poster](./uploads/ECO-CHIP-HPCA2024-Poster.pdf)]


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
-   [Artifact](#artifact)


## File structure

- **config/**
  - **example/**
    - [architecture.json](./config/example/architecture.json)
    - [designC.json](./config/example/designC.json)
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
    - [operationalC.json](./testcases/A15/operationalC.json)
    - [packageC.json](./testcases/A15/packageC.json)
  - **EMR2/**
    - [architecture.json](./testcases/EMR2/architecture.json)
    - [designC.json](./testcases/EMR2/designC.json)
    - [operationalC.json](./testcases/EMR2/operationalC.json)
    - [packageC.json](./testcases/EMR2/packageC.json)
  - **GA102/**
    - [architecture.json](./testcases/GA102/architecture.json)
    - [designC.json](./testcases/GA102/designC.json)
    - [operationalC.json](./testcases/GA102/operationalC.json)
    - [packageC.json](./testcases/GA102/packageC.json)
  - **TigerLake/**
    - [architecture.json](./testcases/TigerLake/architecture.json)
    - [designC.json](./testcases/TigerLake/designC.json)
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

The input system architecture is specified in [architecture.json](config/example/architecture.json) file. The high-level details of each chiplet must be specified as shown below. In the example below, there are three chiplets named chiplet1, chiplet2, and chiplet3.  Each chiplet has its type, which currently includes one of three categories: logic, analog, or sram. The corresponding nodes to each of the chiplet need to be mentioned as shown below. ECO-CHIP currently supports the following nodes 7nm, 10nm, 14nm, 22nm, and 28nm. To select from five distinct pacakging architectures, the parameter 'pkg_type' can be used with "RDL", "EMIB", "passive", "active" and "3D". The area of each chiplet is also specified in mm2, as shown below.  

```
{
"chiplet1" : {
          "type" : "logic",
          "area" : 16.04,
          "node" : 7
        },
"chiplet2" : {
          "type" : "analog",
          "area" : 24.47,
          "node" : 10
        },
"chiplet3" : {
          "type" : "sram",
          "area" : 10.84,
          "node" : 10
       },
"pkg_type" : "RDL"
}
```
The above file can be extended to support any number of chiplets by adding more entries to the JSON file. 

### Design carbon parameters
The [designC.json](./config/example/designC.json) includes parameters such as the number of design iterations, volume (indicating the number of manufactured parts), and the overall architecture power. Additionally, it encompasses parameters like transistors_per_gate, power_per_core which is the power consumed by the compute resources used for design, as well as carbon_per_kWh, indicating the carbon footprint per kWh from the source. The transistor per gate is used to calculate the number of logic gates in the design which is further used to evaluate design effort. 

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
testcases/TigerLake/designC.json
testcases/TigerLake/operationalC.json
testcases/TigerLake/packageC.json
 ---------------------------------------------------------
 
'testcases/TigerLake/' Example testcase
 ---------------------------------------------------------
Manufacture Carbon in Kgs 
                  CPU    Analog    Memory  Packaging
(7, 10, 10)  0.443625  0.505251  0.218273   0.244415
 ---------------------------------------------------------
Design Carbon in Kgs 
                 CPU    Analog    Memory  Packaging
(7, 10, 10)  0.28708  0.204655  0.090661   0.005803
 ---------------------------------------------------------
Operational Carbon in Kgs 
                  CPU    Analog    Memory  Packaging
(7, 10, 10)  3.329402  4.637593  2.054414        0.0
 ---------------------------------------------------------
Total Carbon in Kgs 
                  CPU    Analog    Memory  Packaging
(7, 10, 10)  4.060106  5.347499  2.363347   0.250218
 ---------------------------------------------------------
```

Example output for GA102 testcase with 7nm,10nm and 14nm in the node_list.txt file.


```
 ---------------------------------------------------------
Using below files for CFP estimations : 

testcases/GA102/architecture.json
testcases/GA102/designC.json
testcases/GA102/operationalC.json
testcases/GA102/packageC.json
 ---------------------------------------------------------
 
'testcases/GA102/' Example testcase
 ---------------------------------------------------------
Manufacture Carbon in Kgs 
                 GPU_1    Analog    Memory  Packaging
(7, 10, 14)  26.787675  2.099898  2.216669   4.170742
 ---------------------------------------------------------
Design Carbon in Kgs 
                GPU_1    Analog    Memory  Packaging
(7, 10, 14)  7.606727  0.769695  0.437029   0.005642
 ---------------------------------------------------------
Operational Carbon in Kgs 
                  GPU_1     Analog     Memory  Packaging
(7, 10, 14)  118.006498  23.330982  16.596411        0.0
 ---------------------------------------------------------
Total Carbon in Kgs 
                GPU_1     Analog     Memory  Packaging
(7, 10, 14)  152.4009  26.200575  19.250109   4.176384
 ---------------------------------------------------------
```

With ECO-CHIP you can perform technology and chiplet space carbon exploration based on the architectural inputs to the framework. 

<img src="tech-chiplet-sweep.png" alt="drawing" width="600"/>

It also can take in multiple chiplets and shown below is the variation in total CFP for different chiplet (Nc) numbers for a test case. 

<img src="nc-sweep.png" alt="drawing" width="600"/>

## Artifact 

This artifact is released on Zenodo and contains two parts. The first is [ECO-CHIP](https://github.com/ASU-VDA-Lab/ECO-CHIP) submodule from GitHub (current GitHub repository), and the second is a folder that consists of experiments performed using ECO-CHIP. The appendix section in the paper describes the installation of our artifact, ECO-CHIP, and the procedure to reproduce the results in the paper. 

The artifact directory is available on [ECO-CHIP-Zenodo-Artifact-Link](https://zenodo.org/records/10223759) and has a detailed description of regenerating the results in the paper. 

## Citation

If you find ECO-CHIP useful or relevant to your research, please kindly cite our paper:

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


