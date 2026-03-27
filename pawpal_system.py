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

class Owner:
    def __init__(self, name: str, preferences: dict = None):
        self.name = name
        self.pets: list[Pet] = []
        
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

   


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self) -> list[tuple[Task, Pet, time, str]]:
        """
        Build a daily schedule for the owner's pets.

        Assumptions (all tasks always have these):
          - window_start / window_end  : hard time bounds for the task
          - duration                   : how long the task takes (minutes)
          - priority                   : 1 (low) – 5 (high)
          - complete                   : skip already-done tasks

        Strategy:
          1. Drop completed tasks.
          2. Sort remaining by window_start, break ties by priority (high first).
          3. Walk through tasks in order. Place each task at window_start if
             the slot is free; otherwise push it to the earliest free minute
             still inside the window. If it no longer fits, mark as SKIPPED.
          4. Return list of (task, pet, start_time, reason) sorted by start_time,
             with SKIPPED entries (start_time=None) at the end.
        """
        all_tasks = self.owner.get_todays_tasks()
        if not all_tasks:
            return []

        # 1. Drop completed tasks
        pending = [
            (pet, task) for pet, task in all_tasks if not task.complete
        ]

        # 2. Sort by window_start, then priority descending
        pending.sort(key=lambda x: (x[1].window_start, -x[1].priority))

        scheduled: list[tuple[Task, Pet, time, str]] = []
        skipped:   list[tuple[Task, Pet, time, str]] = []

        # Track occupied intervals as (start_dt, end_dt)
        occupied: list[tuple[datetime, datetime]] = []
        today = datetime.today()

        def to_dt(t: time) -> datetime:
            return datetime.combine(today, t)

        def first_free_slot(earliest: datetime, duration_min: int, deadline: datetime) -> datetime | None:
            """Return the earliest start >= earliest where [start, start+duration) is free."""
            cursor = earliest
            task_len = timedelta(minutes=duration_min)
            while cursor + task_len <= deadline:
                end = cursor + task_len
                conflict = next(
                    (s for s, e in occupied if s < end and e > cursor), None
                )
                if conflict is None:
                    return cursor
                # Jump past the conflicting block
                cursor = next(e for s, e in occupied if s < end and e > cursor)
            return None  # doesn't fit

        # 3. Schedule each task
        for pet, task in pending:
            window_s = to_dt(task.window_start)
            window_e = to_dt(task.window_end)

            slot = first_free_slot(window_s, task.duration, window_e)
    
            if slot is None:
                reason = (
                    f"SKIPPED — could not fit {task.duration}min inside "
                    f"{task.window_start.strftime('%H:%M')}–{task.window_end.strftime('%H:%M')}"
                )
                skipped.append((task, pet, None, reason))
                continue

            slot_end = slot + timedelta(minutes=task.duration)
            occupied.append((slot, slot_end))
            occupied.sort()  # keep sorted for the conflict check

            reason = (
                f"priority {task.priority} | "
                f"window {task.window_start.strftime('%H:%M')}–{task.window_end.strftime('%H:%M')}"
            )
            scheduled.append((task, pet, slot.time(), reason))

        # 4. Sort scheduled by start time, append skipped at end
        scheduled.sort(key=lambda x: x[2])
        return scheduled + skipped

    def display_schedule(self) -> None:
        """Print the generated schedule in a readable format."""
        schedule = self.generate_schedule()
        if not schedule:
            print("No tasks scheduled.")
            return

        print(f"\n{'='*55}")
        print(f"  Daily Schedule for {self.owner.name}")
        print(f"{'='*55}")
        for task, pet, start, reason in schedule:
            if start:
                end_dt = datetime.combine(datetime.today(), start) + timedelta(minutes=task.duration)
                time_str = f"{start.strftime('%H:%M')}–{end_dt.time().strftime('%H:%M')}"
            else:
                time_str = "SKIPPED"
            print(f"  {time_str:15}  {task.task_type:20} ({pet.name})")
            print(f"  {'':15}  ↳ {reason}")
        print(f"{'='*55}\n")