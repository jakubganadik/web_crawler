import os
import re


def clean_article(directories, cleaned_dir):
    line_patterns = r"(<!--\[MOD.*?-->|<!--\[BEFORE-ARTICLE\]-->)"
    text_pattern = r">(.*?)<"

    os.makedirs(cleaned_dir, exist_ok=True)

    for directory in directories:
        directory_path = os.path.join(directory)
        html_files = [f for f in os.listdir(directory_path)]

        output_subdirectory = os.path.join(cleaned_dir, directory)
        os.makedirs(output_subdirectory, exist_ok=True)

        for html_file in html_files:
            input_html_file = os.path.join(directory_path, html_file)

            output_text_file_name = html_file.replace(".html", ".txt")
            if output_text_file_name.startswith("_"):
                output_text_file_name = output_text_file_name[1:]  # Remove leading "_"

            output_text_file = os.path.join(output_subdirectory, output_text_file_name)

            extracted_data = []

            with open(input_html_file, "r", encoding="utf-8") as file:
                lines = file.readlines()

            in_relevant_section = False

            for line in lines:
                if re.search(line_patterns, line):
                    in_relevant_section = True
                if in_relevant_section:
                    matches = re.findall(text_pattern, line)
                    for match in matches:
                        # Remove multiple spaces
                        cleaned_text = ' '.join(match.split())
                        extracted_data.append(cleaned_text)
                    in_relevant_section = False

            # Join the extracted data, remove additional spaces, and write to the output text file
            cleaned_data = ' '.join(extracted_data)
            cleaned_data = ' '.join(cleaned_data.split())

            with open(output_text_file, "w", encoding="utf-8") as file:
                file.write(cleaned_data)

            print(f"Extracted data from '{html_file}' and saved it to '{output_text_file}'.")


# Define the list of directories to process
dirs_to_search = [
    "animal_mammal",
    "animal_amphibian_test",
    "animal_bird",
    "animal_fish",
    "animal_invertebrate",
    "animal_reptile",
    "country",
    "region",
    "geography_land",  # Typo in "geography_land_not_clean"?
    "geography_water",
    "nationalpark"
]
dir_to_save = "./date_cleaned_new_test"
clean_article(dirs_to_search, dir_to_save)
