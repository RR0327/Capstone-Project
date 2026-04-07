import splitfolders

input_folder = "dataset_raw"
output_folder = "dataset"

splitfolders.ratio(
    input_folder,
    output=output_folder,
    seed=42,
    ratio=(0.7, 0.15, 0.15)
)