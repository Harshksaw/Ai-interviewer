
from AI_interview import team_Config, interview
import asyncio


async def main():
    job_position= 'Software Engineer'
    team = await team_Config(job_position)
    
    async for returnMsg in interview(team):
        print(message)    
    
    
if __name__ =="__main__":

    asyncio.run(main())
