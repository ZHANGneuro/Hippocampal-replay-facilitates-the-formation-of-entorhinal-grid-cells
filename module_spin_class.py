import numpy as np
import torch as pt

def spin_class_module(grid_cell_ensemble, w_matrix, n, thres_precent, train_type):
    grid_cell_ensemble_cuda = pt.from_numpy(grid_cell_ensemble)
    w_matrix_cuda = pt.from_numpy(w_matrix)

    if train_type == 'single_neuron_4_scales':
        signma_w = pt.zeros(grid_cell_ensemble_cuda.size()[0], n * n)
        for ith_scale in list(range(0, grid_cell_ensemble_cuda.size()[0])):
            threshold = pt.max(grid_cell_ensemble_cuda[ith_scale]) * thres_precent
            loc_index_higher_thres = (grid_cell_ensemble_cuda[ith_scale,:] > threshold).nonzero()
            signma_w[ith_scale, ...] = pt.sum( pt.mul(w_matrix_cuda[ith_scale, loc_index_higher_thres[:,0], :],
                               pt.sqrt(grid_cell_ensemble_cuda[ith_scale, loc_index_higher_thres[:,0]])[:,None]), dim=0)
        grid_cell_ensemble_cuda = grid_cell_ensemble_cuda + 0.1 * (
                    -grid_cell_ensemble_cuda + signma_w * (signma_w > 0.) * 1)  # * (signma_w > 0.) * 1
        grid_cell_ensemble = grid_cell_ensemble_cuda.cpu().numpy()

    if train_type == 'single_neuron_1_scale':
        threshold = pt.max(grid_cell_ensemble_cuda) * thres_precent
        loc_index_higher_thres = (grid_cell_ensemble_cuda > threshold).nonzero()
        signma_w = pt.sum( pt.mul(w_matrix_cuda[loc_index_higher_thres[:,0], :], pt.sqrt(grid_cell_ensemble_cuda[loc_index_higher_thres[:,0]])[:, None]), dim=0)
        grid_cell_ensemble_cuda = grid_cell_ensemble_cuda + 0.1 * (
                    -grid_cell_ensemble_cuda + signma_w * (signma_w > 0.) * 1)  # * (signma_w > 0.) * 1
        grid_cell_ensemble = grid_cell_ensemble_cuda.cpu().numpy()

    if  train_type == 'population':
        signma_w = pt.zeros(grid_cell_ensemble_cuda.size()[0], n * n, n * n)
        for ith_scale in list(range(0, grid_cell_ensemble_cuda.size()[0])):
            threshold = pt.max(grid_cell_ensemble_cuda[ith_scale]) * thres_precent
            loc_index_higher_thres = (grid_cell_ensemble_cuda[ith_scale] > threshold).nonzero()
            signma_w[ith_scale, ...] = pt.cat(
                [pt.sum(pt.mul(w_matrix_cuda[ith_scale,
                               loc_index_higher_thres[(loc_index_higher_thres[:, 1] == neuron_j).nonzero()[:, 0], 0], :],
                               pt.sqrt(grid_cell_ensemble_cuda[ith_scale, loc_index_higher_thres[
                                   (loc_index_higher_thres[:, 1] == neuron_j).nonzero()[:, 0], 0], neuron_j])[:,
                               None]), dim=0)[None, :]
                 for neuron_j in pt.arange(0, np.shape(grid_cell_ensemble_cuda)[2])], dim=0)
        grid_cell_ensemble_cuda = grid_cell_ensemble_cuda + 0.1 * (
                    -grid_cell_ensemble_cuda + signma_w * (signma_w > 0.) * 1)  # * (signma_w > 0.) * 1
        grid_cell_ensemble = grid_cell_ensemble_cuda.cpu().numpy()

    return grid_cell_ensemble


