import os


def prepare_file_names(directory_path):
    # Specify the directory path

    # Initialize an empty list to store file names
    file_names = []

    # Iterate through each file in the directory
    for root, dirs, files in os.walk(directory_path):
        for dir in dirs:
            for subRoot, subDirs, subFiles in os.walk(os.path.join(directory_path, dir)):
                for file in subFiles:
                    # Split the file name using "_" and remove "-"
                    parts = file.split("_")[1]
                    parts = parts.split(".")[0]
                    parts = parts.split("-")
                    full_string = ""
                    for part in parts:
                        full_string += part.capitalize()
                    file_names.append(full_string)

    # Join the file names with commas
    file_names_str = ",".join(file_names)

    # Specify the path for the output text file
    output_file_path = "file_names2.txt"

    # Write the file names to the text file
    with open(output_file_path, "w") as output_file:
        output_file.write(file_names_str)


directory_path = "C:\\Users\\ASUS\\PycharmProjects\\VINF_data_scraping_ganadik\\date_cleaned_new"
prepare_file_names(directory_path)
