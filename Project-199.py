import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []

print("Server has started...")

questions = [
    "What is the Italian word for PIE \n a.Mozrella\n b.Pasty\n d.Pizza",
    "Water boils at 212 Units at which scale \n a.Fahrenheit\n b.Celsius\n c.Rankine\n d.Kelvin",
    "Which sea creature has three hearts \n a.Dolphin\n b.Octopus\n c.Walrs\n d.Seal",
    "Who was teh character famous in ouyr childhood rhymes associated with a lamg? \n a.Mary\n b.Jack\n c.Johnny\n d.Mukesh",
    "How many bones does an adult human have? \n a.206\n b.208\n c.201\n d.169.",
    "How  many wonders are there in the world \n a.7\n b.10\n c.8\n d.12",
    "What elemnt does not exist \n a.Xf\n b.Re\n c.Se\n d.Pa",
    "How many states are there in India? \n a.24\n b.29\n c.330\n d.31",
    "Who invented the telephbone? \n a.A.G. Bell\n b.John Wick\n c.Thomas\n d.G.Marconi"
    "Who is Loki? \n a.God of Thunder\n b.God of Dwarves\n c.God of Mischief\n d.God of Gods"
]

answers = [
    'a', 'a', 'b', 'a', 'a','a', 'a', 'b','a', 'c'
]

nicknames = []

def clientthread(conn):
    score = 0
    conn.send("Welcomne to the quiz game".encode("utf-8"))
    conn.send("You will receive a question. The answer to that sould be a, b, c or d".encode("utf-8"))
    conn.send("Good Luck!\n\n".encode("utf-8"))

    index, question, answer = get_random_questions(conn)

    while True:
        try: 
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode("utf-8"))
                else:

                    conn.send("INcorrect answer! Better".encode("utf-8"))
                    remove_questions(index)
                    index, question, answer = get_random_questions(conn)

        except:
            continue

def get_random_questions(conn):
    random_index = random.randit(0, len(questions)-1)
    random_question = questions[random_index]  
    random_answers = answers[random_index]

    conn.send(random_question.encode('utf-8'))

    return random_index, random_question, random_answers

def remove_questions(index):
    questions.pop(index)
    answers.pop(index)

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print(nickname + "Connected!")
    new_thread = Thread(target = clientthread, args=(conn, nickname))
    new_thread.start()