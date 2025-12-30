#!/bin/bash

# Step 1: Deactivate any active virtual environments

# Step 2: Navigate to the Grobid client directory and install it
cd ../grobid_client_python/
echo "Installing Grobid Client..."
python3 setup.py install > /dev/null 2>&1

# Step 3: Run Grobid Client in a loop
while true ; do
    echo "Running Grobid Client"
    result_grobid=$(grobid_client --input ../data/pdf_files/ --output ../data/xml_grobid/ processFulltextDocument --force)
    echo "$result_grobid"

    read -p "Are you satisfied with the Grobid result? (y/n): " grobid_input
    if [[ "$grobid_input" == "y" ]]; then
        echo "Proceeding with the next step."
        break
    elif [[ "$grobid_input" == "n" ]]; then
        echo "Re-running Grobid Client..."
    else
        echo "Invalid input. Please type 'y' or 'n'."
    fi
done

# Step 4: Organize XML files
echo "Organizing XML files..."
cd ..
cp ./data/xml_grobid/*.xml ./data/xml_files/
cp ./data/xml_grobid/*.xml ./data/json_files/from_xml/

# Step 5: Activate virtual environment for Software Mentions Client
echo "Activating virtual environment for Software Mentions Client..."
source ./software_mentions_client/venv/bin/activate

# Step 6: Navigate to the Software Mentions Client directory and install it
cd software_mentions_client/
python3 -m pip install -e . > /dev/null 2>&1

# Initialize 'processed' variable
processed="n"

# Step 7: Run Software Mentions Client in a loop
while true; do
    echo "Running Software Mentions Client..."
    if [[ "$processed" == "n" ]]; then
        # First run without --reprocess
        result_softcite=$(python3 -m software_mentions_client.client --repo-in ../data/json_files/from_xml/ --scorched-earth)
        echo "$result_softcite"
        processed="y"  # Mark as processed
    elif [[ "$processed" == "y" ]]; then
        # Second run with --reprocess
        result_softcite=$(python3 -m software_mentions_client.client --repo-in ../data/json_files/from_xml/ --scorched-earth --reprocess)
        echo "$result_softcite"
    fi

    # Ask if the user is satisfied with the result
    read -p "Are you satisfied with the Software Mentions Client result? (y/n): " softcite_input
    if [[ "$softcite_input" == "y" ]]; then
        echo "Proceeding to the end of the pipeline."
        break  # Exit the loop if the user is satisfied
    elif [[ "$softcite_input" == "n" ]]; then
        echo "Re-running Software Mentions Client..."
        processed="n"  # Reset processed flag to run the client again
    else
        echo "Invalid input. Please type 'y' or 'n'."
    fi
done

echo "Launching SOFTware-Viz (light by default)"

source ../SOFTware-Viz-Light/venv/bin/activate
cp ../data/xml_files/*.xml ../SOFTware-Viz-Light/app/static/data/xml_files/
cp ../data/json_files/from_xml/*.json ../SOFTware-Viz-Light/app/static/data/json_files/from_xml/
python ../SOFTware-Viz-Light/run.py