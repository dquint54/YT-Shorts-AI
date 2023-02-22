import csvfile as csvfile
import openai
import csv
import os
import Variables



def facts_generator():
    # Set your OpenAI API key

    openai.api_key = Variables.api_key
    filename = "cooking_facts.csv"
    prompt = Variables.prompt

    # Generate cooking facts using OpenAI's GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=20,
        n=1,
        stop=None,
        temperature=0.75,
    )

    # Extract the generated facts from the OpenAI API response
    fact = response.choices[0].text.strip()

    existing_facts = read_existing_facts_from_csv(filename)

    if check_similarity(fact, existing_facts):
        print("Fact too similar to existing fact. Skipping...")
        return

    # Create a CSV file to store the facts

    if not os.path.exists(filename):
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            print("File opened for writing")
    else:
        # Append the facts to the CSV file
        with open(filename, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([fact])
            print("Fact written to file:", fact)


def check_similarity(fact, existing_facts, threshold=0.8):
    for existing_fact in existing_facts:
        # Calculate the similarity score between the two facts
        try:
            similarity_score = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Similarity between \"{fact}\" and \"{existing_fact}\".",
                temperature=1,
                max_tokens=32,
                n=1,
                stop=None
            ).choices[0].text.strip()

            if similarity_score == "There is no similarity between the two sentences.":
                continue
            # Convert the similarity score to a float
            similarity_score = float(similarity_score)

            # Check if the similarity score is above the threshold
            if similarity_score >= threshold:
                return True
        except ValueError:

            return False

    return False


def read_existing_facts_from_csv(filename):
    # Check if the file exists
    if not os.path.exists(filename):
        # Return an empty list if the file does not exist
        return []

    # Read the existing facts from the CSV file
    existing_facts = []
    with open(filename, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            existing_facts.append(row[0])

    return existing_facts


def main():

    for i in range(20):
        facts_generator()


if __name__ == '__main__':
    main()
