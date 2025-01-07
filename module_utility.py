import numpy as np
import scipy
import scipy.signal
import scipy.ndimage as ndimage

def access_grid_orientation(grid_pattern_auto):
    data_size = grid_pattern_auto.shape[0]
    [coor_y_list, coor_x_list] = np.meshgrid(np.arange(0, data_size), np.arange(0, data_size))
    coor_x_list = coor_x_list.reshape(data_size * data_size).astype(float)
    coor_y_list = coor_y_list.reshape(data_size * data_size).astype(float)
    training_path_coors_1d = obtain_path_coor(coor_x_list, coor_y_list, data_size, nb_points=data_size,
                                                                end_loc=[int(np.round(data_size / 2)), int(np.round(data_size / 2))])
    coor_circle_x = np.cos(np.linspace(np.pi / 2, 3 * (np.pi / 2), 180, endpoint=False)) * data_size / 2 * 0.6 + data_size / 2
    coor_circle_x = np.round(coor_circle_x).astype(int)
    coor_circle_y = np.sin(np.linspace(np.pi / 2, 3 * (np.pi / 2), 180, endpoint=False)) * data_size / 2 * 0.6 + data_size / 2
    coor_circle_y = np.round(coor_circle_y).astype(int)
    orientation_path_coor_array = np.zeros((training_path_coors_1d.shape[0], len(coor_circle_x)))
    for ith_circle_loc in list(range(0, len(coor_circle_y))):
        cur_loc_x = coor_circle_x[ith_circle_loc]
        cur_loc_y = coor_circle_y[ith_circle_loc]
        coor_1d = index_2d_to_1d(cur_loc_x, cur_loc_y, data_size)
        orientation_path_coor_array[:, ith_circle_loc] = training_path_coors_1d[:, coor_1d]
    orientation_path_coor_array = orientation_path_coor_array.astype(int)

    amplitude_list = []
    grid_pattern_auto_1d = grid_pattern_auto.reshape(data_size * data_size)
    for ith_ori in list(range(0, np.shape(orientation_path_coor_array)[1])):
        amplitude_list.append(np.sum(grid_pattern_auto_1d[orientation_path_coor_array[:, ith_ori]]))
    amplitude_list = np.array(amplitude_list)

    cur_index = np.where(amplitude_list == np.max(amplitude_list))[0][0]
    # print(np.remainder(cur_index, 60))

    return np.remainder(cur_index, 60), amplitude_list

