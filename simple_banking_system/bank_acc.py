import sys,random
from typing import Tuple

class Bank:

    def __init__(self, acc_no: int, acc_name: str, amount: int, auth: int, reset: str) -> None:
        self.acc_no = acc_no
        self.acc_name = acc_name
        self.amount = amount
        self.auth = auth
        self.reset = reset

    def checkAuth(self) -> None:
        while True:
            user_auth=int(input("(Press 0 to cancel)\nEnter the auth code: "))            
            try:
                if user_auth!=self.auth:
                    if user_auth == 0:
                        raise InterruptedError("Authentication interrupted by user!")
                    elif len(str(user_auth))!=len(str(self.auth)):
                        raise ValueError(f"Authentication code must be 6 digits long. Please re-enter!")
                    raise ValueError("Invalid code entered. Please enter!")

                return 1
            except ValueError as error:
                print(f"Error: {error}")
            except InterruptedError as error:
                print(f"{error}")
                print("Authentication failed. Access denied!")
                break
            except Exception as error:
                print(f"Unexpected Error: {error}.")
                print("Authentication failed. Access denied!")
                break

    def checkBalance(self) -> None:
        try:
            if self.checkAuth() is None:
                return
            print(f"Current Balance: {self.amount}")
            if self.amount == 0:
                raise ValueError("Zero balance detected!")
        except ValueError as error:
            print(f"NOTE: {error}")
        except Exception as error:
            print(f"Unexpected error: {error}.")

    def depositFunds(self, amount: int) -> None:
        try:
            if self.checkAuth() is None:
                return
            if amount > 999999 or amount <= 0:
                raise ValueError("Please enter a value within 0-999999.\nContact the bank to add more than that!")
            self.amount+=amount
            print(f"Rs. {amount} deposited to your bank account.\nCurrent Balance: {self.amount}")
        except ValueError as error:
            print(f"Error: {error}")
        except Exception as error:
            print(f"Unexpected Error: {error}")
    
    def withdrawFunds(self, amount: int) -> None:
        try:
            if self.checkAuth() is None:
                return
            if amount > 999999 | amount <= 0:
                raise ValueError("Please enter a value within 0-999999.\nContact the bank to add more than that!")
            if self.amount < amount:
                raise ValueError(f"Insufficient funds available in your bank account.\nCurrent Balance: {self.amount}")
            self.amount-=amount
            print(f"Rs. {amount} withdrawn from your bank account.\nCurrent Balance: {self.amount}")
        except ValueError as error:
            print(f"Error: {error}")
        except Exception as error:
            print(f"Unexpected Error: {error}")
    
    def resetAuth(self) -> None:
        while True:
            try:
                reset = str(input("Enter the reset keyword: "))
                if reset != self.reset:
                    if reset == "q":
                        raise InterruptedError("Reset interrupted by user!")
                    raise ValueError(f"Invalid reset code received. Try Again!")
                proceed = int(input("Operation successfull.. Press 1 to continue: "))
            except ValueError as error:
                print(f"Error: {error}")
            except InterruptedError as error:
                print(f"{error}")
                print("Authentication failed. Access denied!")
                proceed = 0
                break
            except Exception as error:
                print(f"Unexpected Error: {error}.")
                print("Authentication failed. Access denied!")
                proceed = 0
                break
        
        if proceed != 1:
            return

        while True:    
            try:
                new_auth=str(input("Enter a new auth code: "))
                if len(str(new_auth)) != len(str(self.auth)):
                    raise ValueError("Authentication code must be 6 digits long. Try again!")
                self.auth = new_auth
                print(f"Auth code successfully changed!\nYour new auth code is {self.auth}.")
            except ValueError as error:
                print(f"Error: {error}")
            except Exception as error:
                print(f"Unexpected Error: {error}")
                break

def createAccount(name: str, already_exists: list) -> tuple:
    try:
        acc_no = random.randint(1111,9999)
        auth = int(input("Enter your auth code (6 digit integer): "))
        reset = str(input("Enter your reset keyword (n character string): "))

        print("Validating account details...")
        
        while acc_no in already_exists:
            acc_no = random.randint(1111,9999)
        while len(str(auth)) != 6:
            auth = int(input("Authentication code must be 6 digits long. Re-enter your auth code: "))
        while not reset.isalpha():
            reset = str(input("Invalid input received for reset keyword. Re-enter your reset keyword: "))
        print(f"Your ACN ID: {acc_no}\nYour Auth Code: {auth}\nYour reset code: {reset}\nCreating account...")

        print("Account created successfully!\n")
        return Bank(acc_no = acc_no, acc_name = name, amount = 0, auth = auth, reset = reset), acc_no
    except Exception as error:
        print(f"Account creation failed.\nUnexpected Error: {error}.")
        

def main():
    print("Banking System Application")
    accounts: dict[str, Bank] = {}
    already_exists: list = []
    while True:
        try:
            choice: int = int (input("1. Create a new account\n2. Deposit funds\n3. Withdraw funds\n4. Check balance\n5. Exit\nEnter your choice: "))
            match choice:
                case 1:
                    name = str(input("Enter your name (n character string): "))
                    result = createAccount(name,already_exists)
                    accounts[name] = result[0]
                    already_exists.append(result[1])
                case 2:
                    name = str(input("Enter the name of the account holder: "))
                    amount = int(input("Enter the amount you wish to deposit: "))
                    accounts[name].depositFunds(amount)
                case 3:
                    name = str(input("Enter the name of the account holder: "))
                    amount = int(input("Enter the amount you wish to withdraw: "))
                    accounts[name].withdrawFunds(amount)
                case 4:
                    name = str(input("Enter the name of the account holder: "))
                    accounts[name].checkBalance()
                case 5:
                    print("Program terminated!")
                    sys.exit(0)
                case 6:
                    for i in already_exists:
                        print(i,"\n")
                case _:
                    raise ValueError("Invalid choice entered. Try again!")
        
        except Exception as error:
            print(f"Unexpected error: {error}. Terminating Program!")
            sys.exit(1)
        
if __name__ == "__main__":
    main()