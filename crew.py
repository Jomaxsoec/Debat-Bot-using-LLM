import requests
import yaml
from crewai import Agent, Task, Crew, Process,LLM
from crewai.project import CrewBase, agent, task, crew

with open("debat/config/agents.yaml", "r") as f:
    agents_config = yaml.safe_load(f)

with open("debat/config/tasks.yaml", "r") as f:
    tasks_config = yaml.safe_load(f)

ollama_llm = LLM(
    model="llama3.2",  # 👈 make sure this matches exactly what you see in `ollama list`
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # dummy, required by CrewAI's LLM wrapper
)
for name, config in agents_config.items():
    if config.get("llm") == "ollama":
        config["llm"] = ollama_llm

# === CrewAI Setup ===
@CrewBase
class Debate():
    """Debate crew"""


    agents_config = 'debat/config/agents.yaml'
    print(agents_config.raw())
    tasks_config = 'debat/config/tasks.yaml'


    @agent
    def debater(self) -> Agent:
        return Agent(
            config=self.agents_config['debater'],
            verbose=True
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config['judge'],
            verbose=True
        )

    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config['propose'],
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config['oppose'],
        )

    @task
    def decide(self) -> Task:
        return Task(
            config=self.tasks_config['decide'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
