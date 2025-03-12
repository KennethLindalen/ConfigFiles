import os
import subprocess
import zipfile
import shutil
from pathlib import Path

project_path = r"PATH"
output_path = os.path.join(project_path, "bin", "Release", "net8.0")  
desktop_path = Path.home() / "Desktop"  
zip_file_name = "ProjectBuild.zip"

def build_project():
    # Print a message indicating that the build process is starting
    print("Building the C# project...")

    # Run the 'dotnet build' command to build the C# project in Release mode
    # Capture the output and return code of the command
    result = subprocess.run(
        ["dotnet", "build", project_path, "-c", "Release"],
        capture_output=True, 
        text=True
    )
    
    # Check if the build process was successful by examining the return code
    if result.returncode == 0:
        # If the return code is 0, print a success message
        print("Build succeeded.")
    else:
        # If the return code is non-zero, print a failure message
        print("Build failed.")
        # Print the standard output and standard error from the build process
        print(result.stdout)
        print(result.stderr)
        # Return False to indicate build failure
        return False

    # Return True to indicate build success
    return True

def zip_build_files():
    """
    This function zips up the files in the Release directory of the C# project
    and creates a zip file on the desktop.

    The zip file is given a name that is specified in the zip_file_name variable.
    The file is created on the desktop, which is the path returned by Path.home() / "Desktop"
    """

    # Construct the path to the zip file
    zip_file_path = desktop_path / zip_file_name

    # Print a message indicating that the zip file is being created
    print(f"Creating zip file at {zip_file_path}...")

    # Create the zip file
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Walk the directory tree rooted in output_path
        for root, dirs, files in os.walk(output_path):
            # Iterate over the files in the current directory
            for file in files:
                # Construct the full path to the current file
                file_path = os.path.join(root, file)

                # Construct the path to the file relative to the output_path
                # This is the path that will be used in the zip file
                arcname = os.path.relpath(file_path, output_path)

                # Add the file to the zip file
                zipf.write(file_path, arcname)

    # Print a message indicating that the zip file has been created
    print("Zip file created successfully.")


def main():
    # Start the build process for the C# project
    if build_project():
        # If the build is successful, proceed to create a zip file of the build files
        zip_build_files()
    else:
        # If the build fails, print an error message indicating that the zip file will not be created
        print("Build process failed. Zip file not created.")

if __name__ == "__main__":
    main()
