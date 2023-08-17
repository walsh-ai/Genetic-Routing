import random 
import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt 

# Generate coordinates for n nodes 
# n: Number of nodes 
# scale: Scaling factor for coordinates generated between [0, 1)
def generate_nodes(n, scale):
    return np.random.rand(n, 2) * scale
	
	
# Calculate the straight line distance between coordinates  
#     by applying Pythagoras' theorem (a^2 + b^2 = c^2)
# a: First coordinate pair 
# b: Second coordinate pair 
def pythag(a, b):
    return np.sqrt(np.square(a[0] - b[0]) + np.square(a[1] - b[1]))
	

# Calculate the depth factor (straight line distance in 
# 		2D Euclidean space) between two nodes i, j
def depth_factor(i, j):
    return np.exp(-pythag(i, j))
	

# Calculate the surface factor between two nodes i,j 
def surface_factor(si, sj):
    return (si + sj)
	

# Function nx_log_normal: Produce a random graph with log-normal degree
# distribution 
# Provide the resultant graph as an adjacency matrix 
# Parameters:
# size: The desired network size (number of nodes)
# degree: The desired number of edges between nodes in the network 
def log_normal_adj(size, scale, degree):
    # Generate coordinates 
    nodes = generate_nodes(size, scale)
    
    # Define surface weights for each node
    surfaces = np.random.lognormal(mean = 0.0, sigma = 1.0, size = size)
    
    # Define surface factor between each and every pair of nodes 
    sf = [[surface_factor(i, j) for i in surfaces] for j in surfaces] 
          
    # Define depth factor between each and every pair of nodes 
    df = [[depth_factor(i, j) for i in nodes] for j in nodes]
    
    # Probability factors for each pair of nodes
    ep = np.multiply(df, sf)
    
    # For each pair of nodes
    # Assign edge with probability propotional to the depth factor 
    total_ep = np.sum(ep)
    
    # For each pair of nodes
    # Create an edge with probability proportional to dij 
    adj = np.zeros(shape = (size, size))

    # Roulette wheel 
    while degree > 0:
        prsum = 0.0 
        ptr = random.random() 
        
        for i, j in itertools.product(range(size), range(size)):  
            if i == j:
                continue 
            
            pr = ep[i][j] / total_ep
            prsum += pr 
            
            if prsum > ptr:
                degree = degree - 1
                adj[i, j] = ep[i][j]
                break
        
    return adj
	

# Function nx_log_normal: Produce a random graph with log-normal degree
# distribution 
# Provide the resultant graph as a Networkx object 
# Parameters:
# size: The desired network size (number of nodes)
# degree: The desired number of edges between nodes in the network 
def nx_log_normal(size, degree):
    # Generate coordinates in range [0, 1]
    scale = 1
    nodes = generate_nodes(size, scale)
    
    # Define surface weights for each node 
    surfaces = np.random.lognormal(mean = 0.0, sigma = 1.0, size = size)
    
    # Define the surface factor between every node pair 
    # Larger surfaces have greater probability to connect 
    sf = [[surface_factor(i, j) for i in surfaces] for j in surfaces] 
    
    # Define the depth factor between every pair of nodes 
    # Geometrically closer nodes have higher depth factor 
    df = [[depth_factor(i, j) for i in nodes] for j in nodes]
    
    # Calculate the existence probability for each edge 
    # depth_factor_ij * surface_factor_ij 
    ep = np.multiply(df, sf)
    total_ep = np.sum(ep)
    
    # Roulette wheel 
    # Create an edge (i, j) with Pr. proportional to ep_ij 
    edges_set = []
    
    while degree > 0:
        pr_sum = 0.0 
        ptr = random.random()
        
        for i, j in itertools.product(range(size), range(size)):
                if i == j:
                    continue 
                
                pr = ep[i][j] / total_ep
                pr_sum += pr 
                
                if pr_sum > ptr: 
                    edges_set.append((i, j, {'weight': pr}))
                    break
        
        degree = degree - 1 
    
    G = nx.Graph()
    G.add_nodes_from(range(size))
    G.add_edges_from(edges_set)
    
    return G 