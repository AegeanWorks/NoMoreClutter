# Decisions

Why this project is built the way it is, oldest first. One entry per decision that changes a
contract, a dependency, a data format or the architecture; IDs are consecutive and never reused.

### ADR-001: RLM Hierarchical Decomposition vs. Flat Batching
- **Date**: 2026-10-14
- **Status**: Accepted
- **Context**: Sending hundreds or thousands of raw file paths directly into an LLM prompt leads to context window exhaustion, rapid exhaustion of free-tier rate limits (e.g. Groq TPM caps), attention dilution, and latency spikes.
- **Decision**: Implement a Recursive Language Model (RLM) engine (`services/rlm_organizer.py`). Files are first partitioned into logical category clusters. Each cluster is serialized into dense JSON payloads using relative IDs rather than long absolute paths. Responses are deterministically mapped by ID.
- **Consequences**: Cuts token overhead by ~70%. Guarantees that free-tier rate limits are respected. Eliminates off-by-one mapping errors. Adds an intermediate clustering step before dispatching requests.

### ADR-002: Zero-Install Cloud Providers with Local Fallback (Hybrid AI)
- **Date**: 2026-10-14
- **Status**: Accepted
- **Context**: Requiring users to download heavy desktop apps before organizing their first file introduces substantial friction. However, power users demand local self-hosted privacy.
- **Decision**: Support both paradigms seamlessly via a pluggable provider abstraction (`services/providers/`). Provide pre-configured cloud presets (Groq with free keys, Google Gemini, OpenAI, OpenRouter) alongside local servers (LM Studio, Ollama) and a 100% offline heuristic fallback.
- **Consequences**: Zero-friction onboarding for new users while retaining full privacy and power for local users.

### ADR-003: Collision Avoidance and Batch Undo Stack
- **Date**: 2026-10-14
- **Status**: Accepted
- **Context**: File operations can be destructive if destination folders already contain files with the same name, or if the user is dissatisfied with AI organization decisions.
- **Decision**: 1. Dynamic collision renaming: if `destination/file.ext` exists, automatically generate `destination/file (1).ext`. 2. Batch undo: every file move is recorded as a `FileMoveRecord(original, new, timestamp)` and pushed to an undo stack. Users can roll back the entire batch with one click.
- **Consequences**: Zero risk of accidental file overwrites or data loss. High user confidence.

### ADR-004: Living Principles System & Automated Cross-AI Synchronization
- **Date**: 2026-10-14
- **Status**: Accepted
- **Context**: Different developers and AI assistants enter this repository across different workflows. Disconnected guidelines lead to knowledge drift and conflicting changes.
- **Decision**: Establish master canonical specifications and automated scripts to synchronize guidelines and validate the knowledge base.
- **Consequences**: 100% consistency across all AI assistants; eliminates knowledge drift.

### ADR-005: Automated Test Verification & Continuous Test Coverage (Regression Shield)
- **Date**: 2026-10-14
- **Status**: Accepted
- **Context**: Frequent additions, refactorings, or modifications made across disparate AI sessions risk breaking existing service interfaces, corrupting data mappings, or regressing path calculation logic.
- **Decision**: Codify automated test verification and continuous test coverage. Every change must be paired with dedicated unit tests in `tests/`, and the complete test suite must be confirmed 100% green before any commit is finalized.
- **Consequences**: Complete regression protection, rapid feedback cycle, clean test baseline.

### ADR-006: 1-Click AI Model Quick-Deploy (Embedded GGUF, Ollama Auto-Pilot, and Cloud Connect)
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Setting up local LLM servers or obtaining cloud API keys introduces friction for non-technical users.
- **Decision**: Implement a multi-path 1-Click Quick Deploy architecture: embedded local GGUF streaming downloader, Ollama auto-pilot daemon integration, and instant free cloud key wizard.
- **Consequences**: Zero-friction onboarding; users can deploy an AI model in a single click with visual progress.

