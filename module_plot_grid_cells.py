import matplotlib.pyplot as plt
from matplotlib import gridspec
import module_utility
import scipy.ndimage as ndimage

def plot(loc_star, grid_cell_ensemble, n, fig_export_path, real_step, train_type, subject, cur_scale):

    if train_type == 'plot_1_scale':
        plt.close('all')
        fig = plt.figure(figsize=(8, 8))
        gs = gridspec.GridSpec(1, 1)
        cur_smooth = ndimage.gaussian_filter(grid_cell_ensemble[0, :].reshape(n, n), sigma=(1, 1))
        ax = fig.add_subplot(gs[0, 0])
        ax.axis('off')
        im = ax.imshow(cur_smooth, cmap='jet', origin='upper')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.savefig(fig_export_path + '/real_step' + str(real_step) + '.jpg')


    if train_type == 'plot_4_scales':
        gap = 0.2
        plt.close('all')
        fig = plt.figure(figsize=(11, 11))
        gs = gridspec.GridSpec(2, 2, width_ratios=[5, 5], height_ratios=[5, 5], wspace=gap, hspace=gap)
        gs.update(left=0, right=1, top=1, bottom=0, wspace=gap, hspace=gap)
        ax = fig.add_subplot(gs[0, 0])
        ax.axis('off')
        im = ax.imshow(grid_cell_ensemble[0, :].reshape(n, n), cmap='jet', origin='upper')
        ax = fig.add_subplot(gs[1, 0])
        ax.axis('off')
        im = ax.imshow(grid_cell_ensemble[1, :].reshape(n, n), cmap='jet', origin='upper')
        ax = fig.add_subplot(gs[0, 1])
        ax.axis('off')
        im = ax.imshow(grid_cell_ensemble[2, :].reshape(n, n), cmap='jet', origin='upper')
        ax = fig.add_subplot(gs[1, 1])
        ax.axis('off')
        im = ax.imshow(grid_cell_ensemble[3, :].reshape(n, n), cmap='jet', origin='upper')
        plt.savefig(fig_export_path + '/plot_grid_step' + str(real_step) + '.jpg')


    if train_type == 'plot_population':
        gap = 0.2
        plt.close('all')
        fig = plt.figure(figsize=(11, 11))
        gs = gridspec.GridSpec(2, 2, width_ratios=[5, 5], height_ratios=[5, 5], wspace=gap, hspace=gap)

        ax = fig.add_subplot(gs[0, 0])
        ax.axis('off')
        im = ax.imshow(grid_cell_ensemble[0, :, module_utility.index_2d_to_1d(loc_star[0], loc_star[1], n)].reshape(n, n), cmap='jet', origin='upper')
        # plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        # ax.set_title('Scale'+str(scale_list[0]))

        ax = fig.add_subplot(gs[1, 0])
        ax.axis('off')
        im = ax.imshow(grid_cell_ensemble[1, :, module_utility.index_2d_to_1d(loc_star[0], loc_star[1], n)].reshape(n, n), cmap='jet', origin='upper')
        # plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        # ax.set_title('Scale' + str(scale_list[1]))

        ax = fig.add_subplot(gs[0, 1])
        ax.axis('off')
        im = ax.imshow(grid_cell_ensemble[2, :, module_utility.index_2d_to_1d(loc_star[0], loc_star[1], n)].reshape(n, n), cmap='jet', origin='upper')
        # plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        # ax.set_title('Scale' + str(scale_list[2]))

        ax = fig.add_subplot(gs[1, 1])
        ax.axis('off')
        im = ax.imshow(grid_cell_ensemble[3, :, module_utility.index_2d_to_1d(loc_star[0], loc_star[1], n)].reshape(n, n), cmap='jet', origin='upper')
        # plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        # ax.set_title('Scale' + str(scale_list[3]))

        plt.savefig(fig_export_path + '/real_step' + str(real_step) + '.jpg')




