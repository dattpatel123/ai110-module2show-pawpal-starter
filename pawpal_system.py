from dataclasses import dataclass, field
from datetime import time
from typing import Optional


@dataclass
class Task:
    task_type: str
    duration: int          # in minutes
    priority: int          # 1 (low) to 5 (high)
    window_start: Optional[time] = None
    window_end: Optional[time] = None

    def update(self, field_name: str, value) -> None:
        pass


@dataclass
class Pet:
    name: str
    age: int
    species: str
    tasks: list[Task] = field(default_factory=list)

    def update_info(self, name: str = None, age: int = None, species: str = None) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass


class Owner:
    def __init__(self, name: str, available_start: time, available_end: time, preferences: dict = None):
        self.name = name
        self.pets: list[Pet] = []
        self.available_start = available_start
        self.available_end = available_end
        self.preferences: dict = preferences or {}

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, pet: Pet, task: Task) -> None:
        pass

    def remove_task(self, pet: Pet, task: Task) -> None:
        pass

    def get_todays_tasks(self) -> list[tuple[Pet, Task]]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self) -> list[tuple[Task, Pet, time, str]]:
        """
        Returns a list of (task, pet, start_time, reason) tuples.
        Scheduling logic:
          1. Collect all tasks across owner's pets
          2. Apply hard constraints (time windows, available hours)
          3. Sort by priority
          4. Slot tasks back-to-back within available hours
          5. Attach a reason string to each scheduled item
        """
        pass
