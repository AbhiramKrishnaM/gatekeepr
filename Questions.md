# Questions

March 11 

1. Should i keep typing the dev start command eg:- fastapi dev. is there some simplified way like we type server run ?

Ans:
    Created a Makefile. Now you can use:
    - `make run` or `make dev` instead of `fastapi dev` 

March 12

2. So my understanding is like this. When user types some kind of change or some query to the llm, our agent blocks the transfer to llm, it checks and does its calculations and sees if it needs to be passed to the llm or not. We assign some kind of score to the current query right ?. Now if the score is bad we ask the user to rephrase it also giving some insights. If its good we pass that to the llm and llm does the changes is this what we are trying to build ?

Ans:
    Whats actually happening 
        The actual flow
            1. User sends a query → Worker Agent (LLM) processes it
            2. Worker Agent decides on an action (e.g., "delete user 2's data")
            3. Guardian intercepts the action before it executes
            4. Guardian evaluates:
                Step A: Check JSON Policy rules (fast, rule-based)
                Step B: LLM risk scoring (0.0 to 1.0)
            5. Guardian returns:
                Score < 0.4: Allow (action proceeds)
                Score 0.4–0.7: Rewrite (suggest safer version)
                Score > 0.7: Block (alert human)
