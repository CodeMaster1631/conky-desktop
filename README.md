# Stellar Conky Desktop

A dark, transparent Linux Mint Cinnamon desktop built with Conky, Eww, and a soft pastel palette. The layout is split across two workspaces so it remains information-rich without feeling crowded.

## Preview

### Workspace 1 — system, calendar, and quote

![Workspace 1: system information, calendar, and quote widgets](assets/Screenshot%20from%202026-09-08%2017-15-47.png)

### Workspace 2 — weather

![Workspace 2: Ahmedabad and Davao weather widgets](assets/Screenshot%20from%202026-09-08%2017-32-14.png)

## What it includes

- A transparent Cinnamon bottom panel with the Transparent Panels extension
- A left-side system monitor and a right-side date/calendar widget
- A centered rotating quote widget
- Weather widgets for Ahmedabad and Davao, with four-hour forecasts
- A startup script that places widgets and toggles them between workspaces
- An Eww panel integration point for a circular workspace indicator

| Workspace | Visible widgets |
| --- | --- |
| 1 | System monitor, calendar, quote |
| 2 | Ahmedabad weather, Davao weather |

The script detects the active workspace with `xdotool get_desktop`: desktop `0` is Workspace 1 and desktop `1` is Workspace 2.

## Requirements

This setup targets Linux Mint Cinnamon on X11. It was created on Linux Mint 22.3 with Cinnamon 6.6.9 at 3072×1728, but the launcher calculates positions from the current primary-display dimensions.

Install the required packages:

```bash
sudo apt install conky-all xdotool x11-utils python3
```

Also install and configure:

- [Eww](https://elkowar.github.io/eww/) (the launcher expects it at `/usr/local/bin/eww`)
- Cinnamon's **Transparent Panels** extension
- Numix-Circle icons (optional, for the pictured panel)
- `JetBrainsMono Nerd Font` for the primary widget font
- DejaVu Sans for weather symbols

The weather helper fetches data from the [Open-Meteo API](https://open-meteo.com/), so it needs network access when Conky refreshes it.

## Install

1. Clone the repository into your Conky configuration directory:

   ```bash
   git clone git@github.com:CodeMaster1631/conky-desktop.git ~/.config/conky
   ```

2. Ensure the launcher and helper scripts are executable:

   ```bash
   chmod +x ~/.config/conky/start-stellar.sh \
     ~/.config/conky/quotes/get-quote.py \
     ~/.config/conky/weather/weather.py
   ```

3. Configure Eww in `~/.config/eww/`. `start-stellar.sh` opens an Eww window named `panel` and then runs `~/.config/eww/place-panel.sh`; create or adapt those files to match your Eww setup.

4. Review the personal paths and hardware names in the configuration before launching:

   - `stellar-left.conf` contains the network interface (`wlo1`) and HDD path (`/home/abby/LinuxData`).
   - `start-stellar.sh` includes absolute Eww and configuration paths.
   - The display position offsets in `start-stellar.sh` are tuned for the screenshots and may need adjustment for your resolution.

5. Launch the desktop setup:

   ```bash
   ~/.config/conky/start-stellar.sh
   ```

To start it automatically after login, create a Cinnamon Startup Applications entry named `Stellar Desktop` with this command:

```text
/home/YOUR_USER/.config/conky/start-stellar.sh
```

Add only this launcher—do not add the individual Conky widgets separately.

## Configuration

### Conky widgets

| File | Widget |
| --- | --- |
| `stellar-left.conf` | System and performance information |
| `stellar-right.conf` | Date and calendar |
| `stellar-quote.conf` | Quote |
| `stellar-ahmedabad.conf` | Ahmedabad weather |
| `stellar-davao.conf` | Davao weather |
| `start-stellar.sh` | Widget startup, positioning, and workspace visibility |

`stellar-center.conf`, `stellar-weather.conf`, and `font-test.conf` are supporting/experimental configurations retained in the repository.

### Weather

`weather/weather.py` accepts a city key:

```bash
python3 weather/weather.py ahmedabad
python3 weather/weather.py davao
```

The cities use their own time zones (`Asia/Kolkata` and `Asia/Manila`) when selecting the current forecast hour, avoiding a mismatch between the computer's local time and Davao's forecast.

To add a city, extend `CITIES` in `weather/weather.py`, create a matching Conky configuration, and add it to the launcher.

### Palette

| Color | Hex | Use |
| --- | --- | --- |
| Light gray | `#d8d8d8` | Primary text |
| Soft lavender | `#b8a9d9` | Headings and accents |
| Soft peach | `#f2c6a0` | Clock and prominent time |
| Light cyan | `#8fd3e8` | Temperature and information |
| Warm yellow | `#f4d06f` | Weather icons and highlights |
| Muted blue | `#8fa8c7` | Secondary information and forecast times |

## Known limitation

At login, Cinnamon can make a Conky window available before its final geometry has settled. The launcher includes a short startup delay, but a widget may occasionally be positioned incorrectly. Restarting the launcher after the desktop finishes loading restores the intended layout.

For a more robust setup, wait until each window's dimensions are stable before calculating its position in `start-stellar.sh`.

## Roadmap

- Finish and precisely position the Eww circular workspace indicator
- Hide Cinnamon's native workspace-switcher after the Eww indicator is ready
- Add and theme a GLava audio spectrum visualizer in the center of Workspace 2
- Continue refining widget alignment and spacing

## Credits

Inspired by the LinuxFam “Stellar Dust” aesthetic, recreated with free and self-configured components.
