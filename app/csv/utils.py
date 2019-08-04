import csv
import os


class CsvWriter:

    school_field_names = ['Name', 'Phone', 'Address']
    prepended_file_name = 'output/'

    @staticmethod
    def write_list(writer, data):
        if data is not None:
            for d in data:
                writer.writerow(d)

    @staticmethod
    def from_list(file_name='schools.csv', data=None):
        full_file_name = CsvWriter.prepended_file_name + file_name
        if os.path.exists(full_file_name):
            file_handle = open(full_file_name, 'a', newline='')
        else:
            file_handle = open(full_file_name, 'w', newline='')

        writer = csv.DictWriter(file_handle, fieldnames=CsvWriter.school_field_names)

        if file_handle.mode == 'w':
            writer.writeheader()

        CsvWriter.write_list(writer, data)
        file_handle.close()
