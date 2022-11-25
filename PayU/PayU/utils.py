import re 
import csv
import json
import uuid
import hashlib
import pandas as pd
from xml.etree import ElementTree

from .constants import CommonConstants, PaymentConstants
from .apis import PayUAPI
from .exceptions import MissingDataException
import os 



class PayUUtils():

    @staticmethod
    def create_invoice(record):
        """
        This function formats the record data into the required format and calls the PayUApi to create_invoice.
        :param: record 
        :returns: payment_response
        """
        # Generating unique transaction id
        txnid = uuid.uuid4()


        phone = record["phone_number"]
        amount = record['loan_amount']

        key = os.getenv('KEY')
        salt = os.getenv('SALT')

        command = PaymentConstants.CREATE_INVOICE
        
        # creating var1 varible
        var1 = {"amount": str(amount),"txnid":str(txnid),"productinfo":PaymentConstants.PRODUCT_INFO,"firstname":PaymentConstants.FIRSTNAME,"email":PaymentConstants.EMAIL,"phone":phone}
        var1string = json.dumps(var1, separators=(',', ':'))

        #fetching the hash value
        hash_value = str(PayUUtils.getHashForInvoice({"key": key, "command": command, "var1": var1string, "salt": salt}))

        payu_instance = PayUAPI()
        payment_response = payu_instance.create_invoice(key, var1string, hash_value)

        return payment_response

    @staticmethod
    def update_payment_url(data):
        """
        Updates each record with payment url link.
        :param: data - Data in the format [{"key": "value", "key": value}, {"key": "value", "key": value}]
        """
        for record in data:

            if not record["phone_number"]:
                raise MissingDataException("Missing data in field {}".format("phone_number"))

            if not record["loan_amount"]:
                raise MissingDataException("Missing data in field {}".format("loan_amount"))

            payment_response = PayUUtils.create_invoice(record)
            payment_url = CommonUtils.get_payment_url(payment_response)
            record["url"] = payment_url

        
    @staticmethod
    def getHashForInvoice(data):
        """
        Used to created hash value for creating invoice. Hash pattern: sha512(key|command|var1|salt)
        :param: data format - {"key": "abcde", "command": "create_voice", "var1": "{}", "salt": salt}
        :returns: hash_value
        """
        m = hashlib.sha512()
        hashString = data["key"] + "|" + data["command"] + "|" + data["var1"] + "|" + data["salt"]
        m.update(hashString.encode("utf8"))
        return m.hexdigest()
    


class CommonUtils(object):

    @staticmethod
    def process_iterable_in_chunks(iterable, chunk_size=CommonConstants.DEFAULT_CHUNK_SIZE):
        '''
        A convenience method for processing a list/queryset of objects in chunks
        pattern stolen from https://stackoverflow.com/a/29708603/199754
        :param: iterable list or queryset of objects
        :param: chunk_size max number of objects to process in one iteration
        :returns: None
        '''
        offset = 0
        chunk = iterable[offset:offset + chunk_size]
        while chunk:
            yield chunk  # body executes here

            # increment the iterable
            offset += chunk_size
            chunk = iterable[offset:offset + chunk_size]

    @staticmethod
    def get_payment_url(response):
        """
        Extracts the url from the string
        :param: response - Returned from the create_invoice api
        """
        tree = ElementTree.fromstring(response.content)
        payment_url = re.findall(r'(https?://[^\s]+)', tree.text)

        if not payment_url:
            return None
        return payment_url[0]


class CSVUtils(object):

    @staticmethod
    def write_header_to_csv(data, file_path, file_name, append=False):
        if data:
            keys = list(data[0].keys())
            if 'url' not in keys:
                keys.extend(["url"])

            write_append_mode = 'a' if append else 'w'

            with open('{}/{}.csv'.format(file_path, file_name), write_append_mode)  as output_file:
                writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
                writer.writeheader()

    @staticmethod
    def write_or_append_to_csv(data, file_path, file_name, append=False):
        if data:
            keys = list(data[0].keys())
            if 'url' not in keys:
                keys.extend(["url"])


            write_append_mode = 'a' if append else 'w'
            with open('{}/{}.csv'.format(file_path, file_name), write_append_mode)  as output_file:
                writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
                writer.writerows(data)

    @staticmethod
    def read_csv(csv_file_path, replace_null=False):
        """
        replace_null: If set to True: all  null values in csv will be replaced by ("NA","NaN","None" etc).
                      If set to False: Null values will remain blank. (In cases like "send_on" date,
                      we want it blank,so default for this function w.r.t the usage of this Demo has been kept as false)
        """
        df = pd.read_csv(csv_file_path, na_filter=replace_null, encoding = "ISO-8859-1", dtype=str)
        headers = df.columns
        data = df.to_dict('records')
        return headers, data