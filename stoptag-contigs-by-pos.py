import sys, screed, khmer

'''divides each contig into 10 bins and counts # of stoptags in each bin'''

'''returns closest bin [10,20,30...], 0 will return 10, 11 will return 20'''

def closest(target, collection):
    d_closest = {}
    collection_max = collection[-1]
    if target == 0:
        return collection[0]
    else:
        for i in collection:
            x = float(target)/i
        
            if x > 1:
                continue
            else:
                d_closest[x] = i
                closest_value = max(d_closest.keys())
        return d_closest[closest_value]        

n_bins = 100
K = 32
ht = khmer.new_hashbits(K, 1e8, 1)
ht.load_stop_tags(sys.argv[1])

d_pos = {}
d_norm = {}

for n, record in enumerate(screed.open(sys.argv[2])):
    bin_list = []
    if len(record.sequence) > 500:
        total_kmer_length = len(record.sequence) - K + 1
        binned_length = float(total_kmer_length)/n_bins
        for i in range(1, n_bins + 1):
            bin_list.append(binned_length*i)

        for x in range(total_kmer_length):
            closest_bin_all_kmer = closest(x, bin_list)
            index_kmer = bin_list.index(closest_bin_all_kmer)
            
            d_norm[index_kmer] = d_norm.get(index_kmer,0) + 1

        
        if ht.identify_stoptags_by_position(record.sequence) == []:
            continue
        stoptag_pos_list = ht.identify_stoptags_by_position(record.sequence)
        for x in stoptag_pos_list:
            closest_bin_stoptag = closest(x, bin_list)
            index_kmer = bin_list.index(closest_bin_stoptag)
            d_pos[index_kmer] = d_pos.get(index_kmer,0) + 1


for key in sorted(d_norm.keys()):
    if d_pos.has_key(key):
        print key, d_pos[key], d_norm[key], float(d_pos[key])/d_norm[key]
    else:
        print key, 0, d_norm[key], 0

        
