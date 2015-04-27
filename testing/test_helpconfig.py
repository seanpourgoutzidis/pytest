import pytest

def test_version(testdir, pytestconfig):
    result = testdir.runpytest("--version")
    assert result.ret == 0
    #p = py.path.local(py.__file__).dirpath()
    result.stderr.fnmatch_lines([
        '*pytest*%s*imported from*' % (pytest.__version__, )
    ])
    if pytestconfig.pluginmanager._plugin_distinfo:
        result.stderr.fnmatch_lines([
            "*setuptools registered plugins:",
            "*at*",
        ])

def test_help(testdir):
    result = testdir.runpytest("--help")
    assert result.ret == 0
    result.stdout.fnmatch_lines("""
        *-v*verbose*
        *setup.cfg*
        *minversion*
        *to see*markers*py.test --markers*
        *to see*fixtures*py.test --fixtures*
    """)

def test_hookvalidation_unknown(testdir):
    testdir.makeconftest("""
        def pytest_hello(xyz):
            pass
    """)
    result = testdir.runpytest()
    assert result.ret != 0
    result.stderr.fnmatch_lines([
        '*unknown hook*pytest_hello*'
    ])

def test_hookvalidation_optional(testdir):
    testdir.makeconftest("""
        import pytest
        @pytest.hookimpl_opts(optionalhook=True)
        def pytest_hello(xyz):
            pass
    """)
    result = testdir.runpytest()
    assert result.ret == 0

def test_traceconfig(testdir):
    result = testdir.runpytest("--traceconfig")
    result.stdout.fnmatch_lines([
        "*using*pytest*py*",
        "*active plugins*",
    ])

def test_debug(testdir, monkeypatch):
    result = testdir.runpytest("--debug")
    assert result.ret == 0
    p = testdir.tmpdir.join("pytestdebug.log")
    assert "pytest_sessionstart" in p.read()

def test_PYTEST_DEBUG(testdir, monkeypatch):
    monkeypatch.setenv("PYTEST_DEBUG", "1")
    result = testdir.runpytest()
    assert result.ret == 0
    result.stderr.fnmatch_lines([
        "*pytest_plugin_registered*",
        "*manager*PluginManager*"
    ])
