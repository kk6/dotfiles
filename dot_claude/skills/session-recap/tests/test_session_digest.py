import json
import os
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import session_digest as sd  # noqa: E402

TOKYO = ZoneInfo("Asia/Tokyo")
SID = "aaaa1111-0000-0000-0000-000000000000"


def user(ts, content, **extra):
    return {
        "type": "user",
        "uuid": f"u-{ts}-{len(str(content))}",
        "timestamp": ts,
        "sessionId": SID,
        "cwd": "/w/app",
        "message": {"role": "user", "content": content},
        **extra,
    }


def tool(ts, name, **inp):
    return {
        "type": "assistant",
        "uuid": f"a-{ts}-{name}",
        "timestamp": ts,
        "sessionId": SID,
        "cwd": "/w/app",
        "message": {"content": [{"type": "tool_use", "name": name, "input": inp}]},
    }


RECORDS = [
    {"type": "custom-title", "customTitle": "Build the panel", "sessionId": SID},
    user(
        "2026-10-18T04:49:17Z",
        "<command-message>grilling</command-message>\n<command-name>/mattpocock-skills:grilling</command-name>\n<command-args>ask me one by one</command-args>",
    ),
    user(
        "2026-10-18T04:49:17Z",
        [{"type": "text", "text": "skill body loaded"}],
        isMeta=True,
    ),
    tool("2026-10-18T04:50:00Z", "Bash", command="ls", description="List files"),
    tool("2026-10-18T04:51:00Z", "Write", file_path="/w/app/README.md", content="x"),
    tool("2026-10-18T04:52:00Z", "Edit", file_path="/w/app/README.md"),
    tool("2026-10-18T04:53:00Z", "Skill", skill="pstack:poteto-help"),
    tool(
        "2026-10-18T04:54:00Z",
        "Agent",
        subagent_type="Explore",
        description="Find callers",
    ),
    user("2026-10-18T04:55:00Z", [{"type": "tool_result", "content": "ok"}]),
    tool("2026-10-18T05:00:00Z", "mcp__ccd_turn__update_plan", items=[]),
    user("2026-10-18T05:02:00Z", "reading使ってみました"),
    user("2026-10-18T16:00:00Z", "next day in Tokyo"),
]


def write_session(directory, records):
    folder = Path(directory) / "-w-app"
    folder.mkdir()
    path = folder / f"{SID}.jsonl"
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n"
    )
    return path


class DigestTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = write_session(self.tmp.name, RECORDS)
        self.session = sd.read_session(self.path, day=date(2026, 10, 18), tz=TOKYO)

    def tearDown(self):
        self.tmp.cleanup()

    def test_keeps_only_records_on_the_local_day(self):
        texts = [p.text for p in self.session.prompts]
        self.assertNotIn("next day in Tokyo", texts)
        self.assertIn("reading使ってみました", texts)

    def test_times_are_in_the_given_timezone(self):
        self.assertEqual(self.session.prompts[0].time.strftime("%H:%M"), "13:49")
        self.assertEqual(self.session.start.strftime("%H:%M"), "13:49")
        self.assertEqual(self.session.end.strftime("%H:%M"), "14:02")

    def test_slash_commands_are_typed_skills_with_their_args(self):
        first = self.session.prompts[0]
        self.assertEqual(first.command, "/mattpocock-skills:grilling")
        self.assertEqual(first.text, "ask me one by one")

    def test_meta_and_tool_results_are_not_prompts(self):
        self.assertEqual(len(self.session.prompts), 2)

    def test_counts_tools_and_separates_model_invoked_skills_and_agents(self):
        self.assertEqual(self.session.tools["Bash"], 1)
        self.assertEqual(self.session.skill_calls, ["pstack:poteto-help"])
        self.assertEqual(self.session.agent_calls, ["Explore: Find callers"])

    def test_app_task_list_tools_are_not_counted(self):
        self.assertNotIn("mcp__ccd_turn__update_plan", self.session.tools)

    def test_lists_changed_files_once_relative_to_the_project(self):
        self.assertEqual(self.session.changed_files, ["README.md"])

    def test_title_comes_from_the_custom_title_record(self):
        self.assertEqual(self.session.title, "Build the panel")

    def test_finds_sessions_by_the_cwd_recorded_inside(self):
        found = sd.find_sessions(
            Path(self.tmp.name), ["/w/app"], date(2026, 10, 18), TOKYO
        )
        self.assertEqual([s.path for s in found], [self.path])
        self.assertEqual(
            sd.find_sessions(
                Path(self.tmp.name), ["/w/other"], date(2026, 10, 18), TOKYO
            ),
            [],
        )

    def test_renders_markdown_with_the_typed_skill(self):
        text = sd.render([self.session])
        self.assertIn("/mattpocock-skills:grilling", text)
        self.assertIn("13:49", text)
        self.assertIn("Bash 1", text)


class ForkTest(unittest.TestCase):
    def test_a_fork_does_not_count_the_copied_records_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = write_session(tmp, RECORDS)
            fork_dir = Path(tmp) / "-w-app-renamed"
            fork_dir.mkdir()
            fork = fork_dir / "bbbb2222-0000-0000-0000-000000000000.jsonl"
            extra = user("2026-10-18T06:00:00Z", "only in the fork")
            fork.write_text(original.read_text() + json.dumps(extra) + "\n")
            os.utime(fork, (original.stat().st_mtime + 10,) * 2)
            found = sd.find_sessions(Path(tmp), ["/w/app"], date(2026, 10, 18), TOKYO)
            prompts = [p.text for s in found for p in s.prompts]
            self.assertEqual(prompts.count("reading使ってみました"), 1)
            self.assertIn("only in the fork", prompts)


class RenamedFolderTest(unittest.TestCase):
    def test_a_session_that_moved_to_a_renamed_folder_is_found_by_its_new_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            moved = user("2026-10-18T07:00:00Z", "after the rename")
            moved["cwd"] = "/w/app-renamed"
            write_session(tmp, RECORDS + [moved])
            found = sd.find_sessions(
                Path(tmp), ["/w/app-renamed"], date(2026, 10, 18), TOKYO
            )
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].cwd, "/w/app-renamed")


if __name__ == "__main__":
    unittest.main()
