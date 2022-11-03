import pytest

from commitdb.postgres import PostgresCommitDB, parse_connect_string, DB_CONNECT_STRING
from datamodel.commit import Commit, make_from_dict, make_from_raw_commit
from git.git import Git


@pytest.fixture
def setupdb():
    db = PostgresCommitDB()
    db.connect()
    db.reset()
    return db


def test_save_lookup(setupdb: PostgresCommitDB):
    #    setupdb.connect(DB_CONNECT_STRING)
    commit = Commit(
        commit_id="42423b2423",
        repository="https://fasfasdfasfasd.com/rewrwe/rwer",
        timestamp=121422430,
        hunks=1,
        message="Some random garbage",
        diff=["fasdfasfa", "asf90hfasdfads", "fasd0fasdfas"],
        changed_files=["fadsfasd/fsdafasd/fdsafafdsa.ifd"],
        message_reference_content=[],
        jira_refs={},
        ghissue_refs={"hggdhd": ""},
        cve_refs=["simola3"],
        tags=["tag1"],
    )
    setupdb.save(commit.to_dict())
    result = setupdb.lookup(
        "https://fasfasdfasfasd.com/rewrwe/rwer",
        "42423b2423",
    )

    retrieved_commit = Commit.parse_obj(result[0])
    assert commit.commit_id == retrieved_commit.commit_id


def test_lookup_nonexisting(setupdb: PostgresCommitDB):
    result = setupdb.lookup(
        "https://fasfasdfasfasd.com/rewrwe/rwer",
        "42423b242342423b2423",
    )
    setupdb.reset()
    assert result is None


def test_parse_connect_string():
    parsed_connect_string = parse_connect_string(DB_CONNECT_STRING)
    assert parsed_connect_string["host"] == "localhost"
    assert parsed_connect_string["user"] == "postgres"
    assert parsed_connect_string["port"] == "5432"
