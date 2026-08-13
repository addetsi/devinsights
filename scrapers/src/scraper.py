"""Config-driven scraper engine that fetches GitHub data and publishes to Kafka"""

from pathlib import Path
from typing import Any

from scrapers.src.config import ScraperConfig, load_config
from scrapers.src.github_client import GitHubClient
from scrapers.src.logging_config import setup_logging
from scrapers.src.producer import GitHubProducer

logger = setup_logging()


class Scraper:
    """Orchestrates fetching configurred endpoints for each repo and publishes them"""

    def __init__(self, config: ScraperConfig) -> None:
        self.config = config
        self.client = GitHubClient(config.base_url)
        self.producer = GitHubProducer(
            bootstrap_servers=config.bootstrap_servers, topic=config.kafka_topic
        )

    def run(self) -> int:
        """Scrape all configurations endpoints for all repos. Returns messages published"""
        published = 0
        for repo in self.config.repositories:
            for endpoint in self.config.endpoints:
                path = endpoint.path.replace("{repo}", repo)
                try:
                    data = self.client.get(path)
                except Exception as err:
                    logger.error("Failed %s for %s: %s", endpoint.name, repo, err)
                    continue

                items = data if isinstance(data, list) else [data]
                for item in items:
                    message = self._build_message(repo, endpoint.message_type, item)
                    self.producer.publish(message, key=repo)
                    published += 1

                logger.info("Published %d messages for %s of %s", len(items), endpoint.name, repo)

        self.producer.flush()
        return published

    @staticmethod
    def _build_message(repo: str, message_type: str, data: Any) -> dict[str, Any]:
        """Wrap fetched data with metadata into a message envelope"""
        return {
            "message_type": message_type,
            "repo": repo,
            "data": data,
        }


def main() -> None:
    """Entry point: load config and run the scraper"""
    config_path = Path("scrapers/config/github_repos.yml")
    config = load_config(config_path)
    scraper = Scraper(config)
    count = scraper.run()
    logger.info("Scraping complete. Published %d messages", count)


if __name__ == "__main__":
    main()
