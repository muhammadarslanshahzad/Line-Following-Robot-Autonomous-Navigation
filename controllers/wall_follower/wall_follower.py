from controller import Robot

# =========================================
# CREATE ROBOT
# =========================================
robot = Robot()

timestep = 32
max_speed = 6.28

# =========================================
# MOTORS
# =========================================
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# =========================================
# IR SENSORS
# =========================================
left_ir = robot.getDevice('ir0')
right_ir = robot.getDevice('ir1')

left_ir.enable(timestep)
right_ir.enable(timestep)

# =========================================
# PARAMETERS
# =========================================

# line threshold
threshold = 15

# movement
base_speed = 1.5

# steering strength
Kp = 0.15

# remembers previous direction
last_error = 0

# =========================================
# BASE DETECTION VARIABLES
# =========================================

# ignore base during startup
startup_counter = 0

# base detection counter
base_detect_counter = 0

# robot has left base
lap_started = False

print("Smart Line Follower Started")

# =========================================
# MAIN LOOP
# =========================================
while robot.step(timestep) != -1:

    # =========================
    # READ SENSORS
    # =========================
    left = left_ir.getValue()
    right = right_ir.getValue()

    print(f"left={left:.2f}, right={right:.2f}")

    # =========================
    # STARTUP TIMER
    # =========================
    startup_counter += 1

    # after few seconds allow base detection
    if startup_counter > 120:
        lap_started = True

    # =====================================
    # BASE DETECTION
    # =====================================
    # both sensors strongly detect black
    # for long enough duration
    # =====================================

    if lap_started:

        if left < 8 and right < 8:
            base_detect_counter += 1
        else:
            base_detect_counter = 0

        # stop after reaching base
        if base_detect_counter > 60:

            print("BASE REACHED")

            left_motor.setVelocity(0.0)
            right_motor.setVelocity(0.0)

            break

    # =====================================
    # LINE LOST CONDITION
    # =====================================
    if left > threshold and right > threshold:

        # rotate toward last known line direction
        if last_error > 0:
            left_speed = 2.0
            right_speed = -2.0
        else:
            left_speed = -2.0
            right_speed = 2.0

    else:

        # =====================================
        # LINE FOLLOWING
        # =====================================
        error = left - right

        last_error = error

        correction = Kp * error

        left_speed = base_speed - correction
        right_speed = base_speed + correction

        # =====================================
        # SHARP CURVE SUPPORT
        # =====================================
        if abs(error) > 15:

            if error > 0:
                # turn right hard
                left_speed = 0.5
                right_speed = 2.5
            else:
                # turn left hard
                left_speed = 2.5
                right_speed = 0.5

    # =====================================
    # LIMIT MOTOR SPEEDS
    # =====================================
    left_speed = max(-max_speed, min(max_speed, left_speed))
    right_speed = max(-max_speed, min(max_speed, right_speed))

    # =====================================
    # APPLY SPEEDS
    # =====================================
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)