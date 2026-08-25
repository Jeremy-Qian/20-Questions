import json
import os
import random


class TwentyQuestionsAI:
    def __init__(self):
        self.data_file = "people_data.json"
        self.people_data = self.load_people_data()
        # Questions relevant to guessing people
        self.questions = [
            "Is this person male?",
            "Is this person female?",
            "Does he/she torture others?",
            "Does he/she like to say 'bruh' a lot?",
            "Does he/she like Les Mis?",
            "Is he/she Chinese?",
            "Is he/she very tall?",
            "Does this person have glasses?",
            "Does this person have Google Chat?",
            "Does this person come to the Ramp only on Sundays?",
            "Does this person live near the Ramp?(<2km)",
            "Does this person's name start with 'J'?",
            "Is this person a student/former student at VSA?",
            "Is this person a student/former student at TPS?",
            "Is this person a student/former student at CHA?",
            "Does this person's name start with 'D'?",
            "Does this person have a middle name?",
            "If there were 1. People Talking; 2. Fewer people playing soccer, would this person choose 2?",
            "Did he attend both 2024 and 2025 5K 10K races?",
            "Is this person one of the best at soccer? (Is he one of Joshua, David, Hudson, Nissi?)",
            "Does this person/this person's family have a pet cat?",
            "Is this person a former Bandit?",
            "Is this person one of the three Mosquitoes?",
        ]
        self.question_count = 0
        self.max_questions = 20
        self.answers = {}

    def list_people_in_database(self):
        """List all people in the database."""
        if not self.people_data:
            print("\n❌ The database is empty.")
            return

        print("\n📋 People in the database:")
        for i, person in enumerate(sorted(self.people_data.keys()), 1):
            print(f"  {i}. {person}")

    def ask_question(self, question):
        """Ask a question and get yes/no/unknown response"""
        print(f"\n🤔 Question {self.question_count}: {question}")

        while True:
            response = input("Your answer (yes/no/unknown/quit): ").strip().lower()
            if response in ["yes", "no", "unknown", "quit"]:
                return response
            print("❌ Please answer with 'yes', 'no', 'unknown', or 'quit'")

    def load_people_data(self):
        """Load people data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                return json.load(f)
        else:
            # Default data if file doesn't exist
            return {}

    def save_people_data(self):
        """Save people data to JSON file"""
        with open(self.data_file, "w") as f:
            json.dump(self.people_data, f, indent=2)

    def calculate_similarity(self, person_answers):
        """Calculate similarity between user answers and person's answers"""
        score = 0
        total_questions = 0

        for question, user_answer in self.answers.items():
            if question in person_answers and user_answer != "unknown":
                total_questions += 1
                if person_answers[question] == user_answer:
                    score += 1

        return score / total_questions if total_questions > 0 else 0

    def find_most_similar_person(self):
        """Find the most similar person based on user answers"""
        if not self.people_data:
            return None, 0.0

        max_similarity = -1
        most_similar_person = None

        for person, answers in self.people_data.items():
            similarity = self.calculate_similarity(answers)
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_person = person

        return most_similar_person, max_similarity

    def make_guess(self):
        """Make a guess about what person the player is thinking"""
        person, similarity = self.find_most_similar_person()
        if not person:
            return False

        print(f"\n🎯 My guess: Is it {person}?")

        response = input("Am I right? (yes/no): ").strip().lower()
        if response == "yes":
            return True
        else:
            # Ask if player wants to add the correct person to the database
            add_to_db = (
                input(
                    "Would you like to add the correct person to my database? (yes/no): "
                )
                .strip()
                .lower()
            )
            if add_to_db == "yes":
                correct_person = input("What is the name of the person? ").strip()
                if correct_person not in self.people_data:
                    self.people_data[correct_person] = {}
                    # Start with existing answers from the game
                    self.people_data[correct_person] = self.answers.copy()

                    # Ask questions that weren't answered or were answered 'unknown'
                    for question in self.questions:
                        if (
                            question not in self.people_data[correct_person]
                            or self.people_data[correct_person][question] == "unknown"
                        ):
                            print(f"\nQuestion about {correct_person}: {question}")
                            while True:
                                answer = (
                                    input(
                                        "What's the correct answer (yes/no/unknown): "
                                    )
                                    .strip()
                                    .lower()
                                )
                                if answer in ["yes", "no", "unknown"]:
                                    break
                                print("❌ Please answer with 'yes', 'no', or 'unknown'")
                            self.people_data[correct_person][question] = answer
                    self.save_people_data()
                    print(f"\n✅ {correct_person} has been added to my database!")
            return False

    def play(self):
        """Play the 20 Questions game focusing on people"""
        print("=" * 60)
        print("🎮 Welcome to 20 QUESTIONS AI! (People Edition) 🎮")
        print("=" * 60)
        print("\n📋 How to play:")
        print("  1. Think of a Rampion")
        print("  2. I'll ask you up to 20 yes/no questions")
        print("  3. Answer honestly with:  yes, no, or unknown")
        print("  4. I'll try to guess who you're thinking of!\n")
        print(f"Number of people in database: {len(self.people_data)}")
        user_input = (
            input(
                "Press Enter when you've thought of a person, or type 'list' to see all people in the database: "
            )
            .strip()
            .lower()
        )

        if user_input == "list":
            self.list_people_in_database()
            input("\nPress Enter to start the game...")

        # Ask questions
        random.shuffle(self.questions)
        question_list = self.questions[: self.max_questions]

        for i, question in enumerate(question_list):
            self.question_count = i + 1

            response = self.ask_question(question)

            if response == "quit":
                print("\n👋 Thanks for playing!  Goodbye!")
                return

            self.answers[question] = response

        # Make final guess
        print("\n" + "=" * 60)
        print("🎯 TIME FOR MY FINAL GUESS!")
        print("=" * 60)

        # Find the most similar person
        guessed_correctly = self.make_guess()

        if not guessed_correctly:
            print("\n❌ I couldn't guess it correctly.")

        play_again = input("\n🔄 Play again? (yes/no): ").strip().lower()
        if play_again == "yes":
            self.__init__()  # Reset the game
            self.play()
        else:
            print("\n👋 Thanks for playing! Goodbye!")


def main():
    """Main entry point"""
    game = TwentyQuestionsAI()
    game.play()


if __name__ == "__main__":
    main()
