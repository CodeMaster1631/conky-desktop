#!/bin/bash

sleep 3

# Start the Eww floating panel after Cinnamon has initialized the display.
/usr/local/bin/eww daemon >/dev/null 2>&1
/usr/local/bin/eww open panel >/dev/null 2>&1
/home/abby/.config/eww/place-panel.sh

# Get primary display dimensions
read WIDTH HEIGHT <<< "$(xdpyinfo | awk '/dimensions:/ {print $2}' | tr 'x' ' ')"

# Start Conky instances
conky -c "$HOME/.config/conky/stellar-left.conf" &
conky -c "$HOME/.config/conky/stellar-right.conf" &
conky -c "$HOME/.config/conky/stellar-ahmedabad.conf" &
conky -c "$HOME/.config/conky/stellar-davao.conf" &
conky -c "$HOME/.config/conky/stellar-quote.conf" &

# Wait for a specific window to appear
wait_for_window() {
    local CLASS="$1"
    local WINDOW=""

    while [ -z "$WINDOW" ]; do
        WINDOW=$(xdotool search --class "$CLASS" 2>/dev/null | head -1)
        sleep 0.01
    done

    echo "$WINDOW"
}

# Get window IDs as soon as they exist
LEFT=$(wait_for_window "StellarLeft")
RIGHT=$(wait_for_window "StellarRight")
AHMEDABAD=$(wait_for_window "StellarAhmedabad")
DAVAO=$(wait_for_window "StellarDavao")
QUOTE=$(wait_for_window "StellarQuote")

# -----------------------------
# Left
# -----------------------------

LEFT_X=$(awk "BEGIN {printf \"%.0f\", $WIDTH * 0.1}")
LEFT_Y=$(awk "BEGIN {printf \"%.0f\", $HEIGHT * 0.3}")

# -----------------------------
# Right
# -----------------------------

RIGHT_W=$(xdotool getwindowgeometry --shell "$RIGHT" \
    | awk -F= '$1=="WIDTH"{print $2}')

RIGHT_X=$(awk "BEGIN {printf \"%.0f\", $WIDTH * 0.90 - $RIGHT_W}")
RIGHT_Y=$(awk "BEGIN {printf \"%.0f\", $HEIGHT * 0.15}")

# -----------------------------
# Center quote
# -----------------------------

QUOTE_W=$(xdotool getwindowgeometry --shell "$QUOTE" \
    | awk -F= '$1=="WIDTH"{print $2}')

QUOTE_X=$(awk "BEGIN {printf \"%.0f\", ($WIDTH - $QUOTE_W) / 2}")
QUOTE_Y=$(awk "BEGIN {printf \"%.0f\", $HEIGHT * 0.55}")

# -----------------------------
# Weather center (origin)
# -----------------------------

# (0,0) below = dead center of the screen. Each box is placed by
# telling it how far its own center should sit from that origin -
# negative X = left of center, positive X = right of center;
# negative Y = above center, positive Y = below center.

WEATHER_W=300   # fixed - both confs pin minimum_width = maximum_width = 300
WEATHER_H=150   # approx rendered height - nudge this if it doesn't match once you eyeball it

ORIGIN_X=$(awk "BEGIN {printf \"%.0f\", $WIDTH / 2 - $WEATHER_H / 2}")
ORIGIN_Y=$(awk "BEGIN {printf \"%.0f\", $HEIGHT / 2 - $WEATHER_W / 2}")

# -----------------------------
# Ahmedabad - move me with these two numbers
# -----------------------------

AHMEDABAD_OFFSET_X=-1100
AHMEDABAD_OFFSET_Y=-50

AHMEDABAD_X=$(awk "BEGIN {printf \"%.0f\", $ORIGIN_X + ($AHMEDABAD_OFFSET_X) - $WEATHER_W/2}")
AHMEDABAD_Y=$(awk "BEGIN {printf \"%.0f\", $ORIGIN_Y + ($AHMEDABAD_OFFSET_Y) - $WEATHER_H/2}")

# -----------------------------
# Davao - move me with these two numbers
# -----------------------------

DAVAO_OFFSET_X=900
DAVAO_OFFSET_Y=-50

DAVAO_X=$(awk "BEGIN {printf \"%.0f\", $ORIGIN_X + ($DAVAO_OFFSET_X) - $WEATHER_W/2}")
DAVAO_Y=$(awk "BEGIN {printf \"%.0f\", $ORIGIN_Y + ($DAVAO_OFFSET_Y) - $WEATHER_H/2}")

# -----------------------------
# Move windows
# -----------------------------

xdotool windowmove "$LEFT" "$LEFT_X" "$LEFT_Y"
xdotool windowmove "$RIGHT" "$RIGHT_X" "$RIGHT_Y"
xdotool windowmove "$AHMEDABAD" "$AHMEDABAD_X" "$AHMEDABAD_Y"
xdotool windowmove "$DAVAO" "$DAVAO_X" "$DAVAO_Y"
xdotool windowmove "$QUOTE" "$QUOTE_X" "$QUOTE_Y"

# -----------------------------
# Workspace visibility
# -----------------------------

# Start on workspace 1
xdotool windowunmap "$AHMEDABAD"
xdotool windowunmap "$DAVAO"

# Continuously check the active workspace
while true; do

    WORKSPACE=$(xdotool get_desktop)

    if [ "$WORKSPACE" -eq 0 ]; then
        # Workspace 1
        xdotool windowmap "$LEFT"
        xdotool windowmap "$RIGHT"
        xdotool windowmap "$QUOTE"

        xdotool windowunmap "$AHMEDABAD"
        xdotool windowunmap "$DAVAO"

    elif [ "$WORKSPACE" -eq 1 ]; then
        # Workspace 2
        xdotool windowunmap "$LEFT"
        xdotool windowunmap "$RIGHT"
        xdotool windowunmap "$QUOTE"

        xdotool windowmap "$AHMEDABAD"
        xdotool windowmap "$DAVAO"
    fi

    sleep 0.2
done
