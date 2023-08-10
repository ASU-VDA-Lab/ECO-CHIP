# ECO-CHIP

Carbon footprint estimator for heterogenous chiplet-based systems. Integration with cost estimation and NoC modeling.

# Table of Contents

-   FAQs
-   File Structure 
-   Requirments 
-   Commands 


# FAQs


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

# Requirments 

# Commands 
To run ECO-chip for your design, please specify the design of interest to obatin its Carbon Foot Print (CFP) 

```sh
python3 src/ECO_chip.py --design config/design.json
```
