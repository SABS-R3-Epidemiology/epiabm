import csv
import typing

class CsvDictWriter:
    def __init__(self, filename: str, fieldnames: typing.List):
        try:    
            self.f = open(filename, 'w')
            self.writer = csv.DictWriter(
                self.f, fieldnames = fieldnames, delimiter=',')
            self.writer.writeheader()
        except FileNotFoundError as e:
            self.f = None
            self.writer = None
            # TODO: Log file not found error
            print(f"FileNotFoundError: {str(e)}.")
            raise e

    def __del__(self):
        if self.f:
            self.f.close()
    
    def write(self, row: typing.Dict):
        self.writer.writerow(row)
