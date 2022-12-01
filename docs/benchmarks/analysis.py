import json
import matplotlib.pyplot as plt

f = open('benchmarks.json')
benchmarks = json.load(f)
f.close()

make_move_benchmarked_time_results = benchmarks[3]['time_results']

t_array = []

for entry in make_move_benchmarked_time_results:
    t_array.append(entry['extrinsic_time'])

t_avg = sum(t_array) / len(t_array)

fig, ax = plt.subplots()
min_ylim, max_ylim = plt.ylim()

ax.hist(t_array, bins=500, range=(0,t_avg*5))
ax.axvline(t_avg, color='k', linestyle='dashed', linewidth=1, label='Average: {:.2f} ns'.format(t_avg))
ax.axvline(t_avg*3, color='r', linestyle='dashed', linewidth=1, label='3*Average: {:.2f} ns'.format(3*t_avg))
ax.set_xlabel('extrinsic time (ns)')
ax.legend()
plt.show()