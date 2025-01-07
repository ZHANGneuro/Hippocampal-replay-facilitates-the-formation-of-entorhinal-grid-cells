This repository collects the python code for grid cell simulation and .NET code for virtual navigation simulation in the manuscript entitled "`Experience replay facilitates the formation of the hexagonal pattern of grid cells`". <br />

bioRxiv link: https://www.biorxiv.org/content/10.1101/2023.02.19.529130v2 <br />

This work shows a significant effect of place cell reverse replay on the formation of multi-scale hexagonal patterns of grid cells using continuous attractor model (CAN) (Fuhs and Touretzky, 2006). The findings may suggest the potential role of reverse replay in maintaining  periodic representation of space and rapidly constructing a high-resolution cognitive map. <br /><br />

## Python environment for grid cell simulation: <br />
python `3.9.16` <br />
pytorch `1.13.1` <br />
ripser++ `1.1.2` <br />
umap-learn `0.5.3` <br />

## .NET environment for virtual navigation: <br />
unity `2021.3.18f1` 

## codes <br />
scripts in the root folder are as following:
<br />
- `module_spin_class.py` is the function of CAN model<br />
- `module_recurrent_weight.py` is the function for generating recurrent excitaiton-inhibition weight required for CAN simualtion (run this code first) <br />
- `module_plot_grid_cells.py` is the function for ploting the generated hexagonal patterns<br />
- folder `models` includes the scripts for four CAN models as following:
  1. "model_CAN": CAN model, no hippocampal replay, no periodic boundary.
  2. "model_CAN_ReverseReplay": CAN model, reverse replay, no periodic boundary.
  3. "model_CAN_ReverseReplay_periodicBoundary": CAN model, reverse replay, periodic boundary.
- folder `Assets` includes the .NET script (used for performing virtual navigation in Unity), and prefab of lines (used for highlighting the animal trajectories).
  
<br />

## CAN-based simulation of hexagonal pattern of grid cells <br />
<p align="center">
  <img src="https://github.com/ZHANGneuro/Hippocampal-replay-facilitates-the-formation-of-entorhinal-grid-cells/blob/main/video_1_grid_pattern_git.gif" width="700" height="300" loop=infinite/>
</p>

<br />

## Spikes of a grid cell with animal trajectory <br />
The animal trajectory was open-accessed by Hafting et al (2005), link https://www.ntnu.edu/kavli/research/grid-cell-data <br />

<p align="center">
  <img src="https://github.com/ZHANGneuro/Hippocampal-replay-facilitates-the-formation-of-entorhinal-grid-cells/blob/main/video_2_firing_rate_git.gif" width="350" height="350" loop=infinite/>
</p>
<br />

### Reference <br />
Fuhs, M. C., & Touretzky, D. S. (2006). A spin glass model of path integration in rat medial entorhinal cortex. Journal of Neuroscience, 26(16), 4266-4276.

Hafting, T., Fyhn, M., Molden, S., Moser, M. B., & Moser, E. I. (2005). Microstructure of a spatial map in the entorhinal cortex. Nature, 436(7052), 801-806.<br />
