import networkx as nx
import pandas as pd
import community as community_louvain  # from python-louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt

# Load datasets
users_df = pd.read_csv("users.csv")
logins_df = pd.read_csv("logins.csv")
devices_df = pd.read_csv("devices.csv")
ip_df = pd.read_csv("ip_metadata.csv")

# Initialize the graph
G = nx.Graph()

# Add nodes from users
for uid in users_df['user_id']:
    G.add_node(uid, type='user')

# Add nodes from devices
for did in devices_df['device_id']:
    G.add_node(did, type='device')

# Add nodes from IPs
for ip in ip_df['ip_address']:
    G.add_node(ip, type='ip')

# Add edges from logins
for _, row in logins_df.iterrows():
    user = row['user_id']
    device = row['device_id']
    ip = row['ip_address']
    
    # User ↔ Device
    G.add_edge(user, device, relation='used_device', timestamp=row['timestamp'])
    
    # User ↔ IP
    G.add_edge(user, ip, relation='used_ip', timestamp=row['timestamp'])
    
    # Device ↔ IP
    G.add_edge(device, ip, relation='device_ip', timestamp=row['timestamp'])

print(f"✅ Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

# Subgraph visualization
largest_cc = max(nx.connected_components(G), key=len)
subgraph_nodes = list(largest_cc)[:30]
H = G.subgraph(subgraph_nodes)

color_map = []
for node in H:
    ntype = G.nodes[node]['type']
    if ntype == 'user':
        color_map.append('skyblue')
    elif ntype == 'device':
        color_map.append('orange')
    elif ntype == 'ip':
        color_map.append('lightgreen')

plt.figure(figsize=(14, 10))
nx.draw(H, with_labels=True, node_color=color_map, node_size=500, font_size=8)
plt.title("Connected Subgraph of Digital Identity Graph")
plt.show()

# Centrality
deg_centrality = nx.degree_centrality(G)
top_users = sorted(
    [(node, score) for node, score in deg_centrality.items() if G.nodes[node]['type'] == 'user'],
    key=lambda x: x[1], reverse=True
)[:10]

print("🔍 Top 10 users by degree centrality:")
for user, score in top_users:
    print(f"{user} — centrality: {score:.3f}")

# Louvain communities
partition = community_louvain.best_partition(G)
colors = [partition[node] for node in G.nodes]

plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx_nodes(G, pos, node_size=300, cmap=cm.Set3, node_color=colors)
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.title("Louvain Community Detection")
plt.show()

# Reused entities
ip_usage = logins_df.groupby('ip_address')['user_id'].nunique()
flagged_ips = ip_usage[ip_usage > 5]
print("🚩 IPs shared by >5 users:")
print(flagged_ips)

device_usage = logins_df.groupby('device_id')['user_id'].nunique()
flagged_devices = device_usage[device_usage > 3]
print("\n🚩 Devices shared by >3 users:")
print(flagged_devices)

# ----------------------------------
# 🔐 Trust Score Function
# ----------------------------------
def compute_trust_score(user_id):
    penalty = 0.0

    # IP penalty
    user_ips = logins_df[logins_df['user_id'] == user_id]['ip_address'].unique()
    for ip in user_ips:
        if ip in flagged_ips.index:
            penalty += 0.3

    # Device penalty
    user_devices = logins_df[logins_df['user_id'] == user_id]['device_id'].unique()
    for device in user_devices:
        if device in flagged_devices.index:
            penalty += 0.3

    # Community diversity penalty
    community_id = partition.get(user_id)
    if community_id is not None:
        members = [n for n in partition if partition[n] == community_id and G.nodes[n]['type'] == 'user']
        unique_ips = set(logins_df[logins_df['user_id'].isin(members)]['ip_address'])
        unique_devices = set(logins_df[logins_df['user_id'].isin(members)]['device_id'])
        if len(unique_ips) <= 1 or len(unique_devices) <= 1:
            penalty += 0.2

    # Centrality penalty
    if user_id in deg_centrality and deg_centrality[user_id] > 0.05:
        penalty += 0.2

    return max(0.0, 1.0 - penalty)

# ----------------------------------
# 🔍 Test: Display trust scores
# ----------------------------------
print("\n🧪 Trust scores for 10 users:")
for uid in users_df['user_id'].head(10):
    score = compute_trust_score(uid)
    status = "⚠️ RISK" if score < 0.5 else "✅ OK"
    print(f"{uid}: {score:.2f} {status}")
