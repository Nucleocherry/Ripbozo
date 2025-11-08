import subprocess
import sys


def execute_it():
	# Lancer generate_img.py en passant le prompt via une variable d'environnement
	subprocess.run([sys.executable, "generate_img.py", "--xvfb"])

