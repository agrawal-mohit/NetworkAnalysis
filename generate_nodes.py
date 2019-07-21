import random
import string

area = ['Delhi', 'Pune', 'Mumbai', 'Pune', 'Hyderabad', 'Bangalore']
teams = ['Sales', 'Operations', 'Technical']
positions = ['Executive', 'Manager', 'Region Head']
sex = ['F', 'M']


def random_string(string_length=10):
    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for _ in range(string_length))


def random_index(mod):
    return random.randint(0, 10000000) % mod


all_emails = []


def generate_nodes(data_size):
    i = 0
    s = ""
    while i < data_size:
        f_name = random_string(random.randint(3, 10))
        s_name = random_string(random.randint(3, 7))
        while f_name + "." + s_name in all_emails:
            s_name = random_string(random.randint(3, 7))
        email = f_name + "." + s_name
        all_emails.append(email)
        s += str(i) + "," + \
            f_name + " " + s_name + "," + \
            sex[random_index(len(sex))] + "," + \
            positions[random_index(len(positions))] + "," + \
            area[random_index(len(area))] + "," + \
            teams[random_index(len(teams))] + "," + \
            email + "@company.com\n"
        i += 1
    f = open('nodes.csv', 'w')
    f.write(s)
    f.close()

if __name__ == '__main__':
    generate_nodes()
    