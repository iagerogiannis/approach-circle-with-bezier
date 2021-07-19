import os


class ScvExporter:

    def __init__(self, fname, path="", delimeter=";"):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.fname = r"{}/{}.csv".format(path, fname)
        self.delimeter = delimeter

    def create_csv(self):
        with open(self.fname, "w") as myfile:
            pass

    def write_headers(self, *headers_titles):
        headers_line = ""
        for headers_title in headers_titles:
            headers_line += headers_title + self.delimeter
        headers_line += "\n"

        with open(self.fname, "a") as myfile:
            myfile.write(headers_line)

    def append_row(self, *contents):
        contents_line = ""
        for content in contents:
            contents_line += str(content) + self.delimeter
        contents_line += "\n"

        with open(self.fname, "a") as myfile:
            myfile.write(contents_line)

    def new_line(self):
        self.append_row(self.fname, "")

    def table_to_csv(self, table):
        with open(self.fname, "a") as myfile:
            for row in table:
                contents_line = ""
                for content in row:
                    contents_line += str(content) + self.delimeter
                contents_line += "\n"
                myfile.write(contents_line)
