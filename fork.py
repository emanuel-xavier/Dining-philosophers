import multiprocessing
import random
import time

############## INITIALIZATION BEGIN ##############

n = 5 # number of philosophers
names = ['Philosofer 1', 'Philosofer 2', 'Philosofer 3', 'Philosofer 4', 'Philosofer 5']
chopsticks = multiprocessing.Array('i', [0, 0, 0, 0, 0])
dishes_is_full = multiprocessing.Array('i', [1, 1, 1, 1, 1])

############## INITIALIZATION END ##############

############### FUNCTIONS BEGIN ###############

def right (num): # get the right philosophers index
    return (num + 1) % n

def left (num): # get the left philosophers index
    return num #(num + n - 1) % n

def eat (pos, dishes_is_full, lock): # the philosophers start to eat
    with lock:
        print(names[pos] + ' is eating...')
    
    time.sleep(random.randint(3, 5)) # each philosopher takes between 3 and 5 seconds to eat
    dishes_is_full[pos] = 0 # set the philosophers dish as empty
    with lock:
        print(names[pos] + ' is satisifed.')

def think (pos, lock):
    with lock:
        print(names[pos] + ' is thinking...')
    time.sleep(random.randint(5, 7)) # each philosopher takes between 5 and 7 seconds to think

def philosopher (pos, dishes_is_full, chopsticks):
    lock = multiprocessing.Lock()

    while dishes_is_full[pos] == 1: # while there is food in the dish
        with lock:
            if chopsticks[left(pos)] == 0: # if the left chopsticks is avaliable
                chopsticks[left(pos)] = pos + 1 # pick up the chopsticks
            if chopsticks[right(pos)] == 0: # if the right chopsticks is avaliable
                chopsticks[right(pos)] = pos + 1 # pick up the chopsticks

        if chopsticks[left(pos)] == pos + 1: # if the philosopher have the left sticker
            if chopsticks[right(pos)] == pos + 1: # if the philosopher have the right sticker
                eat(pos, dishes_is_full, lock)
                chopsticks[right(pos)] = 0 # drop the right chopsticks
                chopsticks[left(pos)] = 0 # drop the left chopsticks
            else: 
                chopsticks[right(pos)] = 0 # drop the left chopsticks
                with lock:
                    print(names[pos] + ' could not eat, the right chopstick was unavaliable.')
                think(pos, lock)
        else: 
            with lock:
                print(names[pos] + ' could not eat, the left chopstick was unavaliable.')
            think(pos, lock)

############### FUNCTIONS END ################

if __name__ == '__main__':
    processes = []

    for pos in range (n):
        process = multiprocessing.Process(target=philosopher, args=(pos, dishes_is_full, chopsticks,))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print('All the philosophers are satisfied.')
    time.sleep(5)