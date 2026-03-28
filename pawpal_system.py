from dataclasses import dataclass, field
from datetime import time, datetime, timedelta
from typing import Optional


@dataclass
class Task:
    task_type: str
    duration: int           # in minutes
    priority: int           # 1 (low) to 5 (high)
    scheduled_time: time = None
    recurrence: str = None          # "daily", "weekly", "monthly", or None (one-time)
    complete: bool = False
    last_completed: datetime = None  # tracks when recurring tasks were last done
    window_start: time = None
    window_end: time = None

    def update(self, field_name: str, value) -> None:
        """Update a task attribute by name."""
        if not hasattr(self, field_name):
            raise AttributeError(f"Task has no attribute '{field_name}'")
        setattr(self, field_name, value)

    def set_complete(self, complete: bool = True) -> None:
        """Mark this task as complete. For recurring tasks, records the completion date."""
        self.complete = complete
        if complete and self.recurrence:
            self.last_completed = datetime.now()

    def is_due_today(self) -> bool:
        """Return True if this task is due today based on recurrence and last completion."""
        today = datetime.today().date()
        if self.recurrence is None:
            return not self.complete
        if self.last_completed is None:
            return True
        last = self.last_completed.date()
        if self.recurrence == "daily":
            return today >= last + timedelta(days=1)
        if self.recurrence == "weekly":
            return today >= last + timedelta(weeks=1)
        if self.recurrence == "monthly":
            return today >= last + timedelta(days=30)
        return True

@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
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

    def get_pet_by_name(self, name: str) -> Optional[Pet]:
        """Return a pet by name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None
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
        all_tasks = [(pet, task) for pet in self.pets for task in pet.tasks]
        if not all_tasks:
            return []

        return  [(pet, task) for pet, task in all_tasks if task.is_due_today()]

   


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
    def generate_schedule(self) -> list[tuple[Task, Pet, time, str]]:
        """Build a daily schedule using each task's scheduled_time, sorted by time then priority."""
        all_tasks = self.owner.get_todays_tasks()
        if not all_tasks:
            return []

        pending = [(pet, task) for pet, task in all_tasks if task.is_due_today()]

        # Sort by scheduled_time (None last), then priority descending
        pending.sort(key=lambda x: (x[1].scheduled_time is None, x[1].scheduled_time, -x[1].priority))

        # Lightweight conflict detection: flag tasks that share the same scheduled_time
        seen_times = {}  # scheduled_time -> first task that claimed it
        results = []
        for pet, task in pending:
            reason = f"priority {task.priority}"
            if task.scheduled_time is not None:
                if task.scheduled_time in seen_times:
                    reason += f" ⚠️ conflict with '{seen_times[task.scheduled_time]}'"
                else:
                    seen_times[task.scheduled_time] = task.task_type
            results.append((task, pet, task.scheduled_time, reason))
        return results
    def filter_by_completion(self, complete: bool) -> list[tuple[Pet, Task]]:
        """Return all (pet, task) pairs filtered by completion status."""
        return [
            (pet, task)
            for pet in self.owner.pets
            for task in pet.tasks
            if task.complete == complete
        ]
    def filter_by_pet(self, pet_name: str) -> list[tuple[Pet, Task]]:
        """Return all (pet, task) pairs for a given pet name."""
        return [
            (pet, task)
            for pet in self.owner.pets
            if pet.name == pet_name
            for task in pet.tasks
        ]
    def print_schedule(self):
        """Print the generated schedule in a readable format."""
        schedule = self.generate_schedule()
        if not schedule:
            print("No tasks scheduled.")
            return

        print(f"\n{'='*55}")
        print(f"  Daily Schedule for {self.owner.name}")
        print(f"{'='*55}")
        for task, pet, start, reason in schedule:
            time_str = start.strftime('%H:%M') if start else "No time"
            print(f"  {time_str:15}  {task.task_type:20} ({pet.name})")
            print(f"  {'':15}  ↳ {reason}")
        print(f"{'='*55}\n")