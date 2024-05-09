import sys
import time
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
import os
import re

# NOTE: to find which model names you have, use cli tool:  `ollama list`
llm = ChatOpenAI(
      model='llama2',
      base_url="http://localhost:11434/v1",
      api_key="NA"
    )

duckduckgo_search = DuckDuckGoSearchRun()

#to keep track of tasks performed by agents
task_values = []

def create_crewai_setup(product_name):
    # Define Agents
    market_research_analyst = Agent(
        role="Market Research Analyst",
        goal=f"""Analyze the market demand for {product_name} and 
                 suggest marketing strategies""",
        backstory=f"""Expert at understanding market demand, target audience, 
                      and competition for products like {product_name}. 
                      Skilled in developing marketing strategies 
                      to reach a wide audience.""",
        verbose=True,
        allow_delegation=True,
        tools=[duckduckgo_search],
        llm=llm,
    )

    technology_expert = Agent(
        role="Technology Expert",
        goal=f"Assess technological feasibilities and requirements for producing high-quality {product_name}",
        backstory=f"""Visionary in current and emerging technological trends, 
                      especially in products like {product_name}. 
                      Identifies which technologies are best suited 
                      for different business models.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
    )

    business_consultant = Agent(
        role="Business Development Consultant",
        goal=f"""Evaluate the business model for {product_name}, 
               focusing on scalability and revenue streams""",
        backstory=f"""Seasoned in shaping business strategies for products like {product_name}. 
                      Understands scalability and potential 
                      revenue streams to ensure long-term sustainability.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
    )


    # Define Tasks
    task1 = Task(
        description=f"""Analyze the market demand for {product_name}. Current month is Jan 2024.
                        Write a report on the ideal customer profile and marketing 
                        strategies to reach the widest possible audience. 
                        Include at least 10 bullet points addressing key marketing areas.""",
        expected_output="Report on market demand analysis and marketing strategies.",
        agent=market_research_analyst,
    )
    # Define Task 2
    task2 = Task(
        description=f"""Assess the technological aspects of manufacturing 
                    high-quality {product_name}. Write a report detailing necessary 
                    technologies and manufacturing approaches. 
                    Include at least 10 bullet points on key technological areas.""",
        expected_output="Report on technological aspects of manufacturing.",
        agent=technology_expert,
    )
    # Define Task 3
    task3 = Task(
        description=f"""Summarize the market and technological reports 
                    and evaluate the business model for {product_name}. 
                    Write a report on the scalability and revenue streams 
                    for the product. Include at least 10 bullet points 
                    on key business areas. Give Business Plan, 
                    Goals and Timeline for the product launch. Current month is Jan 2024.""",
        expected_output="Report on business model evaluation and product launch plan.",
        agent=business_consultant,
    )

    # Create and Run the Crew
    product_crew = Crew(
        agents=[market_research_analyst, technology_expert, business_consultant],
        tasks=[task1, task2, task3],
        verbose=2,
        process=Process.sequential,
    )

    crew_result = product_crew.kickoff()
    return crew_result

#display the console processing on streamlit UI
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary

            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "Market Research Analyst" in cleaned_data:
            # Apply different color 
            cleaned_data = cleaned_data.replace("Market Research Analyst", f":{self.colors[self.color_index]}[Market Research Analyst]")
        if "Business Development Consultant" in cleaned_data:
            cleaned_data = cleaned_data.replace("Business Development Consultant", f":{self.colors[self.color_index]}[Business Development Consultant]")
        if "Technology Expert" in cleaned_data:
            cleaned_data = cleaned_data.replace("Technology Expert", f":{self.colors[self.color_index]}[Technology Expert]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

# Streamlit interface
def run_crewai_app():
    st.title("AI Agent Business Product Launch")
    with st.expander("About the Team:"):
        st.subheader("Diagram")
        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
            st.image("my_img.png")

        st.subheader("Market Research Analyst")
        st.text("""       
        Role = Market Research Analyst
        Goal = Analyze the market demand for {product_name} and suggest marketing strategies
        Backstory = Expert at understanding market demand, target audience, 
                    and competition for products like {product_name}. 
                    Skilled in developing marketing strategies 
                    to reach a wide audience.
        Task = Analyze the market demand for {product_name}. Current month is Jan 2024.
               Write a report on the ideal customer profile and marketing 
               strategies to reach the widest possible audience. 
               Include at least 10 bullet points addressing key marketing areas. """)
        
        st.subheader("Technology Expert")
        st.text("""       
        Role = Technology Expert
        Goal = Assess technological feasibilities and requirements for producing high-quality {product_name}
        Backstory = Visionary in current and emerging technological trends, 
                    especially in products like {product_name}. 
                    Identifies which technologies are best suited 
                    for different business models. 
        Task = Assess the technological aspects of manufacturing 
               high-quality {product_name}. Write a report detailing necessary 
               technologies and manufacturing approaches. 
               Include at least 10 bullet points on key technological areas.""")

        st.subheader("Business Development Consultant")
        st.text("""       
        Role = Business Development Consultant 
        Goal= Evaluate the business model for {product_name}
              focusing on scalability and revenue streams
        Backstory = Seasoned in shaping business strategies for products like {product_name}. 
                    Understands scalability and potential 
                    revenue streams to ensure long-term sustainability.
        Task = Summarize the market and technological reports 
               and evaluate the business model for {product_name}. 
               Write a report on the scalability and revenue streams 
               for the product. Include at least 10 bullet points 
               on key business areas. Give Business Plan, 
               Goals and Timeline for the product launch. Current month is Jan 2024. """)
    
    product_name = st.text_input("Enter a product name to analyze the market and business strategy.")

    if st.button("Run Analysis"):
        # Placeholder for stopwatch
        stopwatch_placeholder = st.empty()
        
        # Start the stopwatch
        start_time = time.time()
        with st.expander("Processing!"):
            sys.stdout = StreamToExpander(st)
            with st.spinner("Generating Results"):
                crew_result = create_crewai_setup(product_name)

        # Stop the stopwatch
        end_time = time.time()
        total_time = end_time - start_time
        stopwatch_placeholder.text(f"Total Time Elapsed: {total_time:.2f} seconds")

        st.header("Tasks:")
        st.table({"Tasks" : task_values})

        st.header("Results:")
        st.markdown(crew_result)

if __name__ == "__main__":
    run_crewai_app()
