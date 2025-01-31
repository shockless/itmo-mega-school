from .roles.researcher import ITMOResearcher
import asyncio

from .json_serialization import JsonSerialization
from metagpt.config2 import Config
from pathlib import Path
import yaml


class Search:
    def __init__(
        self,
        config_path: Path,
        decomposition_nums: int = 3,
        url_per_query: int = 3,
    ):
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)
        self.metagpt_config = Config.from_llm_config(self.config["llm"])
        self.json_serialization = JsonSerialization(
            api_key=self.config["llm"]["api_key"], model=self.config["llm"]["model"]
        )
        self.decomposition_nums = decomposition_nums
        self.url_per_query = url_per_query

    async def get_answer(self, query, max_urls=3):
        summary = await self.get_summary(query)
        answer = await self.json_serialization.extract_json(
            query, summary, max_urls=max_urls
        )
        return answer

    async def get_summary(self, query):
        researcher = ITMOResearcher(
            decomposition_nums=self.decomposition_nums,
            url_per_query=self.url_per_query,
            config=self.metagpt_config,
        )
        msg = await researcher.run(query)
        return msg


if __name__ == "__main__":
    query = """
    В каком городе находится главный кампус Университета ИТМО?\n1. Москва\n2. Санкт-Петербург\n3. Екатеринбург\n4. Нижний Новгород
    """
    search = Search(
        config_path="config.yaml",
        api_key="sk-proj-0123456789012345678901234567890123456789012345678901234567890123",
    )
    print(asyncio.run(search.get_answer(query)))
