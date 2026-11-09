from datetime import datetime
from exceptions import InvalidTransactionError
import math 
import hashlib
from utils import parse_amount , format_xof
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
                if isinstance(amount, bool) or not isinstance(amount,(int,float)) or not math.isfinite(amount) or amount <= 0:
                        raise InvalidTransactionError (f"Invalid amount: {amount}")             
                self._transaction_id= transaction_id
                self._account_id= account_id
                self._counterparty= counterparty
                self._timestamp= timestamp
                self._amount= self._validate_amount(amount)
                self.__fingerprint= self.__make_fingerprint()
        @property
        def transaction_id(self):
                return self._transaction_id
        @property
        def account_id(self):
                return self._account_id
        @property
        def counterparty(self):
                return self._counterparty
        @property
        def timestamp(self):
                return self._timestamp
        @staticmethod
        def _validate_amount(amount):
                if isinstance(amount, bool) or not isinstance (amount, (int, float))or amount <= 0:
                        raise InvalidTransactionError (f"Invalid amount: {amount}")
                return float(amount)
        @property
        def amount(self):
                return self._amount
        @amount.setter
        def amount(self,amount):
                self._amount= self._validate_amount(amount)
        def __make_fingerprint(self):
                string= f"{self._transaction_id}|{self._account_id}|{self._timestamp.isoformat()}|{self._amount:.2f}"
                fingerprint = hashlib.sha256(string.encode("utf-8")).hexdigest()
                return fingerprint
        @property
        def fingerprint(self):
                return self.__fingerprint
        def is_tampered(self):
                return self.__fingerprint != self.__make_fingerprint()
        def __str__(self):
                return f"{self._transaction_id} | {self._account_id} | {self._timestamp.strftime("%Y-%m-%d %H:%M")} | {format_xof(self._amount)}"
        def __repr__(self): 
                return f"{self._transaction_id} | {self._account_id} | {self._timestamp.strftime("%Y-%m-%d %H:%M")} | {format_xof(self._amount)} | {self._counterparty}"
        def __eq__(self, other):
                if not isinstance(other, Transaction):
                        return NotImplemented
                return self._transaction_id == other._transaction_id
        def __hash__(self):
                return hash((self._transaction_id))
        def __lt__(self, other):
                if not isinstance(other, Transaction):
                        return NotImplemented
                return (self._timestamp, self._transaction_id) < (other._timestamp, other._transaction_id)
        @classmethod
        def from_row(cls, row):
                try:
                        transaction_id = row["transaction_id"]
                        account_id = row["account_id"]
                        counterparty = row["counterparty"]
                        timestamp = datetime.fromisoformat(row["timestamp"])
                        amount = parse_amount(row["amount"])
                except (KeyError, ValueError) as e:
                        raise InvalidTransactionError(f"Invalid row data: {row}") from e
                return Transaction(transaction_id, account_id, counterparty, timestamp, amount)
