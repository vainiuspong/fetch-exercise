# fetch-exercise

This is a technical exercise for Fetch hiring. I chose to use pandas as I thought it would be the quickest way to do scrappy data quality testing without a lot of setup. I also used LucidChart for my ERD since it is a software I've used for diagrams in the past. I used SnowSQL for the queries.

Given more time I would have liked to upload the schema files into a Postgres upload table. Then, use SQL and dbt to create dimension tables and new data model. I would have used Postgres's built-in ER diagram generator to create the diagram. Finally, I would have written data quality tests in dbt for each dimension table, and would have liked to use a tool like Elementary or Great Expectations to write more complex tests. I would have also liked to do some freshness and distribution tests.

I would also have preferred to send a Slack asking for a call rather than outlining all the details over text, since I've had the experience of business stakeholders not having enough time to read my message.