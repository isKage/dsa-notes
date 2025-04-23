from utils import ChainHashMap, ProbeHashMap

print("=" * 15, "Chain Hash Map", "=" * 15)
chain_hash_map = ChainHashMap()
chain_hash_map['A'] = 1
chain_hash_map['B'] = 2
chain_hash_map['C'] = 3
for key in chain_hash_map:
    print("key: {}, value: {}".format(key, chain_hash_map[key]))

print("=" * 15, "Probe Hash Map", "=" * 15)
probe_hash_map = ProbeHashMap()
probe_hash_map['Avail'] = 100
probe_hash_map['Bucket'] = 200
probe_hash_map['Capacity'] = 300
for key in probe_hash_map:
    print("key: {}, value: {}".format(key, probe_hash_map[key]))
