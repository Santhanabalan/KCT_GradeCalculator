import os
from pdfminer.high_level import extract_text

def parse_pdf_files(file_paths):
    results = {}
    all_grades = []
    all_credits = []
    for file_path in file_paths:
        print(f'Parsing file: {file_path}')
        text = extract_text(file_path)
        result = []
        for line in text.split('\n'):
            if line.strip().isdigit():
                result.append(int(line.strip()))
        half = len(result) // 2
        all_grades.extend(result[:half])
        all_credits.extend(result[half:])
        results[os.path.basename(file_path)] = result
    return results, all_grades, all_credits

def computeGPA(grade,credit):
    total = 0
    for i in range(len(grade)):
        total += grade[i]*credit[i]
    return round(total/sum(credit),2)

dir_path = './files'
file_paths = [os.path.join(dir_path, file) for file in os.listdir(dir_path) if file.endswith('.pdf')]

if not file_paths:
    print('No PDF files found in the directory')
else:
    parsedDataDict, all_grades, all_credits = parse_pdf_files(file_paths)
    print('-'*30)
    for file_name, parsedData in parsedDataDict.items():
        half = len(parsedData) // 2
        print(f"SGPA for {file_name}: {computeGPA(parsedData[:half],parsedData[half:])}")
    print('-'*30)
    print(f"Overall CGPA: {computeGPA(all_grades, all_credits)}")
