import random
import time
import sys
import tty
import termios

class ThreeLevelPasswordSystem:
    def __init__(self, username, password, security_question, security_answer):
        self.username = username
        self.password = password
        self.security_question = security_question
        self.security_answer = security_answer
        self.otp = None

    def verify_password(self, input_password):
        return input_password == self.password

    def generate_otp(self):
        self.otp = random.randint(100000, 999999)
        print(f"Your OTP is: {self.otp}")
        time.sleep(1)

    def verify_otp(self, input_otp):
        return int(input_otp) == self.otp

    def verify_security_question(self, input_answer):
        return input_answer.lower() == self.security_answer.lower()

    def authenticate(self):
        print("Welcome to the Three-Level Password System")
        input_password = self.get_password("Enter your password: ")
        if not self.verify_password(input_password):
            print("Password is incorrect! Access Denied.")
            return
        self.generate_otp()
        input_otp = input("Enter the OTP generated for your account: ")
        if not self.verify_otp(input_otp):
            print("Incorrect OTP! Access Denied.")
            return

        print(f"Security Question: {self.security_question}")
        input_answer = input("Enter your answer: ")
        if not self.verify_security_question(input_answer):
            print("Incorrect answer! Access Denied.")
            return

        print("Authentication Successful! Access Granted.")

    def get_password(self, prompt):
        print(prompt, end='', flush=True)
        password = ''
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                char = sys.stdin.read(1)
                if char == '\n' or char == '\r':
                    print() 
                    break
                elif char == '\x08' or char == '\x7f': 
                    if len(password) > 0:
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                        password = password[:-1]
                else:
                    sys.stdout.write('*')
                    sys.stdout.flush()
                    password += char
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return password

def main():
    username = input("Set your username: ")
    password = ThreeLevelPasswordSystem(username, "", "", "").get_password("Set your password: ")
    security_question = input("Set your security question: ")
    security_answer = input("Set your security answer: ")
    auth_system = ThreeLevelPasswordSystem(username, password, security_question, security_answer)
    auth_system.authenticate()

if __name__ == "__main__":
    main()
