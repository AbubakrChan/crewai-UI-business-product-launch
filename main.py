import sys
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool

duckduckgo_search = DuckDuckGoSearchRun()


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
    )

    # Define Tasks
    task1 = Task(
        description=f"""Analyze the market demand for {product_name}. Current month is Jan 2024.
                        Write a report on the ideal customer profile and marketing 
                        strategies to reach the widest possible audience. 
                        Include at least 10 bullet points addressing key marketing areas.""",
        agent=market_research_analyst,
    )

    task2 = Task(
        description=f"""Assess the technological aspects of manufacturing 
                    high-quality {product_name}. Write a report detailing necessary 
                    technologies and manufacturing approaches. 
                    Include at least 10 bullet points on key technological areas.""",
        agent=technology_expert,
    )

    task3 = Task(
        description=f"""Summarize the market and technological reports 
                    and evaluate the business model for {product_name}. 
                    Write a report on the scalability and revenue streams 
                    for the product. Include at least 10 bullet points 
                    on key business areas. Give Business Plan, 
                    Goals and Timeline for the product launch. Current month is Jan 2024.""",
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


import re
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer))
            self.buffer = []


# # Redirect stdout to our custom stream
# sys.stdout = StreamToUI(st)


# sys.stdout = sys.__stdout__


# Streamlit interface
def run_crewai_app():
    st.title("CrewAI Business Product Launch")
    product_name = st.text_input("Enter a product name to analyze the market and business strategy.")

    if st.button("Run Analysis"):
        with st.expander("Processing!"):

            sys.stdout = StreamToExpander(st)
            with st.spinner("Generating Results"):
                crew_result = create_crewai_setup(product_name)

        st.header("Results:")
        st.markdown(crew_result)
        # Create an expander
        # with st.expander("Output"):
        #     # Redirect stdout to our custom stream
        # sys.stdout = StreamToExpander(st)


if __name__ == "__main__":
    run_crewai_app()

