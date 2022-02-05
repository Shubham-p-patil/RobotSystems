import logging
import time

class Interpretation(object):
    def __init__(self,sensitivity,polarity):
        self.sensitivity = sensitivity
        self.polarity = polarity
    
    def interpret_data_concurrently(self, in_bus, out_bus, delay, kill_thread):
        while not kill_thread.is_set():
            sensor_vals = in_bus.read()
            if sensor_vals is not None:
                control_val = self.processing_data(sensor_vals)
                out_bus.write(control_val)
            time.sleep(delay)

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