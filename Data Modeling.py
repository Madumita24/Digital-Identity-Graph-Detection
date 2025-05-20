import pandas as pd

# Load datasets
users_df = pd.read_csv("users.csv")
logins_df = pd.read_csv("logins.csv")
devices_df = pd.read_csv("devices.csv")
ip_df = pd.read_csv("ip_metadata.csv")

# Show basic info
print("Users:")
print(users_df.head(), "\n")

print("Logins:")
print(logins_df.head(), "\n")

print("Devices:")
print(devices_df.head(), "\n")

print("IP Metadata:")
print(ip_df.head(), "\n")

# Optional: Check for missing values
print("Missing values:")
print("Users:", users_df.isnull().sum())
print("Logins:", logins_df.isnull().sum())
print("Devices:", devices_df.isnull().sum())
print("IPs:", ip_df.isnull().sum())
