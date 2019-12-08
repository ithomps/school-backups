from HashMap import HashMap, year_count


def main():
    student_info = [('Charlotte', 1997), ('Liam', 1999), ('Emma', 1999), ('William', 1998), ('Elijah', 1998),
                    ('Oliver', 1998), ('Isabella', 1998), ('Amelia', 1999), ('Mason', 1999), ('Sophia', 1999),
                    ('Mia', 2000),
                    ('Noah', 2000), ('Logan', 2000), ('James', 2001), ('Olivia', 2001), ('Benjamin', 2001),
                    ('Evelyn', 2001),
                    ('Ava', 2001), ('Jacob', 2002), ('Abigail', 2002)]
    input_hash = HashMap()
    for name, year in student_info:
        input_hash[name] = year

    year_hash = year_count(input_hash)
    for item in year_hash:
        print(item)

if __name__ == '__main__':
    main()
