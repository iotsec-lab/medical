import os
import sys
def rename_files(folder):
    for filename in os.listdir(folder):
        if filename.startswith("01_"):
            os.rename(
                os.path.join(folder, filename),
                os.path.join(folder, filename[3:])
            )

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the folder name as a command line argument.")
        sys.exit(1)

    folder = sys.argv[1]
    rename_files(folder)