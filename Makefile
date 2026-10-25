.PHONY: bench

PLUGIN_DIR ?= ../okular-mupdf-ng
BENCH_BUILD_DIR ?= bench/build
BENCH_ARGS ?= --manifest corpus/manifest.json

bench:
	@uv sync --project bench --locked
	@cmake -S bench -B "$(BENCH_BUILD_DIR)" -DCMAKE_BUILD_TYPE=Release -DPython3_EXECUTABLE="$(abspath bench/.venv/bin/python)"
	@cmake --build "$(BENCH_BUILD_DIR)" --parallel
	@ctest --test-dir "$(BENCH_BUILD_DIR)" --output-on-failure
	@uv run --project bench --locked python bench/run.py --source-dir "$(PLUGIN_DIR)" --harness "$(BENCH_BUILD_DIR)/okular-bench" $(BENCH_ARGS)
