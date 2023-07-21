import pandas as pd
from pathlib import Path
from tqdm import tqdm


def get_users(folder_path, output_file_path, output_file_name):
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

        df = df[["id", "rawContent", "user"]]

        user = pd.json_normalize(df["user"])

        user = user[["id", "favouritesCount", "followersCount", "friendsCount"]]

        user = user.rename(columns={"id": "user_id"})

        df = pd.concat([df, user], axis=1)

        df.drop("user", inplace=True, axis=1)

        dfs.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_data = pd.concat(dfs, ignore_index=True)

    folder_info = [[folder_name, output_file_name, len(combined_data)]]

    # Write the combined data to a Parquet file
    combined_data.to_parquet(output_file_path / output_file_name, index=False)

    return folder_info


# Define the folder path where the Parquet files are located
folder_path = r"C:\Users\fashaikh\Desktop\rawDataThesis\processed_data"

# Define the output file path for the combined Parquet file
output_file_path = r"C:\Users\fashaikh\Desktop\Thesis_main"

# Define the output file name for the combined Parquet file
output_file_name = "users_data.parquet"

folder_info = get_users(folder_path, output_file_path, output_file_name)

print(folder_info)
