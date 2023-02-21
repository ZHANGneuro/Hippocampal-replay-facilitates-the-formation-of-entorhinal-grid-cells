# `I am building the repository now! `<br />


The repository collects the code of python for grid cell simulation and .NET code for virtual navigation simulation in the manuscript entitled "`Hippocampal replay facilitates the formation of entorhinal grid cells`". <br />

bioRxiv link: https://www.biorxiv.org/content/10.1101/2023.02.19.529130v1 <br />

This work shows a significant effect of reversed neuronal replay in facilitating the pattern formation of grid cells for smaller grid scales underlying the computational simulation using spin-glass model (Fuhs and Touretzky, 2006). The finding may suggest the role of reverse replay in constructing a high-resolution cognitive map. <br /><br />


## Python environment for grid cell simulation: <br />
python `3.9.16` <br />
pytorch `1.13.1` <br />
ripser++ `1.1.2` <br />
umap-learn `0.5.3` <br />

## .NET environment for grid cell simulation: <br />
unity `2021.3.18f1` 


## the scripts
In root folder:<br />
`module_spin_class.py` is the function of spin-glass model<br />
`module_recurrent_weight.py` is the function for predefining excitaiton-inhibition weight for multi grid scales<br />
`module_plot_grid_cells.py` is the function for ploting the grid patterns<br />
folder `models` collects the scripts for the analysis mentioned in the manuscript.<br />
folder `module_spin_class.py` collects the .NET script (used for performing virtual navigation in Unity), and prefab of lines (used for highlighting the animal trajectories). 
folder `models` collects the scripts for the analysis mentioned in the manuscript.<br />
prefab of Gorilla was contained by the package `Low Poly Animated Animals` by polyperfect, which could be purchased from Unity Asset Store
prefab of trees, stones, and tree trunks were contained by the package `Free Low Poly Nature Forest` by Pure Poly, which could be obtained for free from Unity Asset Store

<br /><br />

## Formation of grid pattern by spin-glass model <br />
<p align="center">
  <img src="https://github.com/ZHANGneuro/Hippocampal-replay-facilitates-the-formation-of-entorhinal-grid-cells/blob/main/video_1_grid_pattern_git.gif" width="700" height="300" loop=infinite/>
</p>



<br />
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
