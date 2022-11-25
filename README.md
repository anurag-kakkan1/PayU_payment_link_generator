
# PayU Payment Links

Python script used to create payment links from file.

## Prerequisites
For python:

Download the folder.

Create a virtual environment and activate it. 

Run command `pip install -r ./PayU/requirements.txt`

Create a .env file inside the folder containing create_payment_links.py file.

Add two fields in the .env file:
```bash
KEY=""
SALT=""
```
The KEY (merchant key) and SALT (merchant salt) value is obtained from the PayU dashboard.
These values are used to authenticate the payment and to generate the hash values.


## Usage

Download the folder and open PayU folder in terminal.

Activate the virtual environment.

Run the following command:

```bash
  python create_payment_links.py <source_file_path> <destination_file_path> <destination_file_name>
```

- source_file_path: The full file path along with file name for which url needs to be generated.
- destination_file_path: The full path of the folder where new file needs to be created.
- destination_file_name: Name of the newly created file.

Example:
```bash
python create_payment_links.py "/home/awaazde/Desktop/Work/TestFiles/file1.csv" "/home/awaazde/Download" "new_file123"
```