#!/bin/bash

# Ensure the script exits on error
set -e

# Step 1: Deactivate any active virtual environments
if [[ "$VIRTUAL_ENV" != "" ]]; then
    deactivate
fi

# Step 2: Navigate to the Grobid client directory and install it
cd grobid_client_python/
echo "Installing Grobid Client..."
python3 setup.py install

# Step 3: Run Grobid Client
echo "Running Grobid Client"
result_grobid1=$(grobid_client --input ../data/pdf_files/ --output ../data/xml_grobid/ processFulltextDocument)
echo "$result_grobid1"

# Step 4: Prompt user to rerun Grobid Client if needed
read -p "Do you need to rerun Grobid? (y/n): " user_input
if [[ "$user_input" == "y" ]]; then
    echo "Re-running Grobid Client..."
    result_grobid2=$(grobid_client --input ../data/pdf_files/ --output ../data/xml_grobid/ processFulltextDocument)
    echo "$result_grobid2"
elif [[ "$user_input" == "n" ]]; then
    echo "Skipping Grobid rerun."
else
    echo "Invalid input. Please type 'y' or 'n'."
fi

# Step 5: Navigate back to the main directory and move XML files
cd ..
echo "Organizing XML files..."
cp ./data/xml_grobid/*.xml ./data/xml_files/
cp ./data/xml_grobid/*.xml ./data/json_files/from_xml/

# Step 6: Activate virtual environment for Software Mentions Client
echo "Activating virtual environment for Software Mentions Client..."
source ./software_mentions_client/venv/bin/activate

# Step 7: Navigate to the Software Mentions Client directory and run it
cd software_mentions_client/
echo "Running Software Mentions Client..."
result_softcite1=$(python3 -m software_mentions_client.client --repo-in ../data/json_files/from_xml/ --scorched-earth)
echo "$result_softcite1"

# Step 8: Prompt user to rerun Software Mentions Client if needed
read -p "Do you need to rerun Software Mentions Client? (y/n): " user_input2
if [[ "$user_input2" == "y" ]]; then
    echo "Re-running Software Mentions Client..."
    result_softcite2=$(python3 -m software_mentions_client.client --repo-in ../data/json_files/from_xml/ --scorched-earth --reprocess)
    echo "$result_softcite2"
elif [[ "$user_input2" == "n" ]]; then
    echo "Skipping Software Mentions Client rerun."
else
    echo "Invalid input. Please type 'y' or 'n'."
fi

echo "Script completed successfully."
