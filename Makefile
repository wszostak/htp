.PHONY: tests venv

tests:
	@pytest

tests-cov:
	@coverage run
	@coverage report

clean:
	@rm -rf .coverage
	@rm -rf coverage_html_report
	@rm -rf .pytest_cache
	@rm -rf build