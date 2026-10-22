#!/usr/bin/env python3
"""Digest Claude Code session transcripts into facts a recap can be written from.

Reads ~/.claude/projects/*/<session>.jsonl, keeps the records of one local day for
the given project folders, and prints Markdown: sessions, the user's requests in
order, typed slash commands, tool counts, skills and subagents Claude invoked,
changed files, and git commits of that day.
"""

import argparse
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, tzinfo
from pathlib import Path
from zoneinfo import ZoneInfo

COMMAND = re.compile(r"<command-name>(.*?)</command-name>", re.S)
ARGS = re.compile(r"<command-args>(.*?)</command-args>", re.S)
REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
PASTED = re.compile(r"<pasted_content[^>]*>(.*?)</pasted_content[^>]*>", re.S)
BASH_INPUT = re.compile(r"<bash-input>(.*?)</bash-input>", re.S)
# Echoes of local commands and their output, not requests.
NOISE = ("<local-command", "<bash-stdout", "<bash-stderr", "Caveat:")
# The desktop app's task list and wrap-up tools track progress, not work.
APP_TOOLS = "mcp__ccd_turn__"


@dataclass
class Prompt:
    time: datetime
    text: str
    command: str | None = None


@dataclass
class Session:
    path: Path
    id: str
    cwd: str = ""
    title: str = ""
    prompts: list[Prompt] = field(default_factory=list)
    tools: Counter = field(default_factory=Counter)
    skill_calls: list[str] = field(default_factory=list)
    agent_calls: list[str] = field(default_factory=list)
    changed_files: list[str] = field(default_factory=list)
    start: datetime | None = None
    end: datetime | None = None


def _local(ts: str, tz: tzinfo) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(tz)


def _prompt_text(content) -> tuple[str | None, str] | None:
    """(slash command, text) for a real request, or None for noise."""
    if isinstance(content, list):
        texts = [c.get("text", "") for c in content if c.get("type") == "text"]
        if not texts:
            return None  # tool results
        content = "\n".join(texts)
    content = REMINDER.sub("", content).strip()
    if not content or content.startswith(NOISE):
        return None
    if command := COMMAND.search(content):
        args = ARGS.search(content)
        return command.group(1).strip(), (args.group(1).strip() if args else "")
    if bash := BASH_INPUT.search(content):
        return None, f"$ {bash.group(1).strip()}"
    # Pasted text can be long and private; keep only how much was pasted.
    content = PASTED.sub(
        lambda m: f"[貼り付け {len(m.group(1).strip())} 文字]", content
    )
    return None, content


def read_session(path: Path, day: date, tz: tzinfo, seen: set | None = None) -> Session:
    """Records of one local day. seen collects record uuids across sessions, so a
    forked session, which copies its parent's records, adds only what is new."""
    seen = set() if seen is None else seen
    session = Session(path=path, id=path.stem)
    seen_files, cwds = [], {}
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("type") == "custom-title":
            session.title = record.get("customTitle", session.title)
            continue
        # The latest cwd wins: a session can outlive a rename of its folder.
        if record.get("cwd"):
            session.cwd = record["cwd"]
            cwds.setdefault(record["cwd"], None)
        ts = record.get("timestamp")
        if not ts or record.get("type") not in ("user", "assistant"):
            continue
        if uuid := record.get("uuid"):
            if uuid in seen:
                continue
            seen.add(uuid)
        when = _local(ts, tz)
        if when.date() != day:
            continue
        session.start = min(session.start or when, when)
        session.end = max(session.end or when, when)
        content = record.get("message", {}).get("content")
        if record["type"] == "user":
            if record.get("isMeta"):
                continue
            parsed = _prompt_text(content)
            if parsed:
                session.prompts.append(
                    Prompt(time=when, command=parsed[0], text=parsed[1])
                )
            continue
        for part in content if isinstance(content, list) else []:
            if part.get("type") != "tool_use":
                continue
            name, args = part.get("name", ""), part.get("input", {})
            if name.startswith(APP_TOOLS):
                continue
            session.tools[name] += 1
            if name == "Skill":
                session.skill_calls.append(args.get("skill", "?"))
            elif name in ("Agent", "Task"):
                session.agent_calls.append(
                    f"{args.get('subagent_type', 'general')}: {args.get('description', '')}"
                )
            elif name in ("Write", "Edit", "NotebookEdit") and args.get("file_path"):
                seen_files.append(args["file_path"])
    roots = [c.rstrip("/") + "/" for c in cwds]
    session.changed_files = list(dict.fromkeys(_relative(f, roots) for f in seen_files))
    return session


