# for 'fail' cases, they should be reported to SNS always

import boto3
import os
from moto import mock_s3, mock_sns, mock_sqs
import pytest

from fx_sig_verify.validate_moz_signature import (lambda_handler, )  # noqa: E402


@mock_s3
@mock_sns
@mock_sqs
def test_fail_message_when_not_verbose(set_verbose_false,
                                       bad_files, setup_aws_mocks,
                                       create_bucket):
    queue = setup_aws_mocks
    bucket = create_bucket
    # Given that VERBOSE is not set
    for falsey in set_verbose_false:
        falsey()
        # WHEN a bad file is processed
        for fname in bad_files:
            upload_file(bucket, fname)
            event = build_event(bucket.name, fname)
            response = lambda_handler(event, dummy_context)
            # THEN there should be a message
            count, msg = get_one_message(queue)

            # print things that will be useful to debug
            print("response:", response)
            print("message:", msg)
            print("count:", count)

            # actual criteria to pass
            assert "fail" in response['results'][0]['status']
            assert count is 1 and msg.startswith('fail for')


@mock_s3
@mock_sns
@mock_sqs
def test_fail_message_when_verbose(set_verbose_true, bad_files,
                                   setup_aws_mocks, create_bucket):
    queue = setup_aws_mocks
    bucket = create_bucket
    # Given that VERBOSE is set
    for truthy in set_verbose_true:
        truthy()
        # WHEN a bad file is processed
        for fname in bad_files:
            upload_file(bucket, fname)
            event = build_event(bucket.name, fname)
            response = lambda_handler(event, dummy_context)
            print("response:", response)
            # THEN there should be a message
            count, msg = get_one_message(queue)
            print("message:", msg)
            assert "fail" in response['results'][0]['status']
            assert count is 1 and msg.startswith('fail for')
