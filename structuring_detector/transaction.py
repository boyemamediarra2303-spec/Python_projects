from datetime import datetime
from exceptions import InvalidTransactionError
import math 
import hashlib
class Transaction:
    def __init__(self,transaction_id, account_id, counterparty, timestamp, amount):
            if not isinstance (transaction_id,str) or transaction_id.strip()== '':
                  raise InvalidTransactionError (f"Invalid transaction_id: {transaction_id}")
            if not isinstance(account_id,str) or account_id.strip() =='' :
                    raise InvalidTransactionError (f"Invalid account_id: {account_id}")
            if not isinstance(counterparty,str) or counterparty.strip() =='':
                   raise InvalidTransactionError (f"Invalid counterparty: {counterparty}")
            if not isinstance(timestamp,datetime):
                    raise InvalidTransactionError (f"Invalid timestamp: {timestamp}")
            if not isinstance(amount,(int,float)) or not math.isfinite(amount) or amount <= 0:
                    raise InvalidTransactionError (f"Invalid amount: {amount}")
            self._transaction_id= transaction_id
            self._account_id= account_id
            self._counterparty= counterparty
            self._timestamp= timestamp
            self.amount= amount
        
    def __fingerprint(self):
        finger_print= hashlib.sha256(f"{self._transaction_id}|{self._account_id}|{self._timestamp.isoformat()}|{self.amount:.2f}".encode("utf-8")).hexdigest()
        return finger_print
    def is_tampered(self):
        current_fingerprint = hashlib.sha256(f"{self._transaction_id}|{self._account_id}|{self._timestamp.isoformat()}|{self.amount:.2f}".encode("utf-8")).hexdigest()
        if current_fingerprint != self._fingerprint():
                return True
        return False
    def __str__(self):
        return f"Transaction(transaction_id={self._transaction_id}, account_id={self._account_id}, counterparty={self._counterparty}, timestamp={self._timestamp.isoformat()}, amount={self.amount:.2f})"
           