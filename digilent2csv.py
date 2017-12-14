import sys

in_filename = sys.argv[1]
out_filename = sys.argv[2]

print('Transfering from {} to {}...'.format(in_filename, out_filename))

data_index = 1
times = []
values = []

with open(in_filename, 'r') as f:
    for line in f:
        words = line.split()
        try:
            t = int(words[0])
            times.append(t)
            values.append(float(words[data_index]))
        except:
            continue

with open(out_filename, 'w') as f:
    for i in range(len(times)):
        f.write('{},{}\n'.format(times[i], values[i]))

print('Done.')