def _relative(path: str, roots: list[str]) -> str:
    for root in roots:
        if path.startswith(root):
            return path.removeprefix(root)
    # Outside the project: shorten the home folder so the user's name stays out.
    return (
        "~" + path.removeprefix(str(Path.home()))
        if path.startswith(str(Path.home()))
        else path
    )


CWD = re.compile(r'"cwd":\s*"((?:[^"\\]|\\.)*)"')


def _cwds_of(path: Path) -> set[str]:
    """Every working folder a session ran in, since a folder can be renamed mid-session."""
    return {json.loads(f'"{m}"') for m in CWD.findall(path.read_text(encoding="utf-8"))}


def find_sessions(
    root: Path, project_dirs: list[str], day: date, tz: tzinfo
) -> list[Session]:
    """Sessions whose recorded cwd is one of project_dirs and that have records on day."""
    wanted = {d.rstrip("/") for d in project_dirs}
    found, seen = [], set()
    # Oldest file first, so a parent is read before the forks that copy it.
    for path in sorted(root.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime):
        cwds = _cwds_of(path)
        if not any(c == w or c.startswith(w + "/") for c in cwds for w in wanted):
            continue
        session = read_session(path, day, tz, seen)
        if session.start:
            found.append(session)
    return sorted(found, key=lambda s: s.start)


def git_commits(repo: str, day: date, tz: tzinfo) -> list[str]:
    start = datetime.combine(day, time(), tz)
    try:
        out = subprocess.run(
            [
                "git",
                "-C",
                repo,
                "log",
                "--all",
                f"--since={start.isoformat()}",
                f"--until={(start + timedelta(days=1)).isoformat()}",
                "--reverse",
                "--date=format:%H:%M",
                "--format=%cd %h %s",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return out.stdout.splitlines()


def render(
    sessions: list[Session], commits: list[str] | None = None, max_prompt: int = 400
) -> str:
    hhmm = lambda t: t.strftime("%H:%M")  # noqa: E731
    out = ["# セッションの要約（事実）", ""]
    for s in sessions:
        out.append(f"## {s.title or '(題なし)'}  `{s.id[:8]}`")
        out.append(f"- 時間: {hhmm(s.start)}〜{hhmm(s.end)}　作業フォルダ: `{s.cwd}`")
        tools = "、".join(f"{n} {c}" for n, c in s.tools.most_common())
        out.append(f"- 道具の回数: {tools or 'なし'}")
        typed = [p.command for p in s.prompts if p.command]
        out.append(f"- ユーザーが打ったコマンド: {'、'.join(typed) or 'なし'}")
        out.append(f"- Claude が呼んだスキル: {'、'.join(s.skill_calls) or 'なし'}")
        out.append(f"- サブエージェント: {'、'.join(s.agent_calls) or 'なし'}")
        out.append(
            f"- 書き換えたファイル: {'、'.join(f'`{f}`' for f in s.changed_files) or 'なし'}"
        )
        out += ["", "### 依頼の流れ", ""]
        for p in s.prompts:
            text = " ".join(p.text.split())
            text = text if len(text) <= max_prompt else text[:max_prompt] + "…"
            head = f"`{p.command}` " if p.command else ""
            out.append(f"- {hhmm(p.time)} {head}{text}".rstrip())
        out.append("")
    if commits:
        out += ["## その日のコミット", ""] + [f"- {c}" for c in commits] + [""]
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--project",
        action="append",
        help="project folder; repeat for old names (default: cwd)",
    )
    parser.add_argument(
        "--date", type=date.fromisoformat, help="local date YYYY-MM-DD (default: today)"
    )
    parser.add_argument("--tz", help="IANA time zone (default: system local)")
    parser.add_argument(
        "--session",
        action="append",
        default=[],
        help="only sessions whose id starts with this",
    )
    parser.add_argument(
        "--root", type=Path, default=Path.home() / ".claude" / "projects"
    )
    parser.add_argument("--max-prompt", type=int, default=400)
    a = parser.parse_args()
    tz = ZoneInfo(a.tz) if a.tz else datetime.now().astimezone().tzinfo
    day = a.date or datetime.now(tz).date()
    projects = a.project or [str(Path.cwd())]
    sessions = find_sessions(a.root, projects, day, tz)
    if a.session:
        sessions = [s for s in sessions if any(s.id.startswith(p) for p in a.session)]
    if not sessions:
        print(f"{day} に {', '.join(projects)} のセッションは見つかりませんでした。")
        return
    print(render(sessions, git_commits(projects[0], day, tz), a.max_prompt))


if __name__ == "__main__":
    main()
