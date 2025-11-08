import subprocess
import sys

def execute_it():
    result = subprocess.run([sys.executable, "generate_img.py", "--headed", "--xvfb"])
    if result.returncode != 0:
        print(f"\n\n\nErreur : generate_img.py a échoué avec le code {result.returncode}\n\n\n")
        return False
    else:
        print("Succès !")
        return True
