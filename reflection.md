# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
- Core Actions For User: Add a pet, add/edit tasks, generate today's schedule
- Main Objects Needed: Owner (name, and the pets they own, actions include adding pet, removing pet, adding/removing tasks, see today's tasks/schedule), Pet (name, age, etc, actions include changing basic info ), Task (type of task, duration, prioirity , actions include changing basic info ), Scheduler ( info includes the tasks, actions include generating schedule)


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
- Yes using AI, I improved my logic and cleaned it up. For example I put tasks under Pet:
  Owner
    fields:   name, pets[], available_hours (start/end time), preferences (dict or simple flags)
    actions:  add_pet, remove_pet, add_task(pet, task), remove_task(pet, task), get_todays_tasks()

  Pet
    fields:   name, age, species (or type), tasks[]
    actions:  update_info, add_task, remove_task

  Task
    fields:   task_type, duration (minutes), priority (1-5 or low/med/high), time_window (earliest, latest)
    actions:  update

  Scheduler
    fields:   owner
    actions:  generate_schedule() → list of (task, pet, start_time, reason)
              — uses owner.available_hours + task priorities + time_windows to slot tasks

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
