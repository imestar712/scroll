__author__ = 'ict'

import os

from DAL.driver.base import Base


class CSV(Base):
    def __init__(self, file=None):
        Base.__init__(self)
        self.file = file

    def load(self, file=None):
        if file is None:
            file = self.file
        if file is None:
            raise Exception("Need input file name")
        if not os.path.isfile(file):
            raise FileNotFoundError("No such file: " + file)
        self.tag = file.lower().split(os.path.sep)[-1].replace(".csv", "")
        with open(file, "r") as csv_fp:
            buff = csv_fp.read()
        self.data = []
        if "\r\n" in buff:
            buff_list = buff.split("\r\n")
        else:
            buff_list = buff.split("\n")
        for item in buff_list:
            if len(item) == 0:
                continue
            item_list = item.split(",")
            tmp_list = []
            for each in item_list:
                while True:
                    if len(each) == 0:
                        break
                    if each[0] == " ":
                        each = each[1:]
                    if each[-1] == " ":
                        each = each[:-1]
                    if each[0] != " " and each[-1] != " ":
                        break
                if len(each) != 0:
                    if each[0] == "\"" and each[-1] == "\"":
                        tmp_list.append(each[1:-1])
                    else:
                        tmp_list.append(each)
            self.data.append(tmp_list)
        self.loaded = True

    def save(self, dal_driver, file=None):
        if file is None:
            file = self.file
        if file is None:
            raise Exception("Need input file name")
        loaded = True
        if not dal_driver.done():
            dal_driver.load()
            loaded = False
        data = dal_driver.get_data()
        if not loaded:
            dal_driver.clean()
        with open(file, "w", newline="\n") as csv_fp:
            for item in data:
                for i in range(len(item)):
                    item[i] = str(item[i])
                csv_fp.write(",".join(item) + "\n")