import subprocess


def run(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)


if __name__ == "__main__":
    run(["chmod", "+x", "tasctl"])
    run(["./tasctl", "--help"])
