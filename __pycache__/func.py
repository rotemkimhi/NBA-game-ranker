from dbm import error
import csv

def count_word(filename, word):
    count = 0
    try:
        with open(filename, 'r') as f:
            for line in f:
                if word in line:
                    count += 1
        return count
    except error as e:
        print(f"error with file {filename}:{e}")

def average_column(filename, index):
    total, count = 0, 0
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                total += float(row[index])
                count += 1
            return total /count if count > 0 else 0
    except error as e:
        print(f"file not good {filename}: {e}")

def count_occurrences(filename):
    dic  = {}
    file = open(filename, 'r')
    for line in file:
        for word in line.split():
            dic[word] = dic.get(word, 0) + 1
    file.close()
    return dic

def tester(filename):
    total_num = 0
    passed_num = 0
    failed = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                total_num += 1
                if "PASS" in line:
                    passed_num += 1
                else:
                    failed.append(line.split()[0])
    except error as e:
        print(f"error with file {filename}: {e}")
    print(f"Total tests run: {total_num}/n Tests passed: {passed_num}/n Tests failed: {total_num-passed_num}/n Failed tests: {', '.join(failed)}")



