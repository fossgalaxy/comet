from django.test import TestCase

from fg_competitions.models import Competition, Track, Submission, SubmissionUpload

# Create your tests here.

GOOD = "succeded"
FAIL = "failed"
WIP = "in progress"

class PipelineTestCase(TestCase):
    """Tests for checking that the pipeline names work"""

    def setUp(self):

        self.params = (
            ("BP", GOOD, WIP, "pending"),
            ("BS", GOOD, GOOD, "pending"),
            ("BF", GOOD, FAIL, "skipped"),
            ("VP", GOOD, GOOD, WIP),
            ("VS", GOOD, GOOD, GOOD),
            ("VF", GOOD, GOOD, FAIL),
            ("DA", "bad", "bad", "bad")
        )


    def test_states(self):
        """check that when build status is pending, everything matches"""

        for param in self.params:
            upload = SubmissionUpload(status=param[0])

            self.assertEqual(upload.check_stage('upload'), param[1] )
            self.assertEqual(upload.check_stage('build'), param[2] )
            self.assertEqual(upload.check_stage('validate'), param[3] )

