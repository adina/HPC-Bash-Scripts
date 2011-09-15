import khmer, sys, screed

K = 32
ht = khmer.new_hashbits(K, 1e8, 1)
ht.load_stop_tags(sys.argv[1])

count = 0

d_pos = {}
d_norm = {}

for n, record in enumerate(screed.open(sys.argv[2])):
    for i in range(len(record.sequence) - 32 + 1):
        d_norm[i] = d_norm.get(i,0) + 1
    if ht.identify_stoptags_by_position(record.sequence) == []:
        continue
    position_list = ht.identify_stoptags_by_position(record.sequence)
    for i in position_list:
        i = int(i)
        d_pos[i] = d_pos.get(i, 0) + 1

for key in sorted(d_norm.keys()):
    if d_pos.has_key(key):
        print key, d_pos[key], d_norm[key], float(d_pos[key])/d_norm[key]
    else:
        print key, 0, d_norm[key], 0
