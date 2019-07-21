import random
import string

days = ['Nov 12 2018 ', 'Nov 13 2018 ', 'Nov 14 2018 ']
s = ""


def random_string(string_length=10):
    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for _ in range(string_length))


def add_edge(mail1, mail2):
    global s
    s += mail1 + "," + mail2 + "," + days[random.randint(0, 10000) % len(days)] + str(random.randint(0, 23)).zfill(
        2) + ":" + str(random.randint(0, 59)).zfill(2) + ":" + str(random.randint(0, 59)).zfill(2) + "\n"


def generate_edges(data_size=1000000):
    emails = []
    f = open('nodes.csv', 'r')
    for line in f:
        x = line.split(",")
        emails.append(x[6].strip())

    for i in range(0, data_size):
        int_or_ext = random.randint(0, 100000000)
        if int_or_ext % 25 == 0:
            ext_email = random_string(8) + "@ext.com"
            int_email = emails[random.randint(0, 100000000) % len(emails)]
            if random.randint(0, 1000000) % 2 == 0:
                add_edge(int_email, ext_email)
            else:
                add_edge(ext_email, int_email)
        else:
            email1 = emails[random.randint(0, 100000000) % len(emails)]
            email2 = emails[random.randint(0, 100000000) % len(emails)]
            while email1 == email2:
                email2 = emails[random.randint(0, 100000000) % len(emails)]
            add_edge(email1, email2)

    f1 = open('edges.csv', 'w')
    f1.write(s)
    f1.close()



if __name__ == '__main__':
    generate_edges()
