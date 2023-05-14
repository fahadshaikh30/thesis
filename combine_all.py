import pyarrow as pa
import pyarrow.parquet as pq
import os
from tqdm import tqdm

input_folder = "/Users/fahad/Desktop/processed_data"
output_file = "/Users/fahad/Desktop/processed_data/combined_all.parquet"
row_group_chunk_size = 100000  # Adjust this value based on your memory limitations

# Get the list of Parquet files in the input folder
parquet_files = [file for file in os.listdir(input_folder) if file.endswith(".parquet")]

# Initialize the schema variable
schema = None

# Iterate through each Parquet file
for file in parquet_files:
    file_path = os.path.join(input_folder, file)

    # Create a Parquet file reader
    reader = pq.ParquetFile(file_path)

    # Get the schema from the file
    file_schema = reader.schema.to_arrow_schema()  # Convert ParquetSchema to Schema

    # Initialize the schema if not set
    if schema is None:
        schema = file_schema

    # Check if the schemas are compatible
    if not file_schema.equals(schema):
        raise ValueError("Schemas of the Parquet files do not match.")

    # Get the total number of row groups in the file
    num_row_groups = reader.num_row_groups

    # Create a new Parquet file writer
    writer = None

    # Iterate through each row group and write to the output file
    for i in tqdm(range(num_row_groups), f"{file}"):
        # Read the row group into a table
        table = reader.read_row_group(i)

        # Create a new Parquet file writer if not already set
        if writer is None:
            writer = pq.ParquetWriter(output_file, schema)

        # Write the table to the output file
        writer.write_table(table)

        # Flush the writer periodically to disk
        if (i + 1) % row_group_chunk_size == 0:
            writer.close()
            writer = None

    # Close the writer for each file
    if writer is not None:
        writer.close()

print(f"Combined Parquet file saved as '{output_file}'.")
