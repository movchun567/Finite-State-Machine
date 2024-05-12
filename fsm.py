"""Finite State Machine"""

import random

def prime(fn):
    """wrapper"""
    def wrapper(*args, **kwargs):
        u = fn(*args, **kwargs)
        u.send(None)
        return u
    return wrapper

class FSM:
    """FSM class"""
    def __init__(self):
        """init"""
        self.start = self._create_start()
        self.SLEEP = self._create_sleep()
        self.EAT = self._create_eat()
        self.STUDY = self._create_study()
        self.RELAX = self._create_rest()
        self.DIE = self._create_die()

        self.hunger = 10.0
        self.exhaustion = 10.0
        self.sanity = 10.0

        self.current_state = self.start
        self.stopped = False


    def send(self, hour):
        """The function sends the curretn input to the current state
        It captures the StopIteration exception and marks the stopped flag.
        """
        try:
            
            if self.current_state != self.SLEEP:
                self.hunger -= 1
            if self.exhaustion and self.sanity and self.hunger:
                self.current_state.send(hour)
            else:
                cause_of_death = []
                if self.hunger <= 0:
                    cause_of_death.append('starvation')
                if self.exhaustion <= 0:
                    cause_of_death.append('exhaustion')
                if self.sanity <= 0:
                    cause_of_death.append('insanity')
                print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                print(f'You died of {", ".join(cause_of_death)}...')
                self.current_state = self.DIE
        except StopIteration:
            self.stopped = True

    def does_match(self):
        """The function at any point in time returns if till the current input
        the string matches the given regular expression.

        It does so by comparing the current state with the end state `DIE`.
        It also checks for `stopped` flag which sees that due to bad input the iteration of FSM had to be stopped.
        """
        if self.stopped:
            return False
        return self.current_state == self.DIE

    @prime
    def _create_start(self):
        """start"""
        while True:
            hour = yield
            if hour == 0:
                self.current_state = self.SLEEP

    @prime
    def _create_sleep(self):
        """honk mi mi mi..."""
        while True:
            hour = yield
            print("Sleeping... Honk mi mi mi...")
            luck = random.randint(0, 100)
            
            if luck > 5 or self.exhaustion > 6:
                if hour in [5, 6] and luck < 30:
                    print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                    print('Yawn... Good morning! You feel sleepy and want to eat.')
                    self.exhaustion -= 2
                    self.sanity -= 2
                    self.current_state = self.EAT
                elif hour == 7 and luck < 30:
                    print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                    print('Yawn... Good morning! You want to eat.')
                    self.current_state = self.EAT
                elif hour in [8, 9, 10, 11] and luck < 30:
                    print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                    print('Yawn... You slept too long! You skip your breakfast, because you need to study...')
                    self.sanity -= 3
                    self.exhaustion -= 3
                    self.current_state = self.STUDY
            else:
                print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                print("You can't wake up... You died in your sleep.")
                self.current_state = self.DIE

    @prime
    def _create_eat(self):
        """nom nom nom..."""
        while True:
            hour = yield
            luck = random.randint(0, 100)
            if luck % 39 != 1:
                if hour in [8, 9]:
                    food = ['cereal', 'toast', 'eggs', 'bacon', 'pancakes', 'waffles']
                    random.shuffle(food)
                    breakfast = food.pop()
                    print(f'You eat {breakfast} for breakfast...')
                    match breakfast:
                        case 'cereal':
                            self.hunger += 1
                            self.exhaustion += 0
                        case 'toast':
                            self.hunger += 2
                            self.exhaustion += 0
                        case 'eggs':
                            self.hunger += 3
                            self.exhaustion += 1
                        case 'bacon':
                            self.hunger += 1
                            self.exhaustion += 1
                        case 'pancakes':
                            self.hunger += 2
                            self.exhaustion -= 1
                        case 'waffles':
                            self.hunger += 4
                            self.exhaustion += 1
                    if hour == 9:
                        print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                        print('You feel full and ready to start studying...')
                        self.current_state = self.STUDY

                elif hour in [15, 16]:
                    food = ['sandwich', 'salad', 'soup', 'pasta', 'burger', 'pizza']
                    random.shuffle(food)
                    lunch = food.pop()
                    print(f'You eat {lunch} for lunch...')
                    match lunch:
                        case 'sandwich':
                            self.hunger += 2
                            self.exhaustion += 0
                        case 'salad':
                            self.hunger += 1
                            self.exhaustion += 1
                        case 'soup':
                            self.hunger += 2
                            self.exhaustion += 1
                        case 'pasta':
                            self.hunger += 3
                            self.exhaustion += 0
                        case 'burger':
                            self.hunger += 4
                            self.exhaustion -= 2
                        case 'pizza':
                            self.hunger += 5
                            self.exhaustion -= 2
                    if hour == 16:
                        print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                        print('You feel full and now you wanna relax...')
                        self.current_state = self.RELAX

                elif hour in [19, 20, 21]:
                    food = ['shrimps', 'steak', 'sushi', 'chicken', 'tacos', 'ramen']
                    random.shuffle(food)
                    dinner = food.pop()
                    print(f'You eat {dinner} for dinner...')
                    match dinner:
                        case 'shrimps':
                            self.hunger += 3
                            self.exhaustion += 0
                        case 'steak':
                            self.hunger += 4
                            self.exhaustion += 0
                        case 'sushi':
                            self.hunger += 2
                            self.exhaustion += 0
                        case 'chicken':
                            self.hunger += 3
                            self.exhaustion += 0
                        case 'tacos':
                            self.hunger += 4
                            self.exhaustion -= 1
                        case 'ramen':
                            self.hunger += 1
                            self.exhaustion -= 1
                    if hour == 21:
                        print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                        print('You feel full and now you wanna sleep...')
                        self.current_state = self.SLEEP
            else:
                print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                print('You choked on your food... You died.')
                self.current_state = self.DIE
                

    @prime
    def _create_study(self):
        """:( ..."""
        while True:
            hour = yield
            if hour in [10, 11, 12, 13, 14]:
                luck = random.randint(0, 100)
                if luck < 5 and self.exhaustion < 6 and self.sanity < 6:
                    print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                    print('You had brain aneurysm... You died.')
                    self.current_state = self.DIE
                else:
                    lessons = ['Programming', 'Calculus', 'Discrete Math', 'History', 'English']
                    random.shuffle(lessons)
                    lesson = lessons.pop()
                    print(f'You study {lesson}...')
                    match lesson:
                        case 'Programming':
                            self.sanity += 0
                            self.exhaustion -= 2
                        case 'Calculus':
                            self.sanity -= 1
                            self.exhaustion -= 1
                        case 'Discrete Math':
                            self.sanity -= 2
                            self.exhaustion -= 2
                        case 'History':
                            self.sanity -= 2
                            self.exhaustion += 2
                        case 'English':
                            self.sanity += 3
                            self.exhaustion += 3
                    if hour == 14:
                        print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                        print('You feel smart and tired... You wanna eat...')
                        self.current_state = self.EAT
                

    @prime
    def _create_rest(self):
        """rock n roll..."""
        while True:
            hour = yield
            if hour in [17, 18, 19]:
                check = True
                luck = random.randint(0, 100)
                activities = ['listen to music', 'read a book', 'watch a movie', 'go for a walk']
                random.shuffle(activities)
                activity = activities.pop()
                print(f'You want to {activity}...')
                match activity:
                    case 'listen to music':
                        music = ['Dehumanized - Prophecies Foretold', 'Green River - Rehab Doll', 'Kendrick Lamar - good kid, m.A.A.d city', 'The Beatles - Abbey Road', 'Cypress Hill - Cypress Hill']
                        random.shuffle(music)
                        album = music.pop()
                        print(f'You listen to {album}...')
                        if album == 'Kenrick Lamar - good kid, m.A.A.d city':
                            self.sanity -= 5
                            self.exhaustion -= 5
                            print('You hated it...')
                        else:
                            self.sanity += 2
                            self.exhaustion += 2
                            print('You loved it...')
                    case 'read a book':
                        books = ['H. P. Lovecraft - The Call of Cthulhu', 'George Orwell - 1984', 'J. R. R. Tolkien - The Hobbit', 'Franz Kafka - The Metamorphosis']
                        random.shuffle(books)
                        book = books.pop()
                        print(f'You read {book}...')
                        if book == 'H. P. Lovecraft - The Call of Cthulhu':
                            self.sanity -= 5
                            self.exhaustion -= 0
                            print('You liked it, but your sanity is not okay...')
                            if luck < 20:
                                print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                                print("You went insane. You read something you can't comprehend... You died...")
                                self.current_state = self.DIE
                        else:
                            self.sanity += 3
                            self.exhaustion += 1
                            print('You loved it...')
                    case 'watch a movie':
                        movies = ['Avengers', 'Pulp Fiction', 'The Shawshank Redemption', 'Lobster', 'Oldboy']
                        random.shuffle(movies)
                        movie = movies.pop()
                        print(f'You watch {movie}...')
                        if movie == 'Avengers':
                            self.sanity -= 5
                            self.exhaustion -= 5
                            print('You hated it...')
                        else:
                            self.sanity += 1
                            self.exhaustion += 2
                            print('You loved it...')
                    case 'go for a walk':
                        print('You go for a walk...')
                        self.sanity += 3
                        self.exhaustion += 0
                        if luck < 10:
                            print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                            print('You got mugged in Sykhiv... You died.')
                            check = False
                            self.current_state = self.DIE
                if check:
                    print(f'Hour: {hour}, Hunger: {self.hunger}, Exhaustion: {self.exhaustion}, Sanity: {self.sanity}')
                    print('You feel relaxed and hungry... You wanna eat...')
                    self.current_state = self.EAT

    @prime
    def _create_die(self):
        """RIP..."""
        while True:
            hour = yield

    def begin(self):
        """begin"""
        curr = 0
        while True:
            self.send(curr % 24)
            if self.does_match():
                break
            curr += 1

if __name__ == '__main__':
    fsm = FSM()
    fsm.begin()
