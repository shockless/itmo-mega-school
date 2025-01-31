from openai import AsyncOpenAI

from metagpt.schema import Message
from pydantic import BaseModel, Field
from typing import List, Optional


class QuestionAnswer(BaseModel):
    answer: Optional[int] = Field(
        description="The correct choice number from the list of answer options. If the user query does NOT contain any numbered choices return None."
    )
    reasoning: str = Field(description="Reasoning information from markdown")
    sources: List[str] = Field(
        description="List of sources used to answer the question, in format [url1, url2, url3]"
    )


class JsonSerialization:
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = """you are a smart assistant that solve user problems. Return only fields that exist in the text. 
        Pay attention to all the information provided in the text, such as dates, numbers, etc.
        If the user query contains numbered choices, return the correct choice number in the answer field. Else return None in the answer field.
        Even if the answer is number, if the user query does not contain any numbered choices, return None in the answer field.
        """

    async def extract_entities(self, user_text: str):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {"role": "user", "content": user_text},
        ]

        response = await self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=QuestionAnswer,
            temperature=0.1,
            max_tokens=500,
        )

        result_from_gpt = response.choices[0].message.parsed

        json_result = result_from_gpt.model_dump()
        for key in json_result:
            if key == "answer":
                if isinstance(json_result[key], str):
                    json_result[key] = (
                        int(json_result[key]) if json_result[key].isdigit() else -1
                    )
                if json_result[key] == -1:
                    json_result[key] = None
        return json_result

    async def extract_json(self, question_answers, summary: Message, max_urls=3):
        user_prompt = f"Here is a query from user: {question_answers}\n\n and here is a summary of sources: {summary.instruct_content.content}, used urls: {summary.instruct_content.urls}. If the user query contains numbered choices, return the correct choice number in the answer field. Else return None in the answer field. Even if the answer is number, if the user query does not contain any numbered choices, return None in the answer field."
        answer_json = await self.extract_entities(user_prompt)
        answer_json["reasoning"] = (
            summary.instruct_content.content
            + "\n"
            + "Сгенерированно с помощью модели {}".format(self.model)
        )
        answer_json["sources"] = summary.instruct_content.urls[:max_urls]
        return answer_json
