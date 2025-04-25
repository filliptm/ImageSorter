# ImageSorter
This little app allows you to load up a directory of images and quickly select the ones you want and submit the changes. When submitted it will move those "Good" images in a dedicated folder of your choosing, and move the remaining displayed images to a secondary "BAD" folder. Allowing for quick, manual evaluation of mass amounts of images
__
once you have your folders loaded click save settings to ensure that the folders are set. It will persist through closing the app via a saved config file.
![imagde]([https://github.com/user-attachments/assets/be28561d-e9a6-45d9-bdc1-bff99f264498](https://github.com/filliptm/ImageSorter/blob/main/Screenshot%202025-04-25%20210923.png))

## Getting Started

### Windows
1. Double-click the `start.bat` file
2. The script will:
   - Check if a virtual environment exists
   - Create one if needed and install requirements
   - Activate the environment and launch the application

### macOS and Linux
1. Make the script executable (first time only):
   ```
   chmod +x start.sh
   ```
2. Run the script:
   ```
   ./start.sh
   ```
3. The script will:
   - Check if a virtual environment exists
   - Create one if needed and install requirements
   - Activate the environment and launch the application

## Usage
1. Set your input, good, and bad directories
2. Click "Save Settings" to persist your configuration
3. Click "Load Images" to display images from your input directory
4. Click on images you want to keep (they will be highlighted)
5. Click "Submit Selection" to move selected images to the good directory and unselected to the bad directory
6. Repeat until all images are sorted

## Development Notes

- A `.gitignore` file is included to exclude:
  - The `settings.json` file (contains user-specific settings)
  - Virtual environment directories
  - Python cache files and other common exclusions
