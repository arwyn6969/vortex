import pytest
from hypothesis import settings, Verbosity
import tempfile
import os
from pathlib import Path

# Configure Hypothesis for property-based testing
settings.register_profile("dev", max_examples=10)
settings.register_profile("ci", max_examples=100, deadline=None)
settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)
settings.load_profile("dev")

@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture providing a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture(scope="session")
def benchmark_data_dir(test_data_dir):
    """Fixture providing a directory for benchmark data."""
    bench_dir = test_data_dir / "benchmarks"
    bench_dir.mkdir(exist_ok=True)
    return bench_dir

@pytest.fixture(autouse=True)
def setup_test_env():
    """Fixture to set up test environment variables."""
    original_env = dict(os.environ)
    os.environ["TESTING"] = "1"
    os.environ["VORTEX_ENV"] = "test"
    
    yield
    
    os.environ.clear()
    os.environ.update(original_env)

def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-slow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--run-integration", action="store_true", default=False, help="run integration tests"
    )

def pytest_collection_modifyitems(config, items):
    """Skip tests based on markers unless explicitly requested."""
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
                
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration) 