def edge_function(ith_x_shift, ith_y_shift, grid_ori, cur_scale, n, fillindex, filltype):
    opt_pool = np.zeros((6,2)).astype(int)
    opt1_x = ith_x_shift - np.round(np.sin((grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt1_y = ith_y_shift + np.round(np.cos((grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt2_x = ith_x_shift + np.round(np.sin((grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt2_y = ith_y_shift - np.round(np.cos((grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt3_x = ith_x_shift - np.round(np.cos((90-60-grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt3_y = ith_y_shift + np.round(np.sin((90-60-grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt4_x = ith_x_shift + np.round(np.cos((90-60-grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt4_y = ith_y_shift - np.round(np.sin((90-60-grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt5_x = ith_x_shift - np.round(np.sin((60 - grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt5_y = ith_y_shift - np.round(np.cos((60 - grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt6_x = ith_x_shift + np.round(np.sin((60 - grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt6_y = ith_y_shift + np.round(np.cos((60 - grid_ori) * np.pi / 180) * cur_scale).astype(int)
    opt_pool[0] = [opt1_x, opt1_y]
    opt_pool[1] = [opt2_x, opt2_y]
    opt_pool[2] = [opt3_x, opt3_y]
    opt_pool[3] = [opt4_x, opt4_y]
    opt_pool[4] = [opt5_x, opt5_y]
    opt_pool[5] = [opt6_x, opt6_y]
    indicator = []
    if filltype == 0:
        for ith in list(range(0, opt_pool.shape[0])):
            if (opt_pool[ith][0] < 0 or opt_pool[ith][0] >= n) or (opt_pool[ith][1] < 0 or opt_pool[ith][1] >= n) or (opt_pool[ith][0] == fillindex):
                indicator.append(0)
            else:
                indicator.append(1)
    if filltype == 1:
        for ith in list(range(0, opt_pool.shape[0])):
            if (opt_pool[ith][0] < 0 or opt_pool[ith][0] >= n) or (opt_pool[ith][1] < 0 or opt_pool[ith][1] >= n) or (opt_pool[ith][1] == fillindex):
                indicator.append(0)
            else:
                indicator.append(1)
    indicator = np.array(indicator)
    index = np.where(indicator==1)[0][0]
    return indicator, opt_pool, index

def periodic_boundary(loc_shift, grid_pattern, grid_ori, n, cur_scale):
    [yy, xx] = np.meshgrid(np.array(list(range(0, n))), np.array(list(range(0, n))))
    step_size_x = np.abs(loc_shift[0])
    step_size_y = np.abs(loc_shift[1])
    shift_x = xx - loc_shift[0]
    shift_y = yy - loc_shift[1]

    #  shift along x
    grid_pattern = grid_pattern[np.remainder(shift_x, n), yy]
    if loc_shift[0] < 0:
        shift_x_blank_coor = np.where(np.remainder(shift_x, n) < step_size_x)
        grid_pattern[shift_x_blank_coor[0], shift_x_blank_coor[1]] = 0
        for ith_x_shift in n-1-np.flip(range(0, step_size_x)):
            for ith_y_shift in list(range(0,n)):
                fillindex = ith_x_shift
                filltype = 0
                indicator, pos_pool, index = edge_function(ith_x_shift, ith_y_shift, grid_ori, cur_scale, n, fillindex, filltype)
                grid_pattern[ith_x_shift, ith_y_shift] = grid_pattern[pos_pool[index][0], pos_pool[index][1]]
    if loc_shift[0] > 0:
        shift_x_blank_coor = np.where(np.remainder(shift_x, n) >= n - step_size_x)
        grid_pattern[shift_x_blank_coor[0], shift_x_blank_coor[1]] = 0
        for ith_x_shift in np.flip(range(0, step_size_x)):
            for ith_y_shift in list(range(0,n)):
                fillindex = ith_x_shift
                filltype = 0
                indicator, pos_pool, index = edge_function(ith_x_shift, ith_y_shift, grid_ori, cur_scale, n, fillindex, filltype)
                grid_pattern[ith_x_shift, ith_y_shift] = grid_pattern[pos_pool[index][0], pos_pool[index][1]]

    #  shift along y
    grid_pattern = grid_pattern[xx, np.remainder(shift_y, n)]
    if loc_shift[1] < 0:
        shift_y_blank_coor = np.where(np.remainder(shift_y, n) < step_size_y)
        grid_pattern[shift_y_blank_coor[0], shift_y_blank_coor[1]] = 0
        for ith_y_shift in n-1-np.flip(range(0, step_size_y)):
            for ith_x_shift in list(range(0,n)):
                fillindex = ith_y_shift
                filltype = 1
                indicator, pos_pool, index = edge_function(ith_x_shift, ith_y_shift, grid_ori, cur_scale, n, fillindex, filltype)
                grid_pattern[ith_x_shift, ith_y_shift] = grid_pattern[pos_pool[index][0], pos_pool[index][1]]
    if loc_shift[1] > 0:
        shift_y_blank_coor = np.where(np.remainder(shift_y, n) >= n - step_size_y)
        grid_pattern[shift_y_blank_coor[0], shift_y_blank_coor[1]] = 0
        for ith_y_shift in np.flip(range(0, step_size_y)):
            for ith_x_shift in list(range(0,n)):
                fillindex = ith_y_shift
                filltype = 1
                indicator, pos_pool, index = edge_function(ith_x_shift, ith_y_shift, grid_ori, cur_scale, n, fillindex, filltype)
                grid_pattern[ith_x_shift, ith_y_shift] = grid_pattern[pos_pool[index][0], pos_pool[index][1]]
    return grid_pattern


def no_periodic_boundary(loc_shift, grid_cell_ensemble, n, scale_list, train_type):
    [yy, xx] = np.meshgrid(np.array(list(range(0, n))), np.array(list(range(0, n))))
    step_size_x = np.abs(loc_shift[0])
    step_size_y = np.abs(loc_shift[1])
    shift_x = xx - loc_shift[0]
    shift_y = yy - loc_shift[1]

    if train_type == 'singleScaleAndNeuron':
        grid_cell_ensemble = grid_cell_ensemble.reshape(n, n)
        grid_cell_ensemble = grid_cell_ensemble[np.remainder(shift_x, n), np.remainder(shift_y, n)]
        if loc_shift[0] < 0:
            shift_x_blank_coor = np.where(np.remainder(shift_x, n) < step_size_x)
            grid_cell_ensemble[shift_x_blank_coor[0], shift_x_blank_coor[1]] = 0
        if loc_shift[0] > 0:
            shift_x_blank_coor = np.where(np.remainder(shift_x, n) >= n-step_size_x)
            grid_cell_ensemble[shift_x_blank_coor[0], shift_x_blank_coor[1]] = 0
        if loc_shift[1] < 0:
            shift_y_blank_coor = np.where(np.remainder(shift_y, n) < step_size_y)
            grid_cell_ensemble[shift_y_blank_coor[0], shift_y_blank_coor[1]] = 0
        if loc_shift[1] > 0:
            shift_y_blank_coor = np.where(np.remainder(shift_y, n) >= n-step_size_y)
            grid_cell_ensemble[shift_y_blank_coor[0], shift_y_blank_coor[1]] = 0
        grid_cell_ensemble = grid_cell_ensemble.reshape(n * n)

    if train_type == 'multiscale':
        grid_cell_ensemble = grid_cell_ensemble.reshape(len(scale_list), n, n)
        grid_cell_ensemble = grid_cell_ensemble[:, np.remainder(shift_x, n), np.remainder(shift_y, n)]
        if loc_shift[0] < 0:
            shift_x_blank_coor = np.where(np.remainder(shift_x, n) < step_size_x)
            grid_cell_ensemble[:, shift_x_blank_coor[0], shift_x_blank_coor[1]] = 0
        if loc_shift[0] > 0:
            shift_x_blank_coor = np.where(np.remainder(shift_x, n) >= n-step_size_x)
            grid_cell_ensemble[:, shift_x_blank_coor[0], shift_x_blank_coor[1]] = 0
        if loc_shift[1] < 0:
            shift_y_blank_coor = np.where(np.remainder(shift_y, n) < step_size_y)
            grid_cell_ensemble[:, shift_y_blank_coor[0], shift_y_blank_coor[1]] = 0
        if loc_shift[1] > 0:
            shift_y_blank_coor = np.where(np.remainder(shift_y, n) >= n-step_size_y)
            grid_cell_ensemble[:, shift_y_blank_coor[0], shift_y_blank_coor[1]] = 0
        grid_cell_ensemble = grid_cell_ensemble.reshape(len(scale_list), n * n)

    if train_type == 'population':
        grid_cell_ensemble = grid_cell_ensemble.reshape(len(scale_list), n, n, n * n)
        grid_cell_ensemble = grid_cell_ensemble[:, np.remainder(shift_x, n), np.remainder(shift_y, n), :]
        if loc_shift[0] < 0:
            shift_x_blank_coor = np.where(np.remainder(shift_x, n) < step_size_x)
            grid_cell_ensemble[:, shift_x_blank_coor[0], shift_x_blank_coor[1], :] = 0
        if loc_shift[0] > 0:
            shift_x_blank_coor = np.where(np.remainder(shift_x, n) >= n-step_size_x)
            grid_cell_ensemble[:, shift_x_blank_coor[0], shift_x_blank_coor[1], :] = 0
        if loc_shift[1] < 0:
            shift_y_blank_coor = np.where(np.remainder(shift_y, n) < step_size_y)
            grid_cell_ensemble[:, shift_y_blank_coor[0], shift_y_blank_coor[1], :] = 0
        if loc_shift[1] > 0:
            shift_y_blank_coor = np.where(np.remainder(shift_y, n) >= n-step_size_y)
            grid_cell_ensemble[:, shift_y_blank_coor[0], shift_y_blank_coor[1], :] = 0
        grid_cell_ensemble = grid_cell_ensemble.reshape(len(scale_list), n * n, n * n)
    return grid_cell_ensemble



angles = [30, 60, 90, 120, 150]
def gridscore(sac):
    rotated_matrix = rotated_sacs(sac, angles)
    masks_parameters = zip([0.2] * 10, np.linspace(0.4, 1.0, num=10))
    masks = [(get_ring_mask(sac, mask_min, mask_max), (mask_min, mask_max)) for mask_min, mask_max in masks_parameters]
    scores = [get_grid_scores_for_mask(sac, rotated_matrix, mask) for mask, mask_params in masks]
    cores_60, variances = map(np.asarray, zip(*scores))  # pylint: disable=unused-variable
    max_60_ind = np.argmax(cores_60)
    autocorr_value = np.round(cores_60[max_60_ind], 2)
    return sac, autocorr_value

def rotated_sacs(sac, angles):
    return [scipy.ndimage.rotate(sac, angle, reshape=False) for angle in angles]

def get_ring_mask(sac, mask_min, mask_max, size_sac):
    n_points = [sac.shape[0], sac.shape[1]]
    return (circle_mask(n_points, mask_max * size_sac/2) * (1 - circle_mask(n_points, mask_min * size_sac/2)))

def circle_mask(size, radius, in_val=1.0, out_val=0.0):
    """Calculating the grid scores with different radius."""
    import math
    sz = [math.floor(size[0] / 2), math.floor(size[1] / 2)]
    x = np.linspace(-sz[0], sz[1], size[1])
    x = np.expand_dims(x, 0)
    x = x.repeat(size[0], 0)
    y = np.linspace(-sz[0], sz[1], size[1])
    y = np.expand_dims(y, 1)
    y = y.repeat(size[1], 1)
    z = np.sqrt(x**2 + y**2)
    z = np.less_equal(z, radius)
    vfunc = np.vectorize(lambda b: b and in_val or out_val)
    return vfunc(z)

def get_grid_scores_for_mask(sac, rotated_sacs, mask):
    """Calculate Pearson correlations of area inside mask at corr_angles."""
    masked_sac = sac * mask
    ring_area = np.sum(mask)
    # Calculate dc on the ring area
    masked_sac_mean = np.sum(masked_sac) / ring_area
    # Center the sac values inside the ring
    masked_sac_centered = (masked_sac - masked_sac_mean) * mask
    variance = np.sum(masked_sac_centered**2) / ring_area + 1e-5
    corrs = dict()
    for angle, rotated_sac in zip(angles, rotated_sacs):
        masked_rotated_sac = (rotated_sac - masked_sac_mean) * mask
        cross_prod = np.sum(masked_sac_centered * masked_rotated_sac) / ring_area
        corrs[angle] = cross_prod / variance
    return grid_score_60(corrs)

def grid_score_60(corr, min_max=True):
    if min_max:
        return np.minimum(corr[60], corr[120]) - np.maximum(
            corr[30], np.maximum(corr[90], corr[150]))
    else:
        return (corr[60] + corr[120]) / 2 - (corr[30] + corr[90] + corr[150]) / 3

def calculate_sac(seq1):
    """Calculating spatial autocorrelogram."""
    seq2 = seq1

    def filter2(b, x):
        stencil = np.rot90(b, 2)
        return scipy.signal.convolve2d(x, stencil, mode='full')

    seq1 = np.nan_to_num(seq1)
    seq2 = np.nan_to_num(seq2)

    ones_seq1 = np.ones(seq1.shape)
    ones_seq1[np.isnan(seq1)] = 0
    ones_seq2 = np.ones(seq2.shape)
    ones_seq2[np.isnan(seq2)] = 0

    seq1[np.isnan(seq1)] = 0
    seq2[np.isnan(seq2)] = 0

    seq1_sq = np.square(seq1)
    seq2_sq = np.square(seq2)

    seq1_x_seq2 = filter2(seq1, seq2)
    sum_seq1 = filter2(seq1, ones_seq2)
    sum_seq2 = filter2(ones_seq1, seq2)
    sum_seq1_sq = filter2(seq1_sq, ones_seq2)
    sum_seq2_sq = filter2(ones_seq1, seq2_sq)
    n_bins = filter2(ones_seq1, ones_seq2)
    n_bins_sq = np.square(n_bins)

    std_seq1 = np.power(
        np.subtract(np.divide(sum_seq1_sq, n_bins), (np.divide(np.square(sum_seq1), n_bins_sq))), 0.5)
    std_seq2 = np.power(
        np.subtract(np.divide(sum_seq2_sq, n_bins),(np.divide(np.square(sum_seq2), n_bins_sq))), 0.5)
    multiply_stdseq12 = np.multiply(std_seq1, std_seq2)
    multiply_stdseq12[np.where(multiply_stdseq12==0)] = np.nan

    covar = np.subtract(
        np.divide(seq1_x_seq2, n_bins),
        np.divide(np.multiply(sum_seq1, sum_seq2), n_bins_sq))

    x_coef = np.divide(covar, multiply_stdseq12)
    x_coef = np.real(x_coef)
    x_coef = np.nan_to_num(x_coef)
    x_coef[x_coef < -1e100] = 0
    x_coef[x_coef > 1e100] = 0
    return x_coef


def compute_mean_angle(angle_vector):
    x = y = 0
    for ith_ori in list(range(0, len(angle_vector))):
        cur_ori = angle_vector[ith_ori]
        x += np.cos(cur_ori*np.pi/180)
        y += np.sin(cur_ori*np.pi/180)
        mean_angle = np.round(np.remainder(np.arctan2(y, x) * 180/np.pi, 360))
    return mean_angle

def index_1d_to_2d(index_1d, n):
    return np.array([int(index_1d / n), int(index_1d % n)])

def index_2d_to_1d(x, y, n):
    return x * n + y

def intermediates(p1, p2, nb_points, n):
    x_spacing = (p2[0] - p1[0]) / (nb_points + 1)
    y_spacing = (p2[1] - p1[1]) / (nb_points + 1)
    out_x = np.array([p1[0] + i * x_spacing for i in range(1, nb_points + 1)])
    out_y = np.array([p1[1] + i * y_spacing for i in range(1, nb_points + 1)])
    out_x = out_x.astype(int)
    out_y = out_y.astype(int)
    path_index_1d = index_2d_to_1d(out_x, out_y, n)
    return path_index_1d


def obtain_path_coor(coor_x_list, coor_y_list, n, nb_points, end_loc):
    coor_x = coor_x_list.copy()
    coor_y = coor_y_list.copy()
    middle_point_value = int(n / 2)
    middle_point_index = index_2d_to_1d(middle_point_value, middle_point_value, n)

    horiz_index = np.where(coor_x == middle_point_value)[0]
    verti_index = np.where(coor_y == middle_point_value)[0]
    horiz_xy_index = np.concatenate((horiz_index, verti_index))
    coor_x[horiz_xy_index] = np.nan
    coor_y[horiz_xy_index] = np.nan
    horiz_index = np.delete(horiz_index, np.where(horiz_index == middle_point_index)[0])
    verti_index = np.delete(verti_index, np.where(verti_index == middle_point_index)[0])

    end_x = end_loc[0]
    end_y = end_loc[1]
    diff_in_y = end_y - coor_y
    diff_in_x = end_x - coor_x
    slope = diff_in_y / diff_in_x
    inter = end_y - slope * end_x
    index_slope_p1 = index_2d_to_1d(np.flip(np.arange(0, n)), np.arange(0, n), nb_points)
    index_slope_m1 = index_2d_to_1d(np.arange(0, n), np.arange(0, n), nb_points)
    slope[np.concatenate((index_slope_p1, index_slope_m1))] = np.nan
    inter[np.concatenate((index_slope_p1, index_slope_m1))] = np.nan
    index_slope_p1 = np.delete(index_slope_p1, np.where(index_slope_p1 == middle_point_index)[0])
    index_slope_m1 = np.delete(index_slope_m1, np.where(index_slope_m1 == middle_point_index)[0])

    # for x varies
    x_ylower = np.array([(0 - inter) / slope])[0]
    index_x_ylower = np.where((x_ylower >= 0) & (x_ylower < n))[0]
    effi_x_ylower = np.round(x_ylower[index_x_ylower]).astype(int)
    effi_x_yhigher = n - 1 - effi_x_ylower
    part1_coor = intermediates(p1=np.array([effi_x_ylower, np.array([0] * len(effi_x_ylower))]),
                               p2=np.array([effi_x_yhigher, np.array([n] * len(effi_x_yhigher))]), nb_points=nb_points,
                               n=n)

    # for y varies
    y_x_lower = np.array([0 * slope + inter])[0]
    index_y_xlower = np.where((y_x_lower >= 0) & (y_x_lower < n))[0]
    effi_y_xlower = np.round(y_x_lower[index_y_xlower]).astype(int)
    effi_y_xhigher = n - 1 - effi_y_xlower
    part2_coor = intermediates(p1=np.array([np.array([0] * len(effi_y_xlower)), effi_y_xlower]),
                               p2=np.array([np.array([n] * len(effi_y_xhigher)), effi_y_xhigher]), nb_points=nb_points,
                               n=n)

    # for slope p1
    part3_coor = intermediates(p1=np.array([np.array([n] * len(index_slope_p1)), np.array([0] * len(index_slope_p1))]),
                               p2=np.array([np.array([0] * len(index_slope_p1)), np.array([n] * len(index_slope_p1))]),
                               nb_points=nb_points, n=n)
    # for slope m1
    part4_coor = intermediates(p1=np.array([np.array([0] * len(index_slope_m1)), np.array([0] * len(index_slope_m1))]),
                               p2=np.array([np.array([n] * len(index_slope_m1)), np.array([n] * len(index_slope_m1))]),
                               nb_points=nb_points, n=n)
    # for horiz
    part5_coor = intermediates(p1=np.array([np.array([n / 2] * len(horiz_index)), np.array([0] * len(horiz_index))]),
                               p2=np.array([np.array([n / 2] * len(horiz_index)), np.array([n] * len(horiz_index))]),
                               nb_points=nb_points, n=n)
    # for verti
    part6_coor = intermediates(p1=np.array([np.array([0] * len(verti_index)), np.array([n / 2] * len(verti_index))]),
                               p2=np.array([np.array([n] * len(verti_index)), np.array([n / 2] * len(verti_index))]),
                               nb_points=nb_points, n=n)

    # print(str(np.shape(part1_coor)[1]) + '-' + str(np.shape(part2_coor)[1]) + '-' + str(
    #     np.shape(part3_coor)[1]) + '-' + str(np.shape(part4_coor)[1]) + '-' + str(np.shape(part5_coor)[1]) + '-' + str(
    #     np.shape(part6_coor)[1]))
    # print(np.shape(part1_coor)[1] + np.shape(part2_coor)[1] + np.shape(part3_coor)[1] + np.shape(part4_coor)[1] +
    #       np.shape(part5_coor)[1] + np.shape(part6_coor)[1])

    # path_index_2d = np.zeros((n * n, n * n)).astype(int)
    # path_index_2d[part1_coor, index_x_ylower] = 1
    # path_index_2d[part2_coor, index_y_xlower] = 1
    # path_index_2d[part3_coor, index_slope_p1] = 1
    # path_index_2d[part4_coor, index_slope_m1] = 1
    # path_index_2d[part5_coor, horiz_index] = 1
    # path_index_2d[part6_coor, verti_index] = 1
    path_index_2d = np.zeros((nb_points, n * n)).astype(int)
    path_index_2d[:, index_x_ylower] = part1_coor
    path_index_2d[:, index_y_xlower] = part2_coor
    path_index_2d[:, index_slope_p1] = part3_coor
    path_index_2d[:, index_slope_m1] = part4_coor
    path_index_2d[:, horiz_index] = part5_coor
    path_index_2d[:, verti_index] = part6_coor
    return path_index_2d
