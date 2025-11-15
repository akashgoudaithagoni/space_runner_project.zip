# QA Checklist & Test Cases

Functional Tests
- [ ] Launch game (no crashes)
- [ ] Player moves left/right using arrow keys and A/D
- [ ] Meteors spawn and fall
- [ ] Collision causes Game Over
- [ ] Restart (R) works after Game Over

Edge cases
- [ ] Player stuck at screen edges
- [ ] Rapid key presses don't desync movement
- [ ] Many meteors do not crash the game (stress test)

Performance
- [ ] Stable 60 FPS on target machine
- [ ] Memory usage within reason for session length

Reporting / Repro steps
- Include steps to reproduce any bug, expected vs actual behavior, screenshots, logs, and system specs.

Automation ideas
- Smoke test: launch game, run 10 seconds, check process still running
- Input automation: use a tool to send left/right keystrokes to validate movement

