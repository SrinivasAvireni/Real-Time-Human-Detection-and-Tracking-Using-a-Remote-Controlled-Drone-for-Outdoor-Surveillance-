from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Set the connection string to your Pixhawk
connection_string = "/dev/ttyAMA0"  # Update this with your actual connection string

# Connect to the vehicle
print("Connecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, baud=57600, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

try:
    # Print some basic vehicle information
    print("Vehicle attributes:")
    print("  Autopilot Firmware version: %s" % vehicle.version)
    print("  Vehicle mode: %s" % vehicle.mode.name)
    print("  Global Location: %s" % vehicle.location.global_frame)
    print("  GPS satellites visible: %s" % vehicle.gps_0.satellites_visible)

    # Test successful connection
    print("Connection successful!")

    # Arm and take off to 2 meters
    arm_and_takeoff(2)

    print("Switching to LOITER mode")
    vehicle.mode = VehicleMode("LOITER")

    print("Hovering for 5 seconds")
    time.sleep(5)

    print("Landing")
    vehicle.mode = VehicleMode("LAND")

    while vehicle.armed:
        print(" Waiting for disarming...")
        time.sleep(1)

finally:
    # Close the vehicle object before exiting
    vehicle.close()
    print("Vehicle connection closed.")
