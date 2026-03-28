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
- Yes using AI, I improved my logic and cleaned it up. For example, I put pets under owner, gave availible hours, and preferences for owner. For tasks, I added a time_window which tells the window to schedule tasks. And scheduler now just takes Owner itself and generates schedule using Owner object which has all info. This all simplfies the program and makes it easier to understand naturally:
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

- My scheduler considered the time and priority when deciding how to schedule the tasks. I think these two made sense since both are important in scheduling the tasks. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
- One tradeoff it makes it that it only schedules exact times that we wanted. For example, it does not consider a window of time that the task can be done. So an 8am task must be done at that time and 9 am must be done at 9am, even though the tasks could be scheduled closer together if they don't last too long. I think it's reasonable in this scenario since it's only a basic scheduling app and it would add a lot of complexity as we would need to consider the next open time blocks and considering conflicts with previously scheduled tasks as well. 
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

- I used Claude to help me plan my outline and the classes before coding. I made sure to properly outline exactly how I wanted it so that I wouldn't code wrongly from the start. And throughout the project, I made sure to use it to debug or understand the code it wrote. It helped a lot in refactoring as new features were added throughout the assignment. The most helpful ones were asking it to fix small features at a time instead of something big all at one. Like I would tell it to implement completion logic, or add a basic sorting.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
- I did not accept it's suggestion for window-start and window-end. Initially I accepted it because I thought we needed to make the program complex with adding the window of time our task can be done. However, overtime I saw the assignment only cared about the specific start time so I stopped using it. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

- I tested adding a owner, adding pets, adding tasks, and generating a schedule. These make sense because that's the core functionality of the program. We should be able to creates tasks and generate schedules. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
- The scheduler works pretty well as long as the times don't overlap. This again goes into my design decision where I only chose to sort by the time itself and priority, not considering time windows OR schedule tasks earlier if a previous one is done early. 
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
- The basic functionality I'm proud that I was able to solve. I was able to add tasks, create pets, and generate schedules. However, I do feel the project could be improved greatly but there was a lot of open ended choices to make which made it difficult to decide about how to go about it.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
- I would definitely consider working on the recurring tasks and making sure that works. I would also make it so that it doesn't have to schedule at the exact start time. We could give it a window of time we want to schedule and it would schedule as many tasks together as possible.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
- One important thing I learned was that having a proper system designed early is helpful when making changes. Because it makes it easier to change stuff around as long as your main objects and stuff are properly defined. I had to constantly change and add new fields and functions but having a well defined design made it much easier to work with. Not to mention GitHub copilot autocompletion was doing well at predicting what I needed to write as I wrote.