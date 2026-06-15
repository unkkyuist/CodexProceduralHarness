# 추천 사용법

이 하네스는 기본적으로 자동 적용된다. 평소처럼 요청해도 `AGENTS.md`가
검사, 분해, 검증, 보고 방식을 잡는다. 다만 작업 성격을 명확히 말하면
Codex가 더 좋은 검증 경로를 선택하기 쉽다.

## 기본 사용

보통은 이렇게 말하면 충분하다.

```text
이 프로젝트에서 버그 고쳐줘.
```

```text
새 Godot 게임을 별도 폴더에 만들어줘.
```

```text
이 기능 구현하고 실행 검증까지 해줘.
```

Codex는 자동으로:

- 관련 파일과 구조를 먼저 확인한다.
- 큰 작업은 검증 가능한 단위로 나눈다.
- Godot, 웹, UI, 렌더 산출물은 실제 실행하거나 관찰한다.
- 완료 보고에 검증 결과와 남은 리스크를 포함한다.

## 가장 추천하는 프롬프트

새 프로젝트:

```text
새 Godot 프로젝트를 별도 폴더에 만들어줘. 하네스 기본 방식대로 맥락 확인,
구현, 최종 실행 검증까지 해.
```

기능 추가:

```text
이 기능을 구현해줘. 기존 구조를 먼저 읽고, 필요한 경우 목표를 쪼갠 뒤,
Godot smoke나 실행 로그로 검증해.
```

버그 수정:

```text
이 버그를 고쳐줘. 먼저 재현/로그 확인하고, 가능한 원인 가설을 비교한 뒤
원인 사슬까지 확인해서 수정해.
```

긴 작업:

```text
이건 긴 작업이니까 goal ledger 써서 진행해. 각 단계 완료 증거를 남기고
마지막은 end-to-end 검증 목표로 잡아.
```

리뷰:

```text
코드 리뷰해줘. findings 먼저, 심각도순으로, 파일/라인 근거와 검증 가능한
위험만 분리해서 보고해.
```

## Goal Ledger를 쓰면 좋은 경우

`goal_ledger.py`는 매번 쓸 필요 없다. 다음 경우에만 권장한다.

- 작업이 여러 턴에 걸릴 수 있다.
- 여러 독립 단계를 추적해야 한다.
- 완료 증거를 파일로 남겨야 한다.
- 마지막에 반드시 전체 검증 gate를 통과시켜야 한다.
- 다른 에이전트나 미래 세션에 이어받길 원한다.

예시:

```powershell
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py create --brief "combat polish" --goal "hit feedback::피격 피드백 구현 후 smoke 확인" --goal "final verification::Godot 실행 검증"
```

그 다음:

```powershell
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py next
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py checkpoint --id G001 --status complete --evidence "..."
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py status
```

마지막 목표는 `--verify-cmd`와 `--verify-evidence` 없이는 완료되지 않는다.

## 작업별 권장 강도

| 작업 | 권장 방식 |
| --- | --- |
| 오타, 짧은 문서 수정 | 하네스 기본만 적용. goal ledger 불필요 |
| 작은 코드 수정 | 관련 파일 확인 + focused test |
| Godot 씬/게임 수정 | Godot 실행, smoke, 로그 확인 |
| 웹/UI 수정 | 브라우저/Playwright/스크린샷 관찰 |
| 생성 에셋 추가 | Godot import pass 또는 로더 확인 |
| 크래시/버그 | 재현, 가설 비교, 원인 사슬, 전후 검증 |
| 큰 기능/새 프로젝트 | 단계 분해 + 마지막 end-to-end 검증 |
| 릴리스/배포 | local check + production check |

## 비추천 사용

- 한 줄 수정에 goal ledger를 강제로 쓰는 것
- 렌더/UI 결과를 정적 문법 검사만으로 완료 처리하는 것
- "대충 작동할 것"이라고 보고하는 것
- Claude hook이나 ZCode `/goal`이 Codex에서 자동으로 강제된다고 가정하는 것
- 기존 프로젝트 파일을 읽지 않고 새 구조를 invent하는 것

## Claude에서 쓸 때

Claude Code에서 upstream `fablize` plugin과 hook을 설치하면 일부 동작은
더 강하게 강제될 수 있다. 이 Codex판은 hook 대신 `AGENTS.md`, local skill,
`goal_ledger.py`로 투명하게 작동한다.

자세한 차이는 `CODEX_VS_CLAUDE.md`를 본다.
