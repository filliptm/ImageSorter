#!/bin/bash
echo "Starting ImageSorter..."

# Check if venv directory exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    
    echo "Installing requirements..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo "Setup complete!"
else
    echo "Virtual environment found."
    source venv/bin/activate
fi

echo "Launching ImageSorter..."
python app.py

# Check if the application exited with an error
if [ $? -ne 0 ]; then
    echo "An error occurred while running the application."
    read -p "Press Enter to continue..."
fi