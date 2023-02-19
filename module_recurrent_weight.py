import numpy as np
from matplotlib import gridspec
import matplotlib.pyplot as plt
import os
import module_utility


# generate w weight
import numpy as np
import matplotlib.pyplot as plt
# planar wave for test
def gen_2d_wave(local_angle, cur_scale, loc_x, loc_y, n):
    resolution = 1
    amplitude = 1/3
    x = np.arange(0, n, resolution) - loc_x  # (loc_x / n) * cur_scale
    y = np.arange(0, n, resolution) - loc_y  # (loc_y / n) * cur_scale
    [xx, yy] = np.meshgrid(x, y)
    kx = np.cos(local_angle * np.pi / 180)
    ky = np.sin(local_angle * np.pi / 180)
    # w = 2 * np.pi / (np.sin(np.pi/3) * cur_scale)
    w = 2 * np.pi / (cur_scale)
    gradient_map = w * (kx * xx + ky * yy)
    plane_wave = amplitude * (np.cos(gradient_map))
    return plane_wave, gradient_map, w

import numpy as np
n = 200
# np.array([11, 15, 22, 30])
# for ith_scale in np.round(np.array([10, 14, 20, 28])*n/45).astype(int):
for ith_scale in np.round(np.array([20]) * n / 45).astype(int):
    cur_scale = ith_scale
    out_path = '/Users/bo/Desktop/weights_w/'
    w_matrix_store = np.zeros((n, n, n * n))
    counter = 0
    for loc_x in list(range(0, n)):
        for loc_y in list(range(0, n)):
            w_matrix = np.zeros((n, n))
            for local_angle in list(range(0, 360)):
                plane_wave, gradient_map, w = gen_2d_wave(local_angle, cur_scale, loc_y, loc_x, n)
                w_matrix = w_matrix + plane_wave
            w_matrix = w_matrix / len(list(range(0, 360)))
            w_matrix_store[..., counter] = w_matrix
            # if not os.path.isdir(out_path+'w_size'+str(n)+'_scale'+str(cur_scale)):
            #     os.mkdir(out_path+'w_size'+str(n)+'_scale'+str(cur_scale))
            # plt.close('all')
            # plt.figure(dpi=100)
            # plt.imshow(w_matrix, cmap='jet')
            # plt.show()
            # plt.savefig(out_path + 'w_size'+str(n)+'_scale'+str(cur_scale)+'/counter'+str(counter)+'_loc' + str(loc_x) + '-' + str(loc_y) + '.jpg')
            print('loc_x' + str(loc_x) + ' ' + 'loc_y' + str(loc_y))
            counter = counter + 1
    np.save('/Users/bo/Desktop/weights_w/w_size' + str(n) + '_scale' + str(ith_scale) + '.npy', w_matrix_store)


