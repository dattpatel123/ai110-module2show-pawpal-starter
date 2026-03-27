from dataclasses import dataclass, field
from datetime import time, datetime, timedelta
from typing import Optional


@dataclass
class Task:
    task_type: str
    duration: int           # in minutes
    priority: int           # 1 (low) to 5 (high)
    window_start: time = None
    window_end: time = None
    complete: bool = False

    def update(self, field_name: str, value) -> None:
        """Update a task attribute by name."""
        if not hasattr(self, field_name):
            raise AttributeError(f"Task has no attribute '{field_name}'")
        setattr(self, field_name, value)

    def set_complete(self, complete: bool = True) -> None:
        """Mark this task as complete or incomplete."""
        
        self.complete = True

@dataclass
class Pet:
    name: str
    age: int
    species: str
    tasks: list[Task] = field(default_factory=list)
    
    def update_info(self, name: str = None, age: int = None, species: str = None) -> None:
        """Update any combination of basic pet info."""
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if species is not None:
            self.species = species

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        if task not in self.tasks:
            raise ValueError(f"Task '{task.task_type}' not found for {self.name}")
        self.tasks.remove(task)

    def __str__(self) -> str:
        return f"{self.name} ({self.species}, age {self.age}) — {len(self.tasks)} task(s)"


class Owner:
    def __init__(self, name: str, available_start: time, available_end: time, preferences: dict = None):
        self.name = name
        self.pets: list[Pet] = []
        self.available_start = available_start
        self.available_end = available_end
        # Supported keys: "max_consecutive_minutes" (int)
        self.preferences: dict = preferences or {}

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's roster."""
        if pet in self.pets:
            raise ValueError(f"{pet.name} is already registered")
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's roster."""
        if pet not in self.pets:
            raise ValueError(f"{pet.name} is not registered")
        self.pets.remove(pet)

    def add_task(self, pet: Pet, task: Task) -> None:
        """Convenience method: add a task directly to one of the owner's pets."""
        if pet not in self.pets:
            raise ValueError(f"{pet.name} is not one of {self.name}'s pets")
        pet.add_task(task)

    def remove_task(self, pet: Pet, task: Task) -> None:
        """Convenience method: remove a task from one of the owner's pets."""
        if pet not in self.pets:
            raise ValueError(f"{pet.name} is not one of {self.name}'s pets")
        pet.remove_task(task)

    def get_todays_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all (pet, task) pairs across every registered pet."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]

    def available_minutes(self) -> int:
        """Total minutes between available_start and available_end."""
        start = datetime.combine(datetime.today(), self.available_start)
        end = datetime.combine(datetime.today(), self.available_end)
        return int((end - start).total_seconds() // 60)

    def __str__(self) -> str:
        return (
            f"Owner: {self.name} | "
            f"Available: {self.available_start.strftime('%H:%M')}–{self.available_end.strftime('%H:%M')} | "
            f"Pets: {len(self.pets)}"
        )


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self) -> list[tuple[Task, Pet, time, str]]:
        """
        Build a daily schedule for the owner's pets.

        Strategy:
          1. Collect every (pet, task) pair from the owner.
          2. Split into windowed tasks (hard time constraints) and flexible tasks.
          3. Sort both groups by priority descending.
          4. Slot windowed tasks first at their window_start; fill remaining
             slots with flexible tasks back-to-back within available hours.
          5. Skip any task that won't fit in remaining time and flag it.

        Returns list of (task, pet, start_time, reason) sorted by start_time.
        """
        all_tasks = self.owner.get_todays_tasks()
        if not all_tasks:
            return []

        print("Todays tasks:")
        for pet,task in all_tasks:
            print("Pet: ", pet.name)
            print("Task:", task.task_type)
            print()