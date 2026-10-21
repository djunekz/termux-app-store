# Accessibility Statement

Termux App Store aims to be usable by as many people as possible, including people who rely on keyboards, screen magnification, high-contrast displays, or assistive technology. This document describes what we support today, what we know is not good enough yet, and how to tell us about a barrier you hit.

This is an honest status report, not a claim of formal compliance. Termux App Store has not been audited against WCAG or any other accessibility standard.

## Supported environments

Termux App Store is a terminal application. It runs inside [Termux](https://termux.dev) on Android and is used through two interfaces:

- **CLI** (`tas`): plain text commands such as `list`, `search`, `show`, `install`, `uninstall`, `update` and `upgrade`. Run `tas --help` for the full list.
- **TUI** (full-screen interface built with [Textual](https://textual.textualize.io)): a package browser with a search box, a package list and a details panel.

Because it lives in a terminal, how accessible it is also depends on your terminal emulator, on-screen keyboard, font size and Android accessibility settings.

## What works today

- Every action the TUI offers is also available as a non-interactive CLI command, so nothing requires the full-screen interface.
- CLI output is plain text that can be piped, copied, searched and read by a terminal-aware screen reader or a braille display more easily than a full-screen interface.
- The TUI uses light text on a dark background and does not use sound.
- The TUI can be operated with a keyboard: `Ctrl+R` refreshes packages, `Ctrl+I` installs the selected package and `Ctrl+Q` quits.
- Text size follows your terminal and Termux font size setting, so you can enlarge it without changing the app.
- Documentation is available in several languages (see the `README.*.md` files).

## Known limitations

- **Screen readers:** the TUI has not been tested with TalkBack or other screen readers. Full-screen terminal interfaces are drawn as a grid of characters and are generally hard for screen readers to follow. If you use a screen reader, we recommend the CLI.
- **Fixed color theme:** the TUI has one dark color theme. There is no light theme, no high-contrast theme and no setting to change colors.
- **Color in output:** some output uses color to highlight status. The `NO_COLOR` environment variable is not currently supported.
- **Keyboard shortcuts:** only a few shortcuts exist. In many terminals `Ctrl+I` is the same key as `Tab`, so it may not behave as an install shortcut. Android on-screen keyboards often have no `Ctrl` key; use the Termux extra keys row.
- **Touch and mouse:** parts of the TUI are easiest to use with a mouse or by tapping, and small targets can be hard to hit on a phone screen.
- **No reduced-motion or verbosity settings:** the TUI refreshes parts of the screen periodically (for example while installing), and there are currently no options to reduce this or change how much text is shown.

## Tips

- Prefer the CLI (`tas search <name>`, `tas show <name>`, `tas install <name>`) if the TUI is hard to use with your setup.
- Increase the font size from Termux (long-press the terminal to open its menu) for easier reading.
- Use the Termux extra keys row for `Ctrl`, `Tab` and arrow keys.

## Report an accessibility barrier

If something in Termux App Store, its documentation or this repository is hard or impossible for you to use, please tell us.

- **Public report:** [open an issue](https://github.com/djunekz/termux-app-store/issues/new/choose) using the Support / Help Request or Bug Report template, and put `accessibility` in the title.
- **Question or idea:** start a [discussion](https://github.com/djunekz/termux-app-store/discussions).
- **Prefer private contact:** email gab288.gab288@passinbox.com.

Useful details to include:

- What you were trying to do and what got in the way
- Your device, Android version and terminal (Termux version if known)
- The interface you used (CLI or TUI) and the command, if any
- Any assistive technology, keyboard or display settings you use
- A suggestion for what would work better, if you have one

## What to expect

Termux App Store is maintained by volunteers, so we cannot promise a response time. Accessibility reports are welcome at any time, will be read, and will be handled as bugs. Pull requests that improve accessibility are very welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).

## Related documents

- [SUPPORT.md](SUPPORT.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [SECURITY.md](SECURITY.md)
