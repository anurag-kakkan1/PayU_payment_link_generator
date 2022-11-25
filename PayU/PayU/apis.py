import requests
from .constants import PaymentConstants

class PayUAPI():


    def create_invoice(self, key, var1, hash_value, command=PaymentConstants.CREATE_INVOICE):
        """
        Calls the PayU create_invoice API
        :param: key - string which contains merchant key
        :param: var1 - json string in the format  {"amount": "1000","txnid":"unique_transaction_id","productinfo":"Info",firstname":"name1","email":"test@awaaz.de","phone":"123456789"}
        :param: hash_value
        :param: command - Default value: "create_invoice"
        :returns: response
        """
        url = "https://test.payu.in/merchant/postservice?form=1"
        payload =f"key={key}&command={command}&var1={var1}&hash={hash_value}"
        headers = { "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded" } 

        response = requests.request("POST", url, data=payload, headers=headers)
        return response