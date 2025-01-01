
import pygame
import random
import multiprocessing
from pygame import Surface


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 2
PADDLE_HEIGHT = 100
BALL_SIZE = 15
FPS = 80

WHITE = (255, 250, 250)
BLACK = (0, 1, 17)


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.choice([8, 10])

    def move(self, dy):
        self.y += dy
        if self.y < 0:
            self.y = 0
        elif self.y + PADDLE_HEIGHT > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - PADDLE_HEIGHT

    def get_position(self):
        return self.x, self.y


class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([3, -3])
        self.speed_y = random.choice([3, -3])

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y <= 0 or self.y >= SCREEN_HEIGHT - BALL_SIZE:
            self.speed_y = -self.speed_y

    def reset(self):
        self.__init__()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.paddle_left = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.paddle_right = Paddle(
            SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        self.score_left = 0
        self.score_right = 0

    def reset(self):
        self.paddle_left = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.paddle_right = Paddle(
            SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball.reset()

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (self.paddle_left.x,
                         self.paddle_left.y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (self.paddle_right.x,
                         self.paddle_right.y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.ellipse(self.screen, WHITE,
                            (self.ball.x, self.ball.y, BALL_SIZE, BALL_SIZE))

        font = pygame.font.Font(None, 36)
        score_text = font.render(
            f"{self.score_left} - {self.score_right}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 -
                         score_text.get_width() // 2, 20))

        pygame.display.flip()

    def update(self):
        self.ball.move()
        if self.ball.x <= self.paddle_left.x + PADDLE_WIDTH and self.paddle_left.y < self.ball.y < self.paddle_left.y + PADDLE_HEIGHT:
            self.ball.speed_x = -self.ball.speed_x
        elif self.ball.x >= self.paddle_right.x + PADDLE_WIDTH - BALL_SIZE and self.paddle_right.y < self.ball.y < self.paddle_right.y + PADDLE_HEIGHT:
            self.ball.speed_x = -self.ball.speed_x

    def get_state(self):
        return (self.ball.x, self.ball.y, self.paddle_left.y, self.paddle_right.y)

    def is_done(self):
        if self.ball.x < 0:
            self.score_right += 1
            return True
        elif self.ball.x > SCREEN_WIDTH:
            self.score_left += 1
            return True
        return False


def q_learning_agent(game_state, agent, action_space):
    ball_y = game_state[1]
    paddle_y = game_state[2] if agent == 'left' else game_state[3]

    if ball_y < paddle_y:
        return -1
    elif ball_y > paddle_y + PADDLE_HEIGHT:
        return 1
    return 0


def train_agent(agent_id, game_state_queue, action_queue, event):
    action_space = [-1, 0, 1]

    while True:
        event.wait()
        game_state = game_state_queue.get()
        action = q_learning_agent(game_state, agent_id, action_space)
        action_queue.put(action)


def main():
    game = Game()
    game_state_queue = multiprocessing.Queue()
    action_queue_left = multiprocessing.Queue()
    action_queue_right = multiprocessing.Queue()
    event_left = multiprocessing.Event()
    event_right = multiprocessing.Event()

    left_agent = multiprocessing.Process(target=train_agent, args=(
        'left', game_state_queue, action_queue_left, event_left))
    right_agent = multiprocessing.Process(target=train_agent, args=(
        'right', game_state_queue, action_queue_right, event_right))

    left_agent.start()
    right_agent.start()

    while True:
        game.reset()
        game_state_queue.put(game.get_state())
        event_left.set()
        event_right.set()

        while not game.is_done():
            try:
                action_left = action_queue_left.get_nowait()
            except:
                action_left = 0

            try:
                action_right = action_queue_right.get_nowait()
            except:
                action_right = 0

            if action_left == -1:
                game.paddle_left.move(-game.paddle_left.speed)
            elif action_left == 1:
                game.paddle_left.move(game.paddle_left.speed)

            if action_right == -1:
                game.paddle_right.move(-game.paddle_right.speed)
            elif action_right == 1:
                game.paddle_right.move(game.paddle_right.speed)

            game.update()
            game.draw()
            pygame.display.update()
            game_state_queue.put(game.get_state())

            event_left.clear()
            event_right.clear()

            event_left.set()
            event_right.set()

            game.clock.tick(FPS)

    left_agent.join()
    right_agent.join()


if __name__ == "__main__":
    main()
