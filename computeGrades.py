import os
from pdfminer.high_level import extract_text


class GradeParser:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.file_paths = self.get_file_paths()
        self.all_grades = []
        self.all_credits = []

    def get_file_paths(self):
        return [
            os.path.join(self.dir_path, file)
            for file in os.listdir(self.dir_path)
            if file.endswith(".pdf")
        ]

    def parse_pdf_files(self):
        results = {}
        for file_path in self.file_paths:
            print(f"Parsing file: {file_path}")
            text = extract_text(file_path)
            result = [
                int(line.strip()) for line in text.split("\n") if line.strip().isdigit()
            ]
            half = len(result) // 2
            self.all_grades.extend(result[:half])
            self.all_credits.extend(result[half:])
            results[os.path.basename(file_path)] = result
        return results

    def compute_gpa(self, grades, credits):
        total = sum(grade * credit for grade, credit in zip(grades, credits))
        return round(total / sum(credits), 2)

    def print_results(self):
        if not self.file_paths:
            print("No PDF files found in the directory")
            return

        parsed_data_dict = self.parse_pdf_files()
        print("-" * 30)
        for file_name, parsed_data in parsed_data_dict.items():
            half = len(parsed_data) // 2
            print(
                f"SGPA for {file_name}: {self.compute_gpa(parsed_data[:half], parsed_data[half:])}"
            )
        print("-" * 30)
        print(f"Overall CGPA: {self.compute_gpa(self.all_grades, self.all_credits)}")


if __name__ == "__main__":
    # Initialize the GradeParser class with the directory path './files' as an argument.
    # This is the directory where the code will look for PDF files to parse.
    grade_parser = GradeParser("./files")
    # Call the print_results method on the grade_parser object to parse the PDF files,
    # compute the SGPA for each file and the overall CGPA, and print the results.
    grade_parser.print_results()
