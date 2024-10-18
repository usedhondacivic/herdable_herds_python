"""
Sample simulation / world setup for playing with herdable agents

pyglet documentation:
https://github.com/pyglet/pyglet/tree/master
"""

from abc import ABC, abstractmethod
from typing import List
import random
import math
import pyglet

HERD_AGENT_SIZE = 2
SHEPARD_AGENT_SIZE = 2

PIXELS_PER_METER = 10

WINDOW_SIZE_PIXELS = (640, 480)
WINDOW_SIZE_METERS = (
    WINDOW_SIZE_PIXELS[0] / PIXELS_PER_METER,
    WINDOW_SIZE_PIXELS[1] / PIXELS_PER_METER,
)


class Agent(ABC):
    def __init__(
        self,
        x: float,
        y: float,
        heading: float,
        vel: float,
        batch: pyglet.graphics.Batch,
    ):
        """
        Init a kinematic agent
        x, y: position (m)
        heading: angle (rad)
        vel: velocity in direction of heading (m/s)
        batch: used for rendering graphics
        """
        self.loc = [x, y, heading]
        self.vel = vel
        self.batch = batch

    @abstractmethod
    def update(
        self, shepards: List["HerdAgent"], herd: List["ShepardAgent"], dt: float
    ):
        """
        Update the agent
        """
        pass

    @abstractmethod
    def draw(self):
        """
        Draw the agent
        """
        pass


class HerdAgent(Agent):
    def __init__(self, x, y, heading, vel, batch):
        super().__init__(x, y, heading, vel, batch)
        self.shape = pyglet.shapes.Circle(
            x, y, HERD_AGENT_SIZE, color=(0, 255, 255), batch=batch
        )

    def update(
        self, shepards: List["HerdAgent"], herd: List["ShepardAgent"], dt: float
    ):
        for shepard in shepards:
            # do something to influence motion
            pass

        for sheep in herd:
            if sheep == self:
                # ignore self
                continue
            # do something to influence motion
            pass

        self.loc[0] += math.cos(self.loc[2]) * self.vel * dt
        self.loc[1] += math.sin(self.loc[2]) * self.vel * dt

    def draw(self):
        self.shape.x = self.loc[0] * PIXELS_PER_METER
        self.shape.y = self.loc[1] * PIXELS_PER_METER


class ShepardAgent(Agent):
    def __init__(self, x, y, heading, vel, batch):
        super().__init__(x, y, heading, vel, batch)
        self.shape = pyglet.shapes.Circle(
            x, y, SHEPARD_AGENT_SIZE, color=(255, 0, 0), batch=batch
        )

    def update(
        self, shepards: List["HerdAgent"], herd: List["ShepardAgent"], dt: float
    ):
        self.loc[0] += math.cos(self.loc[2]) * self.vel * dt
        self.loc[1] += math.sin(self.loc[2]) * self.vel * dt

    def draw(self):
        self.shape.x = self.loc[0] * PIXELS_PER_METER
        self.shape.y = self.loc[1] * PIXELS_PER_METER


class World:
    def __init__(self):
        self.window = pyglet.window.Window(*WINDOW_SIZE_PIXELS, "Herds!")
        self.main_batch = pyglet.graphics.Batch()
        self.fps_counter = pyglet.window.FPSDisplay(window=self.window)

        self.herd: List[HerdAgent] = []
        for _ in range(100):
            self.herd.append(
                HerdAgent(
                    random.uniform(0, WINDOW_SIZE_METERS[0]),
                    random.uniform(0, WINDOW_SIZE_METERS[1]),
                    random.uniform(0, 2 * math.pi),
                    random.uniform(0, 2),
                    self.main_batch,
                )
            )
        self.shepards: List[ShepardAgent] = [
            ShepardAgent(
                random.uniform(0, WINDOW_SIZE_METERS[0]),
                random.uniform(0, WINDOW_SIZE_METERS[1]),
                random.uniform(0, 2 * math.pi),
                random.uniform(0, 2),
                self.main_batch,
            )
        ]

    def draw(self):
        """
        Draw the world
        """
        self.window.clear()

        for agent in self.herd + self.shepards:
            agent.draw()
        self.main_batch.draw()

        self.fps_counter.draw()

    def step(self, dt):
        """
        Step the simulation
        """
        for agent in self.herd + self.shepards:
            agent.update(self.herd, self.shepards, dt)


if __name__ == "__main__":
    world = World()

    @world.window.event
    def on_draw():
        world.draw()

    pyglet.clock.schedule_interval(world.step, 1 / 120.0)
    pyglet.app.run()
