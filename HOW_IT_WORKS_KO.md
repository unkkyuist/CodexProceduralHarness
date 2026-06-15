# 작동 방식 상세 설명

`Codex Procedural Harness`는 Codex가 작업할 때 더 일관되게
"확인하고, 작게 나누고, 실제로 검증한 뒤, 증거를 보고"하도록 만드는
절차 레이어다.

핵심은 자동화 프로그램 하나를 계속 실행하는 것이 아니다. 이 하네스는
Codex가 읽는 지침 파일, 필요할 때 불러오는 로컬 skill, 그리고 선택적으로
실행하는 goal ledger 스크립트로 동작한다.

## 전체 구조

설치하면 대상 workspace에 다음 파일들이 들어간다.

```text
AGENTS.md
CODEX.md
CLAUDE.md
.codex-skills/
  procedural-verification-harness/
    SKILL.md
    scripts/
      goal_ledger.py
    references/
      early-stop-guard.md
      investigation-protocol.md
      multistory-goals.md
      review-protocol.md
      routing-matrix.md
      upstream-adaptation.md
      verification-grounding.md
```

각 파일의 역할은 다르다.

| 파일 | 역할 |
| --- | --- |
| `AGENTS.md` | workspace에 들어온 Codex가 항상 읽는 기본 작업 규칙 |
| `CODEX.md` | Codex용 진입 안내. `AGENTS.md`가 기준임을 명시 |
| `CLAUDE.md` | Claude 계열 도구가 볼 때의 호환 안내 |
| `SKILL.md` | 큰 작업, 디버깅, 리뷰, 실행 검증 작업에서 쓰는 상세 절차 |
| `references/*.md` | 필요할 때만 여는 세부 지침 |
| `goal_ledger.py` | 긴 작업의 목표와 완료 증거를 파일로 남기는 선택 도구 |

## 자동 적용 방식

Codex는 workspace에 있는 `AGENTS.md`를 작업 규칙으로 사용한다. 그래서
설치 후에는 사용자가 매번 "fablize 방식으로 해줘" 또는 "prometheus
적용해"라고 말할 필요가 없다.

작업이 들어오면 Codex는 먼저 `AGENTS.md`의 기본 규칙을 적용한다.

1. 관련 파일과 구조를 먼저 확인한다.
2. 요청이 단순한지, 큰 작업인지, 버그인지, 리뷰인지, 렌더/실행 검증이
   필요한지 판단한다.
3. 단순 작업이면 가볍게 처리한다.
4. 큰 작업이면 검증 가능한 단계로 나눈다.
5. Godot, 웹, UI, 렌더 산출물처럼 실제 실행 결과가 중요한 작업은 실행
   또는 관찰을 완료 기준에 포함한다.
6. 마지막 답변에서 변경 내용, 검증 결과, 남은 리스크를 보고한다.

즉, 이 하네스의 기본 구동 방식은 "백그라운드 daemon"이 아니라
`AGENTS.md` 기반의 항상 켜진 절차 지침이다.

## Skill이 켜지는 방식

`AGENTS.md`는 항상 읽히는 얇은 규칙이고, 더 자세한 절차는
`.codex-skills/procedural-verification-harness/SKILL.md`에 있다.

Codex는 다음 작업에서 이 skill을 사용한다.

- 새 프로젝트나 큰 기능처럼 단계가 여러 개인 작업
- 버그, 크래시, 테스트 실패, 원인 불명 문제
- Godot, 웹, HTML, SVG, canvas, UI, 차트, 애니메이션처럼 실행/렌더 확인이
  필요한 작업
- 코드 리뷰나 회귀 위험 확인
- 사용자가 "끝까지", "검증하면서", "goal ledger", "fablize",
  "prometheus" 같은 말을 직접 한 경우

skill은 모든 내용을 한 번에 강제로 읽는 구조가 아니다. 먼저 `SKILL.md`만
읽고, 필요할 때만 `references/` 안의 세부 문서를 연다. 이렇게 해서
컨텍스트를 덜 낭비한다.

예를 들어:

- 버그 수정이면 `investigation-protocol.md`
- UI/Godot 실행 확인이면 `verification-grounding.md`
- 긴 작업이면 `multistory-goals.md`
- 리뷰면 `review-protocol.md`
- 마무리 전 확인이면 `early-stop-guard.md`

## 작업 라우팅

하네스는 요청 문장과 실제 코드베이스 상태를 보고 작업 성격을 나눈다.

| 신호 | 적용 절차 |
| --- | --- |
| "버그", "크래시", "에러", "안 됨" | 재현, 가설 비교, 원인 사슬 추적 |
| "Godot", "웹", "UI", "렌더", "차트" | 실제 실행/렌더/로그 확인 |
| "새 프로젝트", "큰 기능", "끝까지" | 단계 분해와 최종 end-to-end 검증 |
| "리뷰", "검토" | findings 먼저, 심각도순 보고 |
| 대상이 애매함 | 파일/구조/성공 조건을 먼저 확인 |

중요한 점은 작업을 무조건 무겁게 만들지 않는다는 것이다. 오타 수정이나
짧은 문서 수정은 goal ledger 없이 빠르게 처리한다.

## Goal Ledger 작동 방식

`goal_ledger.py`는 긴 작업용 선택 도구다. 사용하면 `.codex-harness/` 폴더에
목표 상태와 증거가 저장된다.

기본 흐름:

```powershell
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py create --brief "작업 설명" --goal "구현::무엇을 구현할지" --goal "최종검증::전체 검증"
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py next
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py checkpoint --id G001 --status complete --evidence "검증 증거"
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py status
```

