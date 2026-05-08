install:
	uv sync

dev:
	uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.13 langgraph dev --allow-blocking
