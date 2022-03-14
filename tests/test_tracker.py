# Unit tests related to 'Trackers' (https://www.easypost.com/docs/api#tracking).

import pytest

import easypost


@pytest.mark.vcr()
def test_tracker_values():

    for code, status in (
        ("EZ1000000001", "pre_transit"),
        ("EZ2000000002", "in_transit"),
        ("EZ3000000003", "out_for_delivery"),
        ("EZ4000000004", "delivered"),
        ("EZ5000000005", "return_to_sender"),
        ("EZ6000000006", "failure"),
        ("EZ7000000007", "unknown"),
    ):
        tracker = easypost.Tracker.create(tracking_code=code)
        assert tracker.status == status
        assert tracker.tracking_details != []
        if status == "delivered":
            assert tracker.signed_by == "John Tester"


@pytest.mark.vcr()
def test_tracker_interactions(per_run_unique):
    # create a pseudo-random tracking code so that we can run multiple instances of this test in parallel
    tracking_code = "EP{0}".format(per_run_unique)

    # Create a tracker and then retrieve it. We assert on created and retrieved tracker's values.
    tracker = easypost.Tracker.create(
        tracking_code=tracking_code,
        carrier="usps",
        options=dict(
            full_test_tracker=True,
        ),
    )
    assert tracker.id  # This is random

    # retrieve tracker by id
    tracker2 = easypost.Tracker.retrieve(tracker.id)

    assert tracker2.id == tracker.id  # Should be the same as above

    # retrieve all trackers by tracking_code
    trackers = easypost.Tracker.all(tracking_code=tracking_code)

    assert len(trackers["trackers"])
    assert trackers["trackers"][0].id == tracker.id == tracker2.id  # Should be the same as the ids above

    # create another test tracker
    tracker3 = easypost.Tracker.create(
        tracking_code=tracking_code,
        carrier="USPS",
        options=dict(
            full_test_tracker=True,
        ),
    )

    assert tracker3.id

    # retrieve all created since 'tracker'
    trackers2 = easypost.Tracker.all(after_id=tracker.id, tracking_code=tracking_code)

    # assert len(trackers2["trackers"]) == 1  this is ignored because the number can vary depending on the user account
    assert trackers2["has_more"] is not None
    assert trackers2["trackers"][0].id == tracker3.id  # Should be the same as the id for tracker3


@pytest.mark.vcr()
def test_tracker_create_list():
    """Tests that we can create a list of trackers in bulk."""
    success = easypost.Tracker.create_list(
        {
            "0": {"tracking_code": "EZ1000000001"},
            "1": {"tracking_code": "EZ2000000002"},
            "2": {"tracking_code": "EZ3000000003"},
            "3": {"tracking_code": "EZ4000000004"},
        }
    )

    # This endpoint/method does not return anything, just make sure the request doesn't fail
    assert success is True
