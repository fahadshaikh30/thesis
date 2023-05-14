import pandas as pd
from pathlib import Path
from tqdm import tqdm


def combine_parquet(folder_path, output_file_path, output_file_name):
    folder_path = Path(folder_path)
    output_file_path = Path(output_file_path)

    folder_name = folder_path.name

    # Get a list of all Parquet files in the folder
    parquet_files = list(folder_path.glob("*.parquet"))

    # Initialize a list to store the DataFrames
    dfs = []

    # Iterate over each Parquet file
    for file in tqdm(parquet_files, desc="Processing"):
        # Read the Parquet file into a DataFrame
        df = pd.read_parquet(file)

        # Add a new column with the title of the file
        df["filename"] = file.stem
        df["filepath"] = str(file)

        # Convert the 'quotedTweet' column to nullable integer type
        df["quotedTweet"] = (
            df["quotedTweet"]
            .apply(lambda x: x if isinstance(x, int) else pd.NA)
            .astype(pd.Int64Dtype())
        )
        df["inReplyToUser"] = (
            df["inReplyToUser"]
            .apply(lambda x: x if isinstance(x, int) else pd.NA)
            .astype(pd.Int64Dtype())
        )

        # Append the DataFrame to the list
        dfs.append(df)

        # Concatenate all DataFrames into a single DataFrame
        combined_data = pd.concat(dfs, ignore_index=True)

        folder_info = [[folder_name, output_file_name, len(combined_data)]]

    # Write the combined data to a Parquet file
    combined_data.to_parquet(output_file_path / output_file_name, index=False)

    return folder_info

def combine_parquetv2(folder_path, output_file_path, output_file_name):
    folder_path = Path(folder_path)
    output_file_path = Path(output_file_path)

    folder_name = folder_path.name

    # Get a list of all folders in the main folder
    subfolders = [f for f in folder_path.iterdir() if f.is_dir()]

    # Initialize lists to store folder information
    folders_with_files = []
    folders_without_files = []

    # Initialize a list to store the DataFrames
    dfs = []

    # Iterate over each subfolder
    for subfolder in subfolders:
        # Get a list of all Parquet files in the subfolder
        parquet_files = list(subfolder.glob("*.parquet"))

        if parquet_files:
            # Subfolder contains parquet files
            folders_with_files.append(subfolder.name)
            for file in parquet_files:
                # Append the DataFrame to the list
                df = pd.read_parquet(file)
                df["filename"] = file.stem
                df["filepath"] = str(file)

                # Convert the 'quotedTweet' column to nullable integer type
                df["quotedTweet"] = (
                    df["quotedTweet"]
                    .apply(lambda x: x if isinstance(x, int) else pd.NA)
                    .astype(pd.Int64Dtype())
                )
                df["inReplyToUser"] = (
                    df["inReplyToUser"]
                    .apply(lambda x: x if isinstance(x, int) else pd.NA)
                    .astype(pd.Int64Dtype())
                )
                dfs.append(df)

        else:
            # Empty subfolder
            folders_without_files.append(subfolder.name)

    if dfs:
        # Concatenate all DataFrames into a single DataFrame
        combined_data = pd.concat(dfs, ignore_index=True)

        # Write the combined data to a Parquet file
        combined_data.to_parquet(output_file_path / output_file_name, index=False)

    else:
        # No parquet files found
        return None

    # Create folder information list
    folder_info = []
    for folder in folders_with_files:
        num_files = sum(folder_name in str(file) for file in parquet_files)
        folder_info.append([folder_name, folder, num_files])

    # Save folder information as a CSV file
    folder_info_df = pd.DataFrame(folder_info, columns=["Main Folder", "Subfolder", "File Count"])
    folder_info_df.to_csv(output_file_path / "folder_info.csv", index=False)

    return folder_info

# Define the folder path where the Parquet files are located
folder_path = "/Users/fahad/Desktop/Data/More data"

# Define the output file path for the combined Parquet file
output_file_path = "/Users/fahad/Desktop/processed_data"

# Define the output file name for the combined Parquet file
output_file_name = "combined_data9.parquet"

folder_info = combine_parquetv2(folder_path, output_file_path, output_file_name)

print(folder_info)
