# ------

# CAN model, reverse replay applied, periodic boundary condition applied

# ------
import numpy as np
import module_plot_grid_cells
import module_utility
import warnings
import os
import torch as pt
import module_spin_class
import random
import time
warnings.filterwarnings("ignore")
mps_device = pt.device("mps")
device = "mps" if pt.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

# output folder name
task_type='original_CAN_reverse_replay_periodic_boundary'

# output directory
fig_export_path = './outputs/' + str(task_type)
if not os.path.isdir(fig_export_path):
    os.makedirs(fig_export_path)

# space size
n = 45

# define start location
loc_center = np.array([int(np.round(n / 2)), int(np.round(n / 2))])

# grid scales
scale_list = np.round(np.array([11, 15, 22, 30])*n/45).astype(int)

# define experience list, 50 experiences, each experience included 8 movements
when_to_pause_list = [10] * 50
random.shuffle(when_to_pause_list)

# define direction list
angles = list(range(0, 180))

# load recurrent weights
w_matrix_multiScale = np.zeros((len(scale_list), n * n, n * n))
for ith_scale in list(range(0, len(scale_list))):
    w_data_cur_scale = np.load(
        './weights_w/w_size' + str(n) + '_scale' + str(scale_list[ith_scale]) + '.npy',
        allow_pickle=True)
    w_matrix_multiScale[ith_scale, ...] = w_data_cur_scale.reshape(n * n, n * n)
w_matrix_multiScale = w_matrix_multiScale * 0.01
w_matrix = w_matrix_multiScale

# initialize hexagonal patterns
grid_cell_multiScale = np.zeros((len(scale_list), n*n))
ith_loc = module_utility.index_2d_to_1d(int(np.round(n / 2)), int(np.round(n / 2)), n)
grid_cell_multiScale[:, ith_loc] = 0.01
grid_cell_ensemble = grid_cell_multiScale

# other parameters
iter_step=0 # timer
spin_time = 3 # number of iteration per movements.
thres_precent = 0 # CAN threshold Ita
step_size = 3 # movement step size

# simulation
for ith_start in list(range(0, len(when_to_pause_list))):
    angle_to_target = random.choice(angles)
    when_to_pause = when_to_pause_list[ith_start]

    for ith_move in list(range(0, when_to_pause)):
        time_start = time.time()
        for ith in list(range(0, spin_time)):
            grid_cell_ensemble = module_spin_class.spin_class_module(grid_cell_ensemble=grid_cell_ensemble,
                                                                           w_matrix=w_matrix, n=n,
                                                                           thres_precent=thres_precent,
                                                                           train_type='single_neuron_4_scales')
        time_end = time.time()
        np.save(
            fig_export_path + '/' + str(task_type) + '_' + str(len(angles)) + 'dir_' + 'step' + str(iter_step) + '.npy',
            grid_cell_ensemble)
        print('iter_step' + str(iter_step) + ' spin-glass time: ' + str(time_end - time_start))
        module_plot_grid_cells.plot(loc_star=loc_center, grid_cell_ensemble=grid_cell_ensemble, n=n,
                                         fig_export_path=fig_export_path, real_step=iter_step, train_type='plot_4_scales',
                                         subject='na', cur_scale='na')

        loc_shift = [int(np.round(np.cos(angle_to_target * np.pi / 180) * step_size)),
                     int(np.round(np.sin(angle_to_target * np.pi / 180) * step_size))]
        grid_cell_ensemble_copy = grid_cell_ensemble.reshape(4, n, n).copy()
        for ith_scale in list(range(0, 4)):
            grid_pattern_auto = module_utility.calculate_sac(grid_cell_ensemble_copy[ith_scale])
            grid_ori, amplitude_list = module_utility.access_grid_orientation(grid_pattern_auto)
            grid_cell_curScale = module_utility.periodic_boundary(loc_shift, grid_cell_ensemble_copy[ith_scale],
                                                                       grid_ori, n, scale_list[ith_scale])
            grid_cell_ensemble[ith_scale, :] = grid_cell_curScale.reshape(n * n)

        iter_step = iter_step + 1

    for ith_back in list(range(0, when_to_pause)):
        time_start = time.time()
        for ith in list(range(0, spin_time)):
            grid_cell_ensemble = module_spin_class.spin_class_module(grid_cell_ensemble=grid_cell_ensemble,
                                                                           w_matrix=w_matrix, n=n,
                                                                           thres_precent=thres_precent,
                                                                           train_type='single_neuron_4_scales')
        time_end = time.time()

        np.save(
            fig_export_path + '/' + str(task_type) + '_' + str(len(angles)) + 'dir_' + 'step' + str(iter_step) + '.npy',
            grid_cell_ensemble)
        print('iter_step' + str(iter_step) + ' spin-glass time: ' + str(time_end - time_start))
        module_plot_grid_cells.plot(loc_star=loc_center, grid_cell_ensemble=grid_cell_ensemble, n=n,
                                         fig_export_path=fig_export_path, real_step=iter_step, train_type='plot_4_scales',
                                         subject='na', cur_scale='na')

        loc_shift = [int(np.round(np.cos((angle_to_target+180) * np.pi / 180) * step_size)),
                     int(np.round(np.sin((angle_to_target+180) * np.pi / 180) * step_size))]
        grid_cell_ensemble_copy = grid_cell_ensemble.reshape(4, n, n).copy()
        for ith_scale in list(range(0, 4)):
            grid_pattern_auto = module_utility.calculate_sac(grid_cell_ensemble_copy[ith_scale])
            grid_ori, amplitude_list = module_utility.access_grid_orientation(grid_pattern_auto)
            grid_cell_curScale = module_utility.periodic_boundary(loc_shift, grid_cell_ensemble_copy[ith_scale],
                                                                       grid_ori, n, scale_list[ith_scale])
            grid_cell_ensemble[ith_scale, :] = grid_cell_curScale.reshape(n * n)

        iter_step = iter_step + 1

grid_cell_ensemble = module_spin_class.spin_class_module(grid_cell_ensemble=grid_cell_ensemble,
                                                            w_matrix=w_matrix, n=n,
                                                            thres_precent=thres_precent,
                                                            train_type='single_neuron_4_scales')
module_plot_grid_cells.plot(loc_star=loc_center, grid_cell_ensemble=grid_cell_ensemble, n=n,
                                 fig_export_path=fig_export_path, real_step=iter_step, train_type='plot_4_scales',
                                 subject='na', cur_scale='na')


