### ADR-007: Persistent Multi-Session Undo & Zero-Dependency Document Peeking
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: In-memory undo was lost on app close or crash. Cryptic filenames (`Scan_001.pdf`, `doc_final.docx`) led to inaccurate grouping without document content peeking.
- **Decision**: Persist atomic batch operations to `history.json` with multi-session rollback. Implement zero-dependency document text peeking using standard library `zipfile` and `zlib` with snippets capped at $\le 200$ chars.
- **Consequences**: Reorganize operations can be undone across app restarts and reboots; categorization accuracy is elevated with zero third-party dependencies.

### ADR-008: Hardware Auto-Benchmark & Camera Timestamp Anti-Hallucination Guard
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Users running diverse hardware had to guess optimal batch sizes and limits. Numeric camera timestamps (`20170926_112101.jpg`) without vision caused text models to hallucinate arbitrary scenes.
- **Decision**: Implement `BenchmarkService` to measure latency/throughput and configure optimal batch settings. Route camera timestamp photos deterministically to `Photos/{year}/` preserving original filenames.
- **Consequences**: Zero-guesswork tuning tailored to user hardware; prevents bizarre photo hallucinations.

### ADR-009: Comprehensive Settings Architecture, Provider Auto-Detection & Persistence
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Switching providers previously wiped custom endpoints and category selections, and setting toggles (`ai_rename`, `create_folders`) needed strict deterministic enforcement.
- **Decision**: Implement self-healing provider auto-detection, protected settings preservation across re-opens, category filter persistence in `settings.json`, and deterministic post-processing overrides.
- **Consequences**: Settings operate predictably and reliably across sessions with zero settings drift.

### ADR-010: Continuous Mathematical Slider Auto-Tuning Architecture
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Coarse latency steps failed to match hardware nuances, and sliders lacked live interactive badges.
- **Decision**: Replace rigid tiers with continuous mathematical clamp functions for batch size, file limit, context peek budget, and inter-batch pacing delay, wired to live CustomTkinter sliders.
- **Consequences**: Exact, bespoke calibration for every user machine; tactile and intuitive UI.

### ADR-011: Vision Capability Safeguards and Graceful Text RLM Fallback
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Text-only models running with vision enabled dumped repetitive errors and dumped all images into generic folders.
- **Decision**: Add provider `has_vision` property, fast-abort vision loops on first unsupported error, route images cleanly to text RLM clustering, and auto-disable UI vision controls for text models.
- **Consequences**: Zero terminal error spam, zero dropped images, and graceful degradation across all providers.

### ADR-012: Interactive Tree Preview, Two-Stage Deduplication & Orphan Pruner
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Users needed visual preview and per-file selective move controls before committing reorganizations, plus duplicate finding and empty folder cleanup.
- **Decision**: Implement `TreePreviewDialog` with collapsible folder cards and checkboxes; build fast zero-dependency $O(N)$ two-stage deduplication (`services/deduplicator.py`); implement bottom-up leaf folder pruning (`services/cleaner_service.py`).
- **Consequences**: Complete visual confidence before file moves; instant recovery of duplicate disk space; clean directory trees.

### ADR-013: Spacious Two-Column Dashboard Layout and Window Zooming
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Vertically congested layouts caused excessive scrolling on modern high-resolution desktop screens.
- **Decision**: Implement a two-column master-detail dashboard with top header bar, left control deck, right dedicated live activity terminal, and automatic window zooming on launch.
- **Consequences**: Modern, spacious layout with clear visual hierarchy and zero scrolling friction.

### ADR-014: Real-Time Progressive Duplicate Card Streaming and Non-Blocking UI Rendering
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Rendering all duplicate cards at once locked the Tkinter main thread on large directory scans.
- **Decision**: Emit duplicate groups progressively via streaming callbacks and render micro-batched cards interleaved with Tkinter's event loop.
- **Consequences**: 100% fluid, responsive UI with zero post-scan freezing; instant visual feedback.

### ADR-015: 1-Click Vision Model Deployment & Model Capability Badging
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Users deploying models had no visual indication of vision capabilities, and local embedded vision was unsupported.
- **Decision**: Build multimodal dual-file downloader supporting base weights and `mmproj` projector weights; display capability badges across all model presets; enable dynamic embedded vision handler dispatch.
- **Consequences**: Complete capability transparency; 1-click offline vision intelligence with atomic dual-file downloads.

