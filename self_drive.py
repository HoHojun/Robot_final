import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class SelfDrive(Node):
    def __init__(self):
        super().__init__('self_drive')
        lidar_qos_profile = QoSProfile(reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
                                       history=rclpy.qos.HistoryPolicy.KEEP_LAST,
                                       depth=1)
        vel_qos_profile = QoSProfile(depth=10)
        self.sub_scan = self.create_subscription(
            LaserScan,
            '/scan',
            self.subscribe_scan,
            lidar_qos_profile)
        self.pub_velo = self.create_publisher(Twist, '/cmd_vel', vel_qos_profile)
        self.step = 0

    def subscribe_scan(self, scan):
        twist = Twist()
        if (0.01 < scan.ranges[0] < 0.25) or (0.01 < scan.ranges[15] < 0.25) or (0.01 < scan.ranges[25] < 0.25) or (0.01 < scan.ranges[35] < 0.25):
            if (scan.ranges[45] < scan.ranges[135] and scan.ranges[45] < 0.25) and (scan.ranges[135] > 0.25):
                twist.linear.x = 0.16
                twist.angular.z = -0.6
                self.get_logger().info(f"scan: {scan.ranges[45]}, {scan.ranges[135]}, go and turn clockwise")
            else:
                twist.linear.x = 0.
                twist.angular.z = -1.
                self.get_logger().info(f"scan: {scan.ranges[45]}, {scan.ranges[135]}, stop and turn clockwise")
        elif (scan.ranges[30] > scan.ranges[150]) and (scan.ranges[30] > 0.25) or ((0.01 < scan.ranges[345] < 0.25) or (0.01 < scan.ranges[330] < 0.25) or (0.01 < scan.ranges[315] < 0.25)):
            twist.linear.x = 0.16
            twist.angular.z = 0.6
            self.get_logger().info(f"scan: {scan.ranges[30]}, {scan.ranges[150]}, go and turn counter clockwise")
        elif (scan.ranges[90] < 0.25) and (scan.ranges[60] > 0.25 or scan.ranges[120] > 0.25):
            twist.linear.x = 0.1
            twist.angular.z = 0.8
            self.get_logger().info(f"scan: {scan.ranges[60]}, {scan.ranges[120]}, stop and turn clockwise")
        else:
            twist.linear.x = 0.16
            twist.angular.z = 0.
            self.get_logger().info(f"scan : {scan.ranges[0]}, forward")
        self.pub_velo.publish(twist)



def main(args=None):
    rclpy.init(args=args)
    node = SelfDrive()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()
