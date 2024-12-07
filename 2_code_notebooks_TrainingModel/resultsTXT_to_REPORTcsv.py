# import os
# import pandas as pd

# def extract_metrics_from_txt(file_path):
#     """
#     Extract metrics from the given .txt file.
#     """
#     metrics = {}
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#         model_name = lines[0].strip().split(": ")[1]
#         metrics['Model'] = model_name
#         metrics['File Path'] = lines[1].strip().split(": ")[1]
        
#         # Extract train metrics
#         for line in lines[3:8]:  # Lines for train metrics
#             if ":" in line:  # Check if line contains a colon
#                 parts = line.strip().split(": ")
#                 if len(parts) == 2:  # Ensure there are exactly two parts
#                     key, value = parts
#                     metrics[key] = value
        
#         # Extract test metrics
#         for line in lines[10:15]:  # Lines for test metrics
#             if ":" in line:  # Check if line contains a colon
#                 parts = line.strip().split(": ")
#                 if len(parts) == 2:  # Ensure there are exactly two parts
#                     key, value = parts
#                     metrics[key + " (Test)"] = value
            
#     return metrics

# def create_report_from_txt_files(folder_path, output_csv):
#     """
#     Create a report from all .txt files in the specified folder.
#     """
#     report_data = []
    
#     # Loop through all files in the directory
#     for file in os.listdir(folder_path):
#         if file.endswith(".txt"):
#             file_path = os.path.join(folder_path, file)
#             metrics = extract_metrics_from_txt(file_path)
#             report_data.append(metrics)
    
#     # Create a DataFrame and save to CSV
#     report_df = pd.DataFrame(report_data)
#     report_df.to_csv(output_csv, index=False)

# # Example usage
# folder_path = "D:/OneDrive - Hanoi University of Science and Technology/GIT/MiniProj_StockPrediction_ML_SpManhGraduationProj_2024/data/raw20192024/"
# output_csv = "D:/OneDrive - Hanoi University of Science and Technology/GIT/MiniProj_StockPrediction_ML_SpManhGraduationProj_2024/2_code_notebooks_TrainingModel/report.csv"
# create_report_from_txt_files(folder_path, output_csv)