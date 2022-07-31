import argparse
import pandas as pd

class options():
    def parse_opt(known=False):
        parser = argparse.ArgumentParser()
        parser.add_argument('--sid', type=str, default='', help='Series ID')
        parser.add_argument('--pkf', type=str, default='', help='Pickle file')
        parser.add_argument('--m2s', type=str, nargs='+', default='', help='Merge 2 series')
        parser.add_argument('--l2s', type=str, nargs='+', default='', help='Labels for 2 series')
        parser.add_argument('--oms', type=str, nargs='+', default='', help='Open merged series')
        parser.add_argument('--oss', type=str, nargs='+', default='', help='Open stationary series')
        parser.add_argument('--otr', type=str, nargs='+', default='', help='Open training set')
        parser.add_argument('--ote', type=str, nargs='+', default='', help='Open test set')
        opt = parser.parse_known_args()[0] if known else parser.parse_args()
        return opt

    def yes_no(question):
        i = 0
        while i < 2:
            answer = input(question)
            if any(answer.lower() == f for f in ["yes", 'y', '1', 'ye', 'Y']):
                return True
            elif any(answer.lower() == f for f in ['no', 'n', '0', 'N']):
                return False
            else:
                i += 1
                if i < 2:
                    print('Please enter y or n')
                else:
                    print("Nothing done")