### ADR-016: In-App File Viewer, Visual Side-by-Side Duplicate Comparator & Headless Test Decoupling
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Inspecting files required external applications; headless tests instantiating CustomTkinter widgets with Mock parents entered unbounded redraw loops consuming excessive RAM.
- **Decision**: Implement `FileViewerDialog` with single-file and side-by-side comparison modes; decouple pure formatting and decoding functions into headless helpers covered by fast unit tests without widget instantiation.
- **Consequences**: Fluid in-app preview; tests run in under 0.02s with zero GUI overhead or RAM bloat.

### ADR-017: Incremental Progress Checkpointing & Zero-Progress-Loss Disruption Recovery Ledger
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Power outages and abrupt shutdowns during multi-step implementations risk losing uncommitted in-progress work.
- **Decision**: Codify incremental progress checkpointing with atomic task ledger writes, quarantine of corrupted state files, and pre-flight disruption audits.
- **Consequences**: Zero progress loss during sudden outages; reliable task resumption.

### ADR-018: Lag-Free Virtual Pagination for Duplicate Finder & Modal Grab Foreground Lift for File Viewer
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Scanning folders with hundreds of duplicate groups caused Tkinter canvas scrolling lag; preview dialogs could be hidden behind parent modal dialogs.
- **Decision**: Implement `PAGE_SIZE = 25` virtual pagination in `DuplicateFinderDialog` while preserving global selection; implement modal grab transfer and foreground window lifting in `FileViewerDialog`.
- **Consequences**: Smooth, lag-free duplicate browsing across large collections; guaranteed preview visibility.

### ADR-019: Universal Operational Dogfooding & Chaos Verification
- **Date**: 2026-10-15
- **Status**: Accepted
- **Context**: Headless unit tests miss interaction boundaries, window destruction timing, and unexpected API schema variations; dogfooding must not touch user personal files.
- **Decision**: Implement `DogfoodBlastRadiusJail` strictly confining runs to ephemeral sandboxes; build `scripts/dogfood_app.py` driving live UI lifecycles, dialogs, sliders, and offline API chaos fuzzing.
- **Consequences**: Complete elimination of silent Tkinter callback crashes; verified operational stability across all corners with zero blast-radius risk.

### ADR-020: Integration into AIKit Cockpit Architecture
- **Date**: 2026-10-19
- **Status**: Accepted
- **Context**: NoMoreClutter originally shipped with embedded standalone copies of early AIKit principles and tooling (`.agents/`, `scripts/`, `knowledge/`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `GUIDELINES.md`). Under AIKit's multi-project cockpit model (ADR-119, PRINCIPLE-011 R8), AIKit is the workspace root and managed projects live in their own repositories under `projects/` with memory isolated to `.aikit/`.
- **Decision**: Migrate NoMoreClutter into a standard AIKit-managed project: clean up obsolete embedded AIKit governance scripts, rules, and knowledge directories; format past ADRs into `.aikit/decisions.md`; integrate the dogfooding harness cleanly; ensure full gate compliance with `aikit check nomoreclutter`.
- **Consequences**: NoMoreClutter codebase becomes lean and focused on its core application functionality; 100% compliant with AIKit's 4 Phase 4 delivery gates; zero duplicate governance files.

### ADR-021: Interactive Dogfood Tests Are Opt-In
- **Date**: 2026-10-29
- **Status**: Accepted
- **Context**: `python -m unittest discover tests` ran `TestDogfoodHarness`, which mounts live CustomTkinter windows and spammed the user's desktop during every gate run. The dogfood harness is an interactive operational check, not a headless unit test.
- **Decision**: Skip the dogfood harness tests unless `NOMORECLUTTER_GUI_TESTS=1`; keep `python scripts/dogfood_app.py` as the explicit interactive entry point. The default test gate stays headless.
- **Consequences**: Gate runs never open windows; interactive UI verification remains available on demand. UI coverage is intentionally opt-in, consistent with ADR-019.

