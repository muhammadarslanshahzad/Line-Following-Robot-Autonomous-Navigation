# Line-Following Robot (Webots)

Line-following robot in Webots using an e-puck with two IR ground sensors. Follows the line, recovers if it loses it, handles sharp turns, and stops automatically when it returns to the starting point.

## Demo
<video width="640" height="360" controls>
  <source src="assets/lfr_1.mp4" type="video/mp4">
</video>


## Files

```
.
├── lfr.wbt              # Webots world (arena, track, e-puck)
├── wall_follower.py     # Controller logic
└── assets/              # Demo media
```

## Requirements

- Webots R2025a+
- No extra Python packages needed

## Run it

1. Open `lfr.wbt` in Webots.
2. Make sure the e-puck's controller is set to `wall_follower`.
3. Update the track texture path in `lfr.wbt` if needed (currently a local Windows path).
4. Hit Run.

## Key parameters (`wall_follower.py`)

| Param | Value | What it does |
|---|---|---|
| `Kp` | 0.15 | Steering correction strength |
| `base_speed` | 1.5 | Default forward speed |
| `threshold` | 15 | IR value above which line is "lost" |
| `max_speed` | 6.28 | Wheel speed cap |


## Possible improvements

- Add I/D terms for full PID (currently P only)
- Encoder-based lap detection instead of pure sensor-based
