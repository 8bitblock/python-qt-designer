with open("pyqt_designer_v2/backend/generator_py.py", "r") as f:
    lines = f.readlines()

# check if class PythonGenerator(BaseGenerator): is missing
has_class = any("class PythonGenerator" in line for line in lines)

if not has_class:
    print("Missing class declaration. Adding it...")
    with open("pyqt_designer_v2/backend/generator_py.py", "w") as f:
        f.write("import json\nfrom .generator_base import BaseGenerator\n\nclass PythonGenerator(BaseGenerator):\n")
        f.writelines(lines[2:])