특징:

- 목표는 `G001`, `G002`처럼 번호가 붙는다.
- `next`를 호출하면 다음 목표가 `in_progress`가 된다.
- 목표 완료에는 `--evidence`가 필요하다.
- 마지막 목표는 `--verify-cmd`와 `--verify-evidence` 없이는 완료되지 않는다.

마지막 gate 예시:

```powershell
python .codex-skills\procedural-verification-harness\scripts\goal_ledger.py checkpoint --id G002 --status complete --evidence "최종 smoke 통과" --verify-cmd "Godot --path . --headless --script tools/smoke.gd" --verify-evidence "exit 0; 새 engine warning 없음"
```

이 도구는 Codex를 물리적으로 강제하는 runtime은 아니다. Codex가 긴 작업에서
진행 상태와 검증 증거를 잃지 않도록 돕는 파일 기반 원장이다.

## Godot 작업에서의 흐름

Godot 작업에서는 다음 순서를 기본으로 한다.

1. 프로젝트 루트와 `project.godot` 확인
2. 관련 scene, script, asset 구조 확인
3. 기존 smoke test나 handoff command 확인
4. 필요한 변경만 적용
5. Godot 실행, headless smoke, import pass, 로그 확인 중 가장 적절한 검증 실행
6. engine warning이 새로 생기면 완료로 보지 않음

이 workspace에서는 가능한 경우 다음 Godot console binary를 우선한다.

```powershell
C:\DevWork\GodotGame\Godot_v4.6.3-stable_win64.exe\Godot_v4.6.3-stable_win64_console.exe
```

신규 PNG/WAV 같은 asset이 loader 오류를 내면 바로 게임 로직 문제로 보지
않고, 먼저 Godot import pass가 필요한지 확인한다.

## Codex판과 Claude판의 차이

이 패키지는 Claude 전용 plugin을 그대로 설치한 것이 아니다. Claude의
아이디어를 Codex용 plain-file 방식으로 바꾼 것이다.

| 항목 | Codex판 | Claude upstream 방식 |
| --- | --- | --- |
| 기본 작동 | `AGENTS.md`를 Codex가 읽고 따름 | Claude Code plugin/hook이 개입 가능 |
| 라우팅 | 지침 기반으로 Codex가 판단 | `UserPromptSubmit` hook으로 주입 가능 |
| early stop 방지 | 체크리스트와 지침 | Stop hook으로 더 강하게 막을 수 있음 |
| 목표 추적 | `goal_ledger.py` 선택 사용 | `goals.py` 또는 ZCode `/goal` 전제 |
| 설치 부작용 | auto-star 없음, hidden hook 없음 | upstream setup은 star 같은 부작용 가능 |
| 강제력 | 투명하지만 runtime 강제는 약함 | hook 설치 시 더 강한 강제 가능 |
| 이식성 | Codex, Claude, 일반 repo 지침으로 쓰기 쉬움 | Claude Code 환경에 더 특화 |

정리하면 Codex판은 더 투명하고 이식성이 좋다. 대신 Claude hook처럼
"멈추려는 순간 runtime이 강제로 막는" 수준의 강제력은 없다. 그 부분을
`AGENTS.md`의 항상 켜진 규칙과 `goal_ledger.py`의 검증 gate로 보완한다.

## 설치 후 실제 사용 예시

일반 요청:

```text
이 버그 고쳐줘.
```

Codex 내부 흐름:

1. 관련 파일 검색
2. 에러 재현 또는 로그 확인
3. 가능한 원인 가설 수립
4. 실제 원인 경로 추적
5. 최소 수정
6. 수정 전후 검증
7. 변경 파일과 검증 결과 보고

긴 요청:

```text
새 Godot 게임을 별도 폴더에 만들고 끝까지 검증해.
```

Codex 내부 흐름:

1. 새 폴더 생성 전 기존 workspace 구조 확인
2. 프로젝트 생성
3. core loop 구현
4. smoke test 또는 실행 검증 추가
5. Godot 실행 검증
6. 사용법과 남은 리스크 보고

명시적으로 더 강하게 시키는 요청:

```text
goal ledger 써서 진행해. 마지막은 end-to-end 검증으로 잡아.
```

이 경우 Codex는 `goal_ledger.py`로 목표를 만들고 각 단계의 evidence를
남기는 쪽으로 진행한다.

## 한계

이 하네스는 모델의 지능 자체를 올리는 도구가 아니다. 다음 한계가 있다.

- Codex가 지침을 읽고 따르는 방식이므로 OS 수준 hook처럼 강제하지 않는다.
- 잘못된 검증 명령을 선택하면 결과도 약해질 수 있다.
- 외부 로그인, API token, GitHub 권한 같은 것은 사용자의 실제 환경에
  의존한다.
- 창의적 품질 판단은 검증 명령만으로 완전히 해결되지 않는다.

그래서 중요한 작업일수록 사용자는 "최종 실행 검증까지", "production
확인까지", "goal ledger 써"처럼 강도를 명확히 말하는 것이 좋다.

## 추천 운용 방식

- 평소에는 자동 적용에 맡긴다.
- Godot/웹/UI 작업은 "실행 검증까지"라고 말한다.
- 긴 작업은 "goal ledger 써"라고 말한다.
- 리뷰는 "findings 먼저, 심각도순"이라고 말한다.
- 한 줄 수정에는 과도한 goal ledger를 요구하지 않는다.
- 완료 보고에서 검증 명령과 결과가 빠져 있으면 다시 검증을 요구한다.
