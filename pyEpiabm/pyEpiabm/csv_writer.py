import csv
import typing

class CsvWriter:
    def __init__(self, filename: str, fieldnames: typing.List):
        try:    
            self.f = open(filename, 'w')
            self.writer = csv.writer(
                self.f, delimiter=',')
            self.writer.writerow(fieldnames)
        except FileNotFoundError as e:
            self.f = None
            self.writer = None
            # TODO: Log file not found error
            print(f"FileNotFoundError: {str(e)}.")
            raise e

    def __del__(self):
        if self.f:
            self.f.close()
    
    def write(self, row: typing.List):
        self.writer.writerow(row)
