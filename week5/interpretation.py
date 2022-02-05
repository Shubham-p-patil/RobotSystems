import logging
import time

class InfraredInterpreter(object):
    def __init__(self,sensitivity,polarity):
        self.sensitivity = sensitivity
        self.polarity = polarity

    def processing_data(self, sensor_list):
        current_pos = None
        try:
            if abs(sensor_list[0] - sensor_list[2]) > self.sensitivity:
                if sensor_list[0] < sensor_list[2]:
                    if sensor_list[0] + abs((sensor_list[2]-sensor_list[0])/4) > sensor_list[1]:
                        current_pos = .5 * self.polarity   
                    else:
                        current_pos = 1* self.polarity
                else:
                    if sensor_list[2]+abs((sensor_list[2]-sensor_list[0])/4) < sensor_list[1]:
                        current_pos = -1 * self.polarity   
                    else:
                        current_pos = -.5* self.polarity
            else:
                current_pos = 0
        except :
            logging.info("robot pos: {0}".format(current_pos))

        return current_pos

class UltrasonicInterpreter():
    def __init__(self, thresh= 10):
        self.threshold = thresh
        self.stop = False

    def obstacle_detection_response(self, distance):
        if distance < self.threshold:
            self.stop = True
        else:
            self.stop = False

        return self.stop