# Engineering Task Manager MCP Server

An AI client can create and find engineering tasks and update their status through
the official Python MCP SDK. SQLite persists tasks across client sessions.
This is a local, single-user stdio server, not a hosted service.

## Development workflow

Clone the development branch and enter the repository before running the setup
commands below:

```bash
git clone --branch develop https://github.com/Saikiran-12-git/ai-engineering-portfolio.git
cd ai-engineering-portfolio
```

For an existing clone, commit or stash any local edits before switching branches:

```bash
git fetch origin
git switch develop
git pull --ff-only origin develop
```

Make changes on `develop`, run the storage tests and MCP smoke test, and push to
`develop`. When the changes are ready, open a pull request from `develop` to
`main`. GitHub Actions runs the project checks on pushes and pull requests.

## Run and verify

Python 3.12 is the tested runtime. From this project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python smoke_test.py
```

On Windows activate with `.venv\Scripts\activate` instead.
The requirements allow compatible SDK v1 releases; the tested version is 1.30.0.

The smoke test starts a server subprocess and performs MCP initialization,
tool discovery, creation, search, missing-ID error handling, and resource reading.
It uses a temporary database and leaves no demo tasks behind.

## Connect an MCP client

Add the following server entry to your client's MCP configuration, replacing both
paths with absolute paths on your computer. Windows paths need JSON escaping.

```json
{
  "mcpServers": {
    "engineering-tasks": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/server.py"],
      "env": {"TASK_DB": "/absolute/path/to/data/tasks.db"}
    }
  }
}
```

Example requests:

- Create a task titled "Review Java 21 migration" with description "Check dependencies."
- Find tasks containing "Java".
- Mark task 1 as in_progress, then done.
- Read tasks://recent.

You can also run `python server.py`, but it waits for MCP messages rather than
showing an interactive terminal prompt.

## Architecture and decisions

MCP client → stdio protocol → typed tools → TaskStore → SQLite.

`server.py` defines tools and resource contracts; `store.py` owns transactions,
validation, SQL queries, and connection lifetime. Each operation closes its
connection. SQL uses bound parameters; literal substring search treats `%` and
`_` as characters. Results are bounded to prevent unbounded context growth.
No arbitrary SQL, shell execution, deletion tool, or model credentials are exposed.
Tools propagate errors to the SDK so clients can distinguish failure from success.

Status values are todo, in_progress, and done. Any transition between these is
allowed. Recent tasks are ordered by creation ID, not last update.

## Limitations and next improvements

There is no authentication or tenant isolation; use only as a trusted local process.
The task contents are untrusted data and should not become model instructions.
This version has bounded substring search, not semantic search or pagination.
SQLite can serialize concurrent writes; this is a portfolio-scale task store.
Future improvements: audit events, pagination, idempotent task creation, and
concurrency tests before expanding into a hosted service.

## Interview explanation

"I separated the MCP protocol layer from storage so I could test business rules
without a model. I used typed tool schemas, bound SQL parameters, bounded results,
and explicit missing-task errors. My protocol smoke test uses a real MCP client
and subprocess, so it verifies more than calling Python functions directly."

Reference: https://github.com/modelcontextprotocol/python-sdk/tree/v1.x
