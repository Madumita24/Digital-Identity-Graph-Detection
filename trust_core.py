# trust_core.py

import pandas as pd
import networkx as nx
import community as community_louvain

# Load CSVs
users_df = pd.read_csv("users.csv")
logins_df = pd.read_csv("logins.csv")
devices_df = pd.read_csv("devices.csv")
ip_df = pd.read_csv("ip_metadata.csv")

# Build the graph
G = nx.Graph()
for uid in users_df['user_id']:
    G.add_node(uid, type='user')
for did in devices_df['device_id']:
    G.add_node(did, type='device')
for ip in ip_df['ip_address']:
    G.add_node(ip, type='ip')
for _, row in logins_df.iterrows():
    G.add_edge(row['user_id'], row['device_id'])
    G.add_edge(row['user_id'], row['ip_address'])
    G.add_edge(row['device_id'], row['ip_address'])

# Centrality and Louvain community
deg_centrality = nx.degree_centrality(G)
partition = community_louvain.best_partition(G)

# Flag reused IPs and devices
ip_usage = logins_df.groupby('ip_address')['user_id'].nunique()
flagged_ips = ip_usage[ip_usage > 5]
device_usage = logins_df.groupby('device_id')['user_id'].nunique()
flagged_devices = device_usage[device_usage > 3]

# Trust scoring function
def compute_trust_score(user_id):
    penalty = 0.0

    # IP reuse
    user_ips = logins_df[logins_df['user_id'] == user_id]['ip_address'].unique()
    for ip in user_ips:
        if ip in flagged_ips.index:
            penalty += 0.3

    # Device reuse
    user_devices = logins_df[logins_df['user_id'] == user_id]['device_id'].unique()
    for device in user_devices:
        if device in flagged_devices.index:
            penalty += 0.3

    # Community analysis
    community_id = partition.get(user_id)
    if community_id is not None:
        members = [n for n in partition if partition[n] == community_id and G.nodes[n]['type'] == 'user']
        unique_ips = set(logins_df[logins_df['user_id'].isin(members)]['ip_address'])
        unique_devices = set(logins_df[logins_df['user_id'].isin(members)]['device_id'])
        if len(unique_ips) <= 1 or len(unique_devices) <= 1:
            penalty += 0.2

    # Centrality
    if user_id in deg_centrality and deg_centrality[user_id] > 0.05:
        penalty += 0.2

    return max(0.0, 1.0 - penalty)
