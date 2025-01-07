# generate w weight

import numpy as np
from matplotlib import gridspec
import matplotlib.pyplot as plt

# space size
n = 45
# output directory
out_path = './weights_w/'
# grid scales
scale_list = np.round(np.array([11, 15, 22, 30])*n/45).astype(int)

# recurrent weight generator
def gen_2d_wave(local_angle, cur_scale, loc_x, loc_y, n):
    resolution = 1
    x = np.arange(0, n, resolution) - loc_x  # (loc_x / n) * cur_scale
    y = np.arange(0, n, resolution) - loc_y  # (loc_y / n) * cur_scale
    [xx, yy] = np.meshgrid(x, y)
    kx = np.cos(local_angle * np.pi / 180)
    ky = np.sin(local_angle * np.pi / 180)
    w = 2 * np.pi / (cur_scale)
    gradient_map = w * (kx * xx + ky * yy)
    plane_wave = 1/3 * (np.cos(gradient_map))
    return plane_wave, gradient_map, w


# plot recurrent weight matrix
cur_scale = scale_list[0]
loc_y = 10
loc_x = 10
w_matrix = np.zeros((n, n))
for local_angle in list(range(0, 360)):
    plane_wave, gradient_map, w = gen_2d_wave(local_angle, cur_scale, loc_y, loc_x, n)
    w_matrix = w_matrix + plane_wave
w_matrix = w_matrix / len(list(range(0, 360)))
plt.close('all')
plt.figure(dpi=100)
plt.imshow(w_matrix, cmap='jet')
plt.show()

# plot line chart of recurrent weight
plt.close('all')
plt.figure(dpi=100)
plt.plot(w_matrix[10, :])
plt.show()

# generate recurrent weight for CAN simulation
for ith_scale in scale_list:
    cur_scale = ith_scale
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
            counter = counter + 1
            # if not os.path.isdir(out_path+'w_size'+str(n)+'_scale'+str(cur_scale)):
            #     os.mkdir(out_path+'w_size'+str(n)+'_scale'+str(cur_scale))
            # plt.close('all')
            # plt.figure(dpi=100)
            # plt.imshow(w_matrix, cmap='jet')
            # plt.show()
            # plt.savefig(out_path + 'w_size'+str(n)+'_scale'+str(cur_scale)+'/counter'+str(counter)+'_loc' + str(loc_x) + '-' + str(loc_y) + '.jpg')
    print(str(ith_scale))
    np.save(out_path + 'w_size' + str(n) + '_scale' + str(ith_scale) + '.npy', w_matrix_store)


#
ith_scale=0
cur_array = np.load(out_path + 'w_size' + str(n) + '_scale' + str(scale_list[ith_scale]) + '.npy')
cur_array = cur_array.reshape(n,n,n,n)
plt.close('all')
fig = plt.figure(figsize=(50, 50))
gs = gridspec.GridSpec(n, n)
gs.update(left=0, right=1, top=1, bottom=0, wspace=0.05, hspace=0.05)
for xx in list(range(0,n)):
    for yy in list(range(0, n)):
        cur_ima = cur_array[:, :, xx, yy]
        ax = fig.add_subplot(gs[xx,yy])
        ax.imshow(cur_ima, cmap='jet')
        ax.axis('off')
plt.show()