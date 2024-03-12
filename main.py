import pandas as pd
import json
import gzip
import os

# Load files into pandas df's
brands = pd.read_json('brands.json.gz', lines=True)
receipts = pd.read_json('receipts.json.gz', lines=True)
# users = pd.read_json('users.json.gz', lines=True)
# the line above was erroring so I manually unpacked the zipped file
users = pd.read_json('users.json', lines=True)


# Data quality tenants
# completeness, timeliness, validity, accuracy, consistency, uniqueness

# Checking null counts
null_counts = brands.isnull().sum()
print('\n brands null counts')
print(null_counts)
# _id               0
# barcode           0
# category        155
# categoryCode    650
# cpg               0
# name              0
# topBrand        612
# brandCode       234

null_counts = receipts.isnull().sum()
print('\n receipts null counts')
print(null_counts)
# _id                          0
# bonusPointsEarned          575
# bonusPointsEarnedReason    575
# createDate                   0
# dateScanned                  0
# finishedDate               551
# modifyDate                   0
# pointsAwardedDate          582
# pointsEarned               510
# purchaseDate               448
# purchasedItemCount         484
# rewardsReceiptItemList     440
# rewardsReceiptStatus         0
# totalSpent                 435
# userId                       0

null_counts = users.isnull().sum()
print('\n users null counts')
print(null_counts)
# _id              0
# active           0
# createdDate      0
# lastLogin       62
# role             0
# signUpSource    48
# state           56



# Checking for unique values

# Function to check if a value is a dictionary (JSON object)
def is_dict(value):
    return isinstance(value, dict)


# brands
# Iterate through each column and parse JSON if applicable
for column in brands.columns:
    if brands[column].apply(is_dict).all():
        # If all values in the column are dictionaries, convert to DataFrame
        json_brands_df = pd.json_normalize(brands[column])
        # Add a prefix to the column names to avoid potential conflicts
        json_brands_df.columns = [f"{column}_{col}" for col in json_brands_df.columns]
        brands_df = pd.concat([brands.drop(columns=[column]), json_brands_df], axis=1)
        # print(brands_df)

unique_counts = pd.Series()
for column in brands_df.columns:
    if not brands_df[column].apply(is_dict).any():
        unique_counts[column] = brands_df[column].nunique()

# Compute unique counts including the total number of rows
unique_counts = pd.DataFrame(columns=['unique_count', 'duplicate_count', 'total_count'])
for column in brands_df.columns:
    if not brands_df[column].apply(is_dict).any():
        unique_values = brands_df[column].value_counts()
        unique_count = len(unique_values)
        total_count = len(brands_df[column])
        duplicate_count = total_count - unique_count
        unique_counts.loc[column] = [unique_count, duplicate_count, total_count]

# Display the count of unique values in each column
print("Count of unique values and total rows in each column:")
print(unique_counts)

# Check for unique values in each non-dictionary column
for column in brands_df.columns:
    if not brands_df[column].apply(is_dict).any():
        unique_values = brands_df[column].unique()
        print(f"\nUnique values in column '{column}': {unique_values}")



# users
# Iterate through each column and parse JSON if applicable
for column in users.columns:
    if users[column].apply(is_dict).all():
        # If all values in the column are dictionaries, convert to DataFrame
        json_users_df = pd.json_normalize(users[column])
        # Add a prefix to the column names to avoid potential conflicts
        json_users_df.columns = [f"{column}_{col}" for col in json_users_df.columns]
        users_df = pd.concat([users.drop(columns=[column]), json_users_df], axis=1)
        print(users_df)

unique_counts = pd.Series()
for column in users_df.columns:
    if not users_df[column].apply(is_dict).any():
        unique_counts[column] = users_df[column].nunique()

# Compute unique counts including the total number of rows
unique_counts = pd.DataFrame(columns=['unique_count', 'duplicate_count', 'total_count'])
for column in users_df.columns:
    if not users_df[column].apply(is_dict).any():
        unique_values = users_df[column].value_counts()
        unique_count = len(unique_values)
        total_count = len(users_df[column])
        duplicate_count = total_count - unique_count
        unique_counts.loc[column] = [unique_count, duplicate_count, total_count]

# Display the count of unique values in each column
print("Count of unique values and total rows in each column:")
print(unique_counts)

# Check for unique values in each non-dictionary column
for column in users_df.columns:
    if not users_df[column].apply(is_dict).any():
        unique_values = users_df[column].unique()
        print(f"\nUnique values in column '{column}': {unique_values}")




# receipts
# Iterate through each column and parse JSON if applicable
for column in receipts.columns:
    if receipts[column].apply(is_dict).all():
        # If all values in the column are dictionaries, convert to DataFrame
        json_receipts_df = pd.json_normalize(receipts[column])
        # Add a prefix to the column names to avoid potential conflicts
        json_receipts_df.columns = [f"{column}_{col}" for col in json_receipts_df.columns]
        receipts_df = pd.concat([receipts.drop(columns=[column]), json_receipts_df], axis=1)
        # print(receipts_df)


# Filter out missing values in the 'rewardsReceiptItemList' column
filtered_df = receipts_df.dropna(subset=['rewardsReceiptItemList'])
# Expand the 'rewardsReceiptItemList' column into new columns
expanded_df = pd.json_normalize(filtered_df['rewardsReceiptItemList'].explode())
# Combine the expanded DataFrame with the original DataFrame
result_df = pd.concat([filtered_df.drop(columns=['rewardsReceiptItemList', 'pointsEarned']), expanded_df], axis=1)
# print(result_df)


# Compute unique counts including the total number of rows
unique_counts = pd.DataFrame(columns=['unique_count', 'duplicate_count', 'total_count'])
for column in result_df.columns:
    if not result_df[column].apply(is_dict).any():
        unique_values = result_df[column].value_counts()
        unique_count = len(unique_values)
        total_count = len(result_df[column])
        duplicate_count = total_count - unique_count
        unique_counts.loc[column] = [unique_count, duplicate_count, total_count]

# Display the count of unique values in each column
print("Count of unique values and total rows in each column:")
print(unique_counts)

# Check for unique values in each non-dictionary column
for column in result_df.columns:
    if not result_df[column].apply(is_dict).any():
        unique_values = result_df[column].unique()
        # print(f"\nUnique values in column '{column}': {unique_values}")



# freshness
# distribution