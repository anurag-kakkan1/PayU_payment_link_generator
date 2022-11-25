import os
import argparse
from dotenv import load_dotenv

from PayU.validators import DataValidator
from PayU.utils import CSVUtils, PayUUtils, CommonUtils

load_dotenv()

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("source_path", help="Source path of file", type=str)
    parser.add_argument("destination_path", help="Destination path of file", type=str)
    parser.add_argument("destination_file_name", help="Name of destination file", type=str)

    # Parse arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parseArguments()
    source_path = args.__dict__['source_path']
    destination_path= args.__dict__['destination_path']
    destination_file_name = args.__dict__['destination_file_name']

    print("Reading data from {}...". format(source_path))

    #Check if file path exists
    if os.path.exists(source_path):
        file_path = source_path
    else:
        print("File path don't exists")

    headers, data = CSVUtils.read_csv(source_path)

    # Validate the data
    validator = DataValidator()
    validator.validate(data)

    CSVUtils.write_header_to_csv(data, destination_path, destination_file_name)
    print("Data validated...")


    print("Creating Urls...")
    for records in CommonUtils.process_iterable_in_chunks(data):
        PayUUtils.update_payment_url(records)    
        CSVUtils.write_or_append_to_csv(records, destination_path, destination_file_name, append=True)
    print("Urls created...")

    print("Created file \"{}\" at {} ".format(destination_file_name, destination_path))
    
