import subprocess

# Runs both modules in order to gather repos and convert list to excel
subprocess.run(["python3", "get_repo_list.py"])
subprocess.run(["python3", "convert_csv_xlsx.py"])