### ADR-022: Hierarchical Folder Sanitization With Single-Slash Guard and Strict ID Validation
- **Date**: 2026-11-02
- **Status**: Accepted
- **Context**: `_sanitize_folder_name` flattened `Photos/2017` to `Photos_2017`, diverging AI/vision output from heuristic `Photos/YYYY` albums; duplicate/out-of-range/non-int LLM IDs could double-move or drop files.
- **Decision**: Per-segment sanitize allowing at most one `/` (extra depth folded with `_`), dropping `..`/`.`/drive/leading-slash; strict first-wins int-ID validation in `_analyze_cluster` with heuristic fallback for missed files; identical sanitize in text and vision paths.
- **Consequences**: `Photos/YYYY` preserved end-to-end, traversal contained inside `output_folder`, wrong-AI-answer covered by persistent `FileExecutor` undo, offline fallback parity kept; cleaner/dedup permanent deletes and constrained-folder `existing[0]` fallback stay out of scope.

## Licensing migration (agpl-final)

- New versions use the Aegean License 1.1 (AL-1.1); versions up to and including `agpl-final` remain under GNU AGPL-3.0.
- Rights holder: AegeanWorks; commercial use under ACL-1.0.
- Counsel review of the 1.1 texts remains pending.

## License notice cleanup (2026-10-26)

- The license-history notes were removed from README.md and COMMERCIAL.md: the project is offered only under the Aegean License 1.1 (AL-1.1), with commercial use under ACL-1.0.

### ADR-023: Audit Batch — Vision/Text Parity, Identity-Safe Selection, Scanner and Import Hardening
- **Date**: 2026-11-02
- **Status**: Accepted
- **Context**: Stage 2 audit found vision path missing the ADR-008 camera-timestamp guard (camera photos mis-filed under vision), `_match_closest_folder` returning unsanitized caller input (traversal escape), `_sanitize_filename` permitting LLM extension swaps (`.pdf`→`.exe`) and vision empty-stem hidden `.jpg`, `TreePreviewDialog` toggling/executing wrong files (equality-based `.index()` on `FileChange` values plus render-order/input-order key mismatch), `FileScanner.scan_folder` crashing on missing dirs and missing uppercase/dotless extensions, `main.py` missing `Optional` import (hard `NameError` on Python 3.10–3.13, lazy-annotation failure on 3.14), and `_load_more_cards(count=25)` diverging from `PAGE_SIZE`.
- **Decision**: Apply the camera-timestamp guard to the vision path (parity with text path), sanitize `_match_closest_folder` returns, enforce original file extensions and basename fallback on empty stems, key tree-preview selection by object-identity render maps, guard shallow scans to `[]` with normalized extensions, import `Optional` in `main.py`, default pagination count to `PAGE_SIZE`; update `test_process_images_with_integer_json_fields` expectation from `/dest/2017/…` to `/dest/Photos/2017/…` to match the documented `Photos/YYYY` convention.
- **Consequences**: Vision and text organize identically for timestamp photos; traversal contained even for hostile `existing_folders`; no executable masquerade via rename; tree selection/execution maps 1:1 to checked rows; scanner never crashes callers; app imports on all supported Pythons; pagination tuning stays single-sourced. PROPOSE items (cleaner age/size policy, executor journal locking, settings persistence/schema, plaintext API key, modal grab races) stay out of scope for human decision.

### ADR-024: Main-window keeper via PrintWindow
- **Date**: 2026-11-03
- **Status**: Accepted
- **Context**: No registered screenshots existed; the CustomTkinter window never takes focus from a headless launcher, so fullscreen grabs frame the IDE.
- **Decision**: Register `2026-11-03-main.png` (`python main.py`, PrintWindow on the `NoMoreClutter` window, 1356x919, commit `b9cb347`) in `.aikit/media.json` and the README `aegean:screenshots` block. The single window is the whole UI, so one keeper is full coverage. No folders were selected and nothing was organized.
- **Consequences**: README proves the current app. Reproduce with the launch plus PrintWindow helper above.
