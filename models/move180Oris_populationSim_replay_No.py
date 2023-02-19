import numpy as np
import matplotlib
import module_plot_grid_cells
import module_utility
import warnings
import os
import torch as pt
import module_spin_class
import random
from random import shuffle
import matplotlib.pyplot as plt
from matplotlib import gridspec
import time

warnings.filterwarnings("ignore")
matplotlib.rcParams.update({'font.size': 20})

mps_device = pt.device("mps")
x = pt.zeros(1, device=mps_device)
print(x)
device = "mps" if pt.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

angles_main = np.linspace(0, 360, 8, endpoint=False)
angles_main = np.repeat(angles_main, 2)

for sub in list(range(12, 16)):

    task_type = 'noreplay180_no'

    n = 45
    scale_list = np.round(np.array([11, 15, 22, 30]) * n / 45).astype(int)
    spin_time = 1
    thres_precent = 0
    loc_center = np.array([int(np.round(n / 2)), int(np.round(n / 2))])

    iter_step = 0
    step_size = 3
    when_to_pause_list = [5,10,15] * 40
    random.shuffle(when_to_pause_list)
    cur_main_angle = angles_main[sub]
    angle_offsets = np.linspace(-90, 90, 180, endpoint=False)
    coor_x = [5]
    coor_y = [22]

    w_matrix_multiScale = np.zeros((len(scale_list), n * n, n * n))
    for ith_scale in list(range(0, len(scale_list))):
        w_data_cur_scale = np.load(
            '/Users/bo/Desktop/weights_w/w_size' + str(n) + '_scale' + str(scale_list[ith_scale]) + '.npy',
            allow_pickle=True)
        w_matrix_multiScale[ith_scale, ...] = w_data_cur_scale.reshape(n * n, n * n)
    w_matrix_multiScale = w_matrix_multiScale * 0.01

    # single cell
    grid_cell_multiScale = np.zeros((len(scale_list), n * n))
    ith_loc = module_utility.index_2d_to_1d(int(np.round(n / 2)), int(np.round(n / 2)), n)
    grid_cell_multiScale[:, ith_loc] = 0.01

    fig_export_path = '/Users/bo/Desktop/replay_data/multiSubject_' + str(task_type) + '_' + str(
        len(angle_offsets)) + 'dir_stepsize' + str(step_size)
    if not os.path.isdir(fig_export_path):
        os.makedirs(fig_export_path)

    w_matrix = w_matrix_multiScale
    grid_cell_ensemble = grid_cell_multiScale

    for ith_start in list(range(0, len(when_to_pause_list))):
        angle_to_target = cur_main_angle+random.choice(angle_offsets)
        when_to_pause = when_to_pause_list[ith_start]
        for ith_move in list(range(0, when_to_pause)):
            time_start = time.time()
            grid_cell_ensemble = module_spin_class.spin_class_HD_module(grid_cell_ensemble, w_matrix, n, spin_time,
                                                                           thres_precent, 'single_neuron_4_scales')
            time_end = time.time()
            print('iter_step' + str(iter_step) + ' spin-glass time: ' + str(time_end - time_start))
            np.save(fig_export_path + '/' + str(task_type) + '_' + str(len(angle_offsets)) + 'dir_' + 'step' + str(
                iter_step) + '.npy', grid_cell_ensemble)
            module_plot_grid_cells.plot(loc_star=loc_center, grid_cell_ensemble=grid_cell_ensemble, n=n,
                                        fig_export_path=fig_export_path, real_step=iter_step,
                                        train_type='plot_4_scales',
                                        subject=sub, cur_scale='na')

            loc_shift = [int(np.round(np.cos(angle_to_target * np.pi / 180) * step_size)),
                         int(np.round(np.sin(angle_to_target * np.pi / 180) * step_size))]
            grid_cell_ensemble_copy = grid_cell_ensemble.reshape(4, n, n).copy()
            for ith_scale in list(range(0, 4)):
                grid_pattern_auto = module_utility.calculate_sac(grid_cell_ensemble_copy[ith_scale])
                grid_ori, amplitude_list = module_utility.access_grid_orientation(grid_pattern_auto)
                grid_cell_curScale = module_utility.pick_gridcell_twist(loc_shift,
                                                                           grid_cell_ensemble_copy[ith_scale],
                                                                           grid_ori, n, scale_list[ith_scale])
                grid_cell_ensemble[ith_scale, :] = grid_cell_curScale.reshape(n * n)

            coor_x.append(coor_x[-1] + loc_shift[0])
            coor_y.append(coor_y[-1] + loc_shift[1])
            iter_step = iter_step + 1

    grid_cell_ensemble = module_spin_class.spin_class_HD_module(grid_cell_ensemble, w_matrix, n, spin_time,
                                                                   thres_precent, 'single_neuron_4_scales')
    module_plot_grid_cells.plot(loc_star=loc_center, grid_cell_ensemble=grid_cell_ensemble, n=n,
                                     fig_export_path=fig_export_path, real_step=iter_step, train_type='plot_4_scales',
                                     subject=sub, cur_scale='na')
    np.save(fig_export_path + '/' + str(task_type) + '_' + str(len(angle_offsets)) + 'dir_' + 'step' + str(iter_step) + '.npy',
            grid_cell_ensemble)

    np.save(fig_export_path + '/sub' + str(sub) + '_size' + str(n) + '_coor_' + str(task_type) + '_dir_x.npy', np.array(coor_x))
    np.save(fig_export_path + '/sub' + str(sub) + '_size' + str(n) + '_coor_' + str(task_type) + '_dir_y.npy', np.array(coor_y))





# plt.figure(figsize=(5, 5))
# plt.plot(coor_x, coor_y, c='black')
# plt.axis('off')
# plt.show()


# ## test plots
# plt.close('all')
# plt.figure(figsize=(5, 5))
# plt.imshow(aaa[:,:, 22, 40], cmap='jet')
# # plt.colorbar()
# plt.axis('off')
# plt.show()