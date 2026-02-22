PLANNING_PROMPT = [
    {
        "role": "system",
        "content": (
            "You are an expert research assistant. Your task is to break down a research topic into subtopics "
            "and determine how deep each subtopic should be explored."
        )
    },
    {
        "role": "user",
        "content": (
            "Topic: {topic}\n"
            "Mode: {mode}\n\n"
            "Instructions:\n"
            "- Generate a list of subtopics to research named subtopics\n"
            "- Determine depth_required (1=shallow, 3=deep).\n"
            "- Indicate if math is needed for understanding.\n"
            "- Indicate if sources are required.\n"
            "Output should match the ResearchPlan schema."
        )
    }
]

SYNTHESIS_PROMPT = [
    {
        "role": "system",
        "content": (
            "You are a research synthesis assistant. Your task is to summarize validated notes "
            "into a structured, concise report with references."
        )
    },
    {
        "role": "user",
        "content": (
            "Topic: {topic}\n"
            "Validated Notes:\n{validated_notes}\n\n"
            "Sources:\n{validated_sources}\n\n"
            "Instructions:\n"
            "- Summarize the notes into clear paragraphs.\n"
            "- Keep references at the end.\n"
            "- Output should be a single string suitable for a report."
            "- If the topic is related to math, include the math formulas and equations."
            """- Output should be:
             content: string
             confidence_score: float"""
        )
    }
]
