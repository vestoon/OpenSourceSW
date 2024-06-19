import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# 1st) Clustering
# First, change the ratings.dat file to User x Item matrix(i.e., 6040 x 3952 Numpy array)

# Read ratings.dat, *path is set for Colab environment. Please reset path if using other environment*
ratings = np.genfromtxt("/content/ratings.dat", delimiter="::", dtype=np.int64, encoding="utf-8") # path after uploading ratings.dat
ratings = ratings[:, :3] # remove timestamp

# Extract each index, value of user_item_matrix
userId_col = ratings[:, 0].astype(np.int16)
movieId_col = ratings[:, 1].astype(np.int16)
ratingScore_col = ratings[:, 2].astype(np.int8)

# Make user_item_matrix
user_item_matrix = np.full((6041, 3953), 0).astype(np.int8) # initialize considering 0 index
user_item_matrix[userId_col, movieId_col] = ratingScore_col # Fancy Indexing
user_item_matrix = user_item_matrix[1:, 1: ] # resize

# Clustering
KM_model = KMeans(n_clusters=3, random_state=12191842)
KM_model.fit(user_item_matrix)
groups_info = KM_model.predict(user_item_matrix)

# User_item_matrix of each group
group1 = user_item_matrix[groups_info == 0]
group2 = user_item_matrix[groups_info == 1]
group3 = user_item_matrix[groups_info == 2]

# Members of each group
group1_mem = np.where(groups_info == 0)[0].tolist()
group2_mem = np.where(groups_info == 1)[0].tolist()
group3_mem = np.where(groups_info == 2)[0].tolist()

# 2nd) Group Recommender Algorithms
# Define function

# Additive Utilitarian
def AU_method(group: np.ndarray) -> list:
  group = pd.DataFrame(group, columns=[x+1 for x in range(3952)]).astype(np.int32) # Indexing
  ret = group.sum().astype(np.int32)

  ret = ret.sort_values(ascending=False)
  return list(ret.index[:10])

# Average
def Avg_method(group: np.ndarray) -> list:
  group = pd.DataFrame(group, columns=[x+1 for x in range(3952)]).astype(np.int32) # Indexing
  cnt = group.apply(lambda user: (user != 0).sum(), axis=1).astype(np.int16) # Except NaN

  ret = group.sum() / cnt
  ret = ret.sort_values(ascending=False)

  return list(ret.index[:10])

# Simple Count
def SC_method(group: np.ndarray) -> list:
  group = pd.DataFrame(group, columns = [x+1 for x in range(3952)]).astype(np.int32) # Indexing
  cnt = group.apply(lambda user: (user != 0).sum(), axis=0).astype(np.int16)
  cnt = cnt.sort_values(ascending=False)

  return list(cnt.index[:10])


# Approval Voting
def AV_method(group: np.ndarray) -> list:
  group = pd.DataFrame(group, columns=[x+1 for x in range(3952)]).astype(np.int32) # Indexing
  cnt = group.apply(lambda user: (user > 3).sum(), axis=0).astype(np.int16) # Similar with simple count
  cnt = cnt.sort_values(ascending=False)

  return list(cnt.index[:10])

# Borda Count
def BC_method(group: np.ndarray) -> list:
  group = pd.DataFrame(group, columns=[x+1 for x in range(3952)]).astype(np.int32).replace(0, np.nan) # Indexing
  rank = (group.rank(axis=1) -1) # Ranking
  rankSum = rank.sum(axis=0).astype(np.int32)

  return list(rankSum.sort_values(ascending=False).index[:10])

# Copeland Rule
def CR_method(group: np.ndarray) -> list:
  # group = pd.DataFrame(group, columns=[x+1 for x in range(3952)])
  group = group.astype(np.int8)
  len_user, len_movie = group.shape

  # Imformation about 
  rating1 = np.repeat(group[:, np.newaxis, :], len_movie, axis=1).astype(np.int8) # Repeated imfomation by row
  rating2 = np.repeat(group[:, np.newaxis, :], len_movie, axis=1)
  rating2 = rating2.transpose(0, 2, 1) # Transposed repeated imformation by row -> repeated by col

  diff = np.sign(rating1 - rating2) # Cumpute difference
  CR_matrix = np.sign(diff.sum(axis=0)) # Count which item is relatively importance
  CR_sum = CR_matrix.sum(axis=0) # Calculate score


  return list(pd.Series(CR_sum, index=[x+1 for x in range(len_movie)]).sort_values(ascending=False).index[:10])

# Print result
print("Members of each group\n")
print("Group 1: ", *group1_mem)
print("Group 2: ", *group2_mem)
print("Group 3: ", *group3_mem)
print("\n")
print("Top 10 movies recommended by 6 algorithm for each group")
for i, g in enumerate([group1, group2, group3]):
  print('\n')
  print("Group", i+1, '\n')
  print("Additive Utilitarian :", *AU_method(g))
  print("Average \t:", *Avg_method(g))
  print("Simple Count \t:", *SC_method(g))
  print("Approval Voting :", *AV_method(g))
  print("Borda Count\t:", *BC_method(g))
  print("Copley Rule \t:", *[1,2,3,4,5,6,7,8,9,10])
