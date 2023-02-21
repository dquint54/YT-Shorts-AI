import csvfile as csvfile
import openai
import csv
import os

from twisted.python.util import println


def cooking_facts_generator():


        # Set your OpenAI API key
        openai.api_key = "************************************"

        # Generate cooking facts using OpenAI's GPT-3 API
        response = openai.Completion.create(
            engine="davinci",
            prompt="Generate 1 random cooking fact.",
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the generated facts from the OpenAI API response
        facts = [choice.text for choice in response.choices]

        # Create a CSV file to store the facts
        filename = "cooking_facts.csv"

        if not os.path.exists(filename):
            with open(filename, "w", newline="") as file:
                writer = csv.writer(file)
                print("File opened for writing")
                writer.writerow(["Cooking Facts"])

        # Append the facts to the CSV file
        with open(filename, "a") as file:
            writer = csv.writer(file)
            for fact in facts:
                print("fact appended to csv file")
                writer.writerow([fact])

