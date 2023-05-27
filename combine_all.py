import pyarrow.parquet as pq
import os

# Directory path where the Parquet files are located
directory = 'data/'

# Output file path for the combined Parquet file
output_file = 'combined_all.parquet'

# List to store the Parquet file paths
file_paths = []

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.parquet'):
        file_paths.append(os.path.join(directory, filename))

# # Read and concatenate the Parquet files
# dfs = [pq.read_table(file_path) for file_path in file_paths]
# combined_table = pq.concatenate_tables(dfs)

# # Write the combined Parquet file
# pq.write_table(combined_table, output_file)

with pq.ParquetWriter("output.parquet", schema=pq.ParquetFile(file_paths[0]).schema_arrow) as writer:
    for file in file_paths:
        writer.write_table(pq.read_table(file))
