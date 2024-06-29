from dronekit import connect

# Set the connection string to your Pixhawk
connection_string = "/dev/ttyAMA0"  # Update this with your actual connection string

# Connect to the vehicle
print("Connecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, baud=57600, wait_ready=True)

try:
    # Print some basic vehicle information
    print("Vehicle attributes:")
    print("  Autopilot Firmware version: %s" % vehicle.version)
    print("  Vehicle mode: %s" % vehicle.mode.name)
    print("  Global Location: %s" % vehicle.location.global_frame)
    print("  GPS satellites visible: %s" % vehicle.gps_0.satellites_visible)

    # Test successful connection
    print("Connection successful!")

finally:
    # Close the vehicle object before exiting
    vehicle.close()
    print("Vehicle connection closed.")
