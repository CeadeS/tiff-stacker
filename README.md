# tiff-stacker

## Simple usage

python to_one_file.py input_directory

input_directory is scanned for tiff-files. Stacked files are stored to ./out/input_directory

### Example

python to_one_file.py ./16bit

## Output directory

python to_one_file.py input_directory_name -o output_directory

Creates an output directory and stores files in output_directory/input_directory

### Example
python to_one_file.py ./16bit -o /data/example/
