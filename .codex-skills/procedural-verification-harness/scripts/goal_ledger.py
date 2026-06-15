#!/usr/bin/env python3
"""Codex procedural harness goal ledger.

This is a stdlib-only persistent goal/evidence helper adapted from the
fablize goal-engine idea for Codex workspaces. It does not enforce completion
by itself; the agent must still call it. Its value is a durable ledger with a
final verification gate.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_STATE_DIR = ".codex-harness"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def paths(state_dir: str) -> tuple[Path, Path, Path]:
    root = Path(state_dir)
    return root, root / "goals.json", root / "ledger.jsonl"


def write_event(state_dir: str, event: str, **data: object) -> None:
    root, _, ledger_path = paths(state_dir)
    root.mkdir(parents=True, exist_ok=True)
    record = {"ts": utc_now(), "event": event, **data}
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_plan(state_dir: str) -> dict:
    _, goals_path, _ = paths(state_dir)
    if not goals_path.exists():
        raise SystemExit(
            f"goal_ledger: no plan at {goals_path}. Run `create` from the repo root first."
        )
    return json.loads(goals_path.read_text(encoding="utf-8"))


def save_plan(state_dir: str, plan: dict) -> None:
    root, goals_path, _ = paths(state_dir)
    root.mkdir(parents=True, exist_ok=True)
    goals_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_goal(raw: str, index: int) -> dict:
    if "::" not in raw:
        raise SystemExit(f"goal_ledger: --goal must use 'title::objective': {raw}")
    title, objective = raw.split("::", 1)
    title = title.strip()
    objective = objective.strip()
    if not title or not objective:
        raise SystemExit(f"goal_ledger: empty title/objective in --goal: {raw}")
    return {
        "id": f"G{index:03d}",
        "title": title,
        "objective": objective,
        "status": "pending",
        "evidence": None,
        "verify_cmd": None,
        "verify_evidence": None,
    }


def cmd_create(args: argparse.Namespace) -> None:
    _, goals_path, _ = paths(args.state_dir)
    if goals_path.exists() and not args.force:
        raise SystemExit(
            f"goal_ledger: plan already exists at {goals_path}. Use status or --force."
        )
    if not args.goal:
        raise SystemExit("goal_ledger: at least one --goal is required.")
    goals = [parse_goal(goal, i) for i, goal in enumerate(args.goal, 1)]
    plan = {"brief": args.brief, "created": utc_now(), "goals": goals}
    save_plan(args.state_dir, plan)
    write_event(args.state_dir, "plan_created", brief=args.brief, count=len(goals))
    print(f"goal_ledger: plan created with {len(goals)} goals")
    for goal in goals:
        print(f"  {goal['id']} {goal['title']}: {goal['objective']}")


def cmd_next(args: argparse.Namespace) -> None:
    plan = load_plan(args.state_dir)
    active = [g for g in plan["goals"] if g["status"] == "in_progress"]
    if active:
        goal = active[0]
    else:
        pending = [g for g in plan["goals"] if g["status"] == "pending"]
        if not pending:
            print("goal_ledger: all goals complete")
            return
        goal = pending[0]
        goal["status"] = "in_progress"
        save_plan(args.state_dir, plan)
        write_event(args.state_dir, "goal_started", id=goal["id"], title=goal["title"])

    is_final = goal["id"] == plan["goals"][-1]["id"]
    print(f"=== goal_ledger handoff: {goal['id']} {goal['title']}")
    print(f"Objective: {goal['objective']}")
    print("Rule: work this goal only and collect evidence.")
    if is_final:
        print("Final goal: completion requires --verify-cmd and --verify-evidence.")


def cmd_checkpoint(args: argparse.Namespace) -> None:
    plan = load_plan(args.state_dir)
    goal = next((g for g in plan["goals"] if g["id"] == args.id), None)
    if goal is None:
        raise SystemExit(f"goal_ledger: {args.id} not found.")
    if goal["status"] != "in_progress":
        raise SystemExit(
            f"goal_ledger: {args.id} is {goal['status']}; activate it with `next` first."
        )

    if args.status == "complete":
        if not args.evidence.strip():
            raise SystemExit("goal_ledger: complete requires non-empty --evidence.")
        is_final = goal["id"] == plan["goals"][-1]["id"]
        if is_final and not (args.verify_cmd.strip() and args.verify_evidence.strip()):
            raise SystemExit(
                "goal_ledger: final goal requires --verify-cmd and --verify-evidence."
            )

    goal["status"] = args.status
    goal["evidence"] = args.evidence
    goal["verify_cmd"] = args.verify_cmd or None
    goal["verify_evidence"] = args.verify_evidence or None
    save_plan(args.state_dir, plan)
    write_event(
        args.state_dir,
        "checkpoint",
        id=goal["id"],
        status=args.status,
        evidence=args.evidence,
        verify_cmd=args.verify_cmd,
        verify_evidence=args.verify_evidence,
    )
    remaining = [g for g in plan["goals"] if g["status"] in ("pending", "in_progress")]
    print(f"goal_ledger: {goal['id']} -> {args.status}")
    print("goal_ledger: all goals complete" if not remaining else f"goal_ledger: {len(remaining)} goals left")


def cmd_status(args: argparse.Namespace) -> None:
    plan = load_plan(args.state_dir)
    done = sum(1 for g in plan["goals"] if g["status"] == "complete")
    print(f"goal_ledger: {done}/{len(plan['goals'])} complete - {plan['brief']}")
    markers = {"complete": "done", "in_progress": "active", "pending": "todo", "failed": "failed", "blocked": "blocked"}
    for goal in plan["goals"]:
        marker = markers.get(goal["status"], goal["status"])
        print(f"  {goal['id']} [{marker}] {goal['title']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="goal_ledger.py")
    parser.add_argument("--state-dir", default=DEFAULT_STATE_DIR)
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--brief", required=True)
    create.add_argument("--goal", action="append", default=[])
    create.add_argument("--force", action="store_true")
    create.set_defaults(func=cmd_create)

    next_goal = sub.add_parser("next")
    next_goal.set_defaults(func=cmd_next)

    checkpoint = sub.add_parser("checkpoint")
    checkpoint.add_argument("--id", required=True)
    checkpoint.add_argument("--status", required=True, choices=["complete", "failed", "blocked"])
    checkpoint.add_argument("--evidence", default="")
    checkpoint.add_argument("--verify-cmd", default="")
    checkpoint.add_argument("--verify-evidence", default="")
    checkpoint.set_defaults(func=cmd_checkpoint)

    status = sub.add_parser("status")
    status.set_defaults(func=cmd_status)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
