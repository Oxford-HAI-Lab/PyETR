import subprocess


def main():
    subprocess.run(["pre-commit", "run", "--all-files"])
