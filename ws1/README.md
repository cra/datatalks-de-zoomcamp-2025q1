# Ingestion with dlt

[workshop description](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/workshops/dlt/dlt_homework.md)

## Notes on setup and walkthrough

Obviously, I used [uv](https://github.com/astral-sh/uv) for package management. I dislike Jupyter Noobebooks and prefer to avoid them whenever I can. **Due to that, most of the times that `df()` at the end of duckdb/dlt queries is actually redundant**. but I still added pandas to run it just in case

```bash
uv init
uv add dlt[duckdb]
uv run dlt --version
```

Whenever possible, I used [Makefile](./Makefile) targets to track questions
