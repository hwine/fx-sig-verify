import pytest
import os
from fx_sig_verify.validate_moz_signature import Severity, \
                                                 MozSignedObjectViaLambda

# Currently defined values
expected_names = "Nothing, ProgramIssue, SuspectBinary".split(", ")


@pytest.fixture(scope='module', autouse=True)
def setup_environment():
    os.environ['VERBOSE'] = "2"


def test_constant_values():
    for i, attr_name in enumerate(expected_names):
        assert i == Severity.__dict__[attr_name]


def test_arn_configured():
    for i, attr_name in enumerate(expected_names):
        arn = Severity.get_ARN_env_var(i)
        assert arn is not None


def test_setting_severity_increase():
    obj = MozSignedObjectViaLambda()
    # we should always be able to raise severity, but not lower it
    # starts at Nothing
    expected_severity = None
    assert obj.severity == expected_severity
    for desired_severity in expected_names:
        expected_severity = Severity.__dict__[desired_severity]
        obj.set_severity(expected_severity)
        assert obj.severity == expected_severity
        # and check it doesn't go back down
        for lower_serverity in range(expected_severity, 0, -1):
            # try to lower
            obj.set_severity(lower_serverity)
            # shouldn't change
            assert obj.severity == expected_severity
