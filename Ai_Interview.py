from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletions
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
import os
load_dotenv()
async def team_Config(job_position="Software Engineer"):
    model_client = OpenAIChatCompletions(model="gpt-4o", temperature=0, api_key= os.getenv("OPENAI_API_KEY"))
    

    job_position="Software Engineer"





    interviewer = AssistantAgent(
        name ="Interviewer"
        model_client=model_client,
        description =f"As an interviewer, you will assess the candidate's skills and fit for the {job_position} position."
        system_message = f'''
        You are a professional interviewer for a {job_position} position
        Ask on clear question at a time and wait for user to respond
        Ask3 questionas in total covering technical skills and experience , problem-solving abilities and cultural fit
        '''
    )

    interviewee = UserProxyAgent(
        name="Interviewee",
        model_client=model_client,
        description=f"As a candidate, you will showcase your skills and experience for the {job_position} position."
        system_message=f'''
        You are a candidate applying for a {job_position} position
        Answer the interviewer's questions clearly and concisely
        Provide examples from your experience to demonstrate your skills
        '''
    )

    career_coach = AssistantAgent(
        name="Career_coach"
        model_client=model_client,
        description=f"An AI agent that provides feedback and advice to candidates for a {job_position} position"
        system_message=f'''
        You are a career coach helping candidates prepare for a {job_position} position
        Provide constructive feedback on their interview performance
        Suggest areas for improvement and resources for further learning
        '''
    )

    termination_condition = TextMentionTermination(text="TERMINATE")

    team = RoundRobinGroupChat(
        participants=[interviewer, candidate,career_coach]
        termination_condition = TextMentionTermination("TERMINATE")
        max_turns=20
    )
    return team



async def interview(team):
    stream = team.run_stream(task="Conducting an interview fora software engineer position")


    async for message in team.run_stream(task='Start the interview with first question'):
        message = message.content
        yield message
        print(f"{message.sender.name}: {message.text}")')
    
async def main():
    job_position= 'Software Engineer'
    team = await team_Config
    
if __name__ =="__main__":
    import asyncio
    asyncio.run(main())
