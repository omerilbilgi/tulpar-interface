import serial
import serial.tools.list_ports
from time import sleep
import struct
import constants as cns
import csv


class Communication:

    def __init__(self, port, baud, widget):

        self.baudrate = baud
        self.portName = port
        self.widget = widget
        self.q = False
        self.ser = serial.Serial()

    def connect(self):

        try:
            self.ser = serial.Serial(self.portName, self.baudrate)
            print("Connected : ", self.portName)
            self.q = True
            return True

        except serial.serialutil.SerialException:
            print("Can't open : ", self.portName)
            return False

    def disconnect(self):

        if self.ser.isOpen():
            self.ser.close()
            print("Disconnected : ", self.portName)
            self.q = False

    def getData(self):

        line = []
        last = b'\x00'
        lastlast = b'\x00'

        while self.q:
            try:
                byte = self.ser.read()
                if byte == cns.HEADER_BYTE_2 and len(line) == 0:
                    1 == 1

                elif byte == cns.HEADER_BYTE_1 and last == cns.HEADER_BYTE_2 and len(line) == 0:
                    line.append(last)
                    line.append(byte)

                elif byte and last == cns.FINISH_BYTE_1 and lastlast == cns.FINISH_BYTE_2 and len(line) == cns.TELEMETRY_LEN-1:
                    line.append(byte)
                    self.pckParser(line)
                    line = []
                    sleep(cns.TELEMETRY_PERIOD)

                elif byte and len(line) != 0:
                    line.append(byte)

                if len(line) >= cns.TELEMETRY_LEN:
                    line = []

                lastlast = last
                last = byte

            except BaseException as be:
                print("Serial exception, read at: ", self.portName)
                print("Exception: ", be)

    def pckParser(self, line):

        # header = line[0] + line[1]
        length = line[2]
        length = int.from_bytes(length, "little", signed=False)
        paket_no = line[4] + line[5]
        paket_no = int.from_bytes(paket_no, "little", signed=False)
       
        status = line[6]
        status = int.from_bytes(status, "little", signed=False)
        aras = line[7]
        aras = int.from_bytes(aras, "little", signed=False)
        day = line[8]
        day = int.from_bytes(day, "little", signed=False)
        month = line[9]
        month = int.from_bytes(month, "little", signed=False)
        year = line[10]
        year = int.from_bytes(year, "little", signed=False)
        hour = line[11]
        hour = int.from_bytes(hour, "little", signed=False)
        minute = line[12]
        minute = int.from_bytes(minute, "little", signed=False)
        second = line[13]
        second = int.from_bytes(second, "little", signed=False)

        pressure_pl = line[14] + line[15] + line[16] +  line[17]
        [pressure_pl] = struct.unpack("f", pressure_pl)
        pressure_car = line[18] + line[19] + line[20] + line[21]
        [pressure_car] = struct.unpack("f", pressure_car)

        height_pl = line[22] + line[23] + line[24] + line[25]
        [height_pl] = struct.unpack("f", height_pl)
        height_car = line[26] + line[27] + line[28] + line[29]
        [height_car] = struct.unpack("f", height_car)
        height_diff = line[30] + line[31] + line[32] +  line[33]
        [height_diff] = struct.unpack("f", height_diff)

        speed = line[34] + line[35] + line[36] + line[37]
        [speed] = struct.unpack("f", speed)
        tempe = line[38] + line[39] + line[40] + line[41]
        [tempe] = struct.unpack("f", tempe)
        b_voltage = line[42] + line[43] + line[44] + line[45]
        [b_voltage] = struct.unpack("f", b_voltage)

        latitude_pl = line[46] + line[47] + line[48] + line[49]
        [latitude_pl] = struct.unpack("f", latitude_pl)
        longitude_pl = line[50] + line[51] + line[52] + line[53]
        [longitude_pl] = struct.unpack("f", longitude_pl)
        altitude_pl = line[54] + line[55] + line[56] + line[57] 
        [altitude_pl] = struct.unpack("f", altitude_pl)

        yaw = line[58] + line[59] + line[60] + line[61]
        [yaw] = struct.unpack("f", yaw)
        roll = line[62] + line[63] + line[64] + line[65]
        [roll] = struct.unpack("f", roll)
        pitch = line[66] + line[67] + line[68] + line[69]
        [pitch] = struct.unpack("f", pitch)

        takim_no = line[70] + line[71]
        takim_no = int.from_bytes(takim_no, "little", signed=False)
        takim_no = takim_no * 8

        finish = line[72] + line[73]
        finish = int.from_bytes(finish, "little", signed=False)

        crc = line[74]
        crc = int.from_bytes(crc, "little", signed=False)
    #    return_number = line[82]
    #    return_number = int.from_bytes(return_number, "little", signed=False)
    #    video_status = line[83]
    #    video_status = int.from_bytes(video_status, "little", signed=False)
    #    weather_forecast = line[84]
    #    weather_forecast = int.from_bytes(weather_forecast, "little", signed=False)
        
    #   altitude_car = line[57] + line[58] + line[59] + line[60]
    #   [altitude_car] = struct.unpack("f", altitude_car)
    #   latitude_car = line[61] + line[62] + line[63] + line[64]
    #  [latitude_car] = struct.unpack("f", latitude_car)
    #  longitude_car = line[65] + line[66] + line[67] + line[68]
    #  [longitude_car] = struct.unpack("f", longitude_car)

        
        # humidity = humidity[85]+lihumidityne[86]+humidity[87]+humidity[88]
        # [humidity] = struct.unpack("f", humidity)
        # finish = line[89:91]
        # crc = line[91]

        row = []
        row.append(takim_no)
        row.append(paket_no)
        date = str(hour) + ":" + str(minute) + ":" + str(second) + " " + str(day) + "/" + str(month) + "/" + str(year)
        row.append(date)
        row.append(float("{:.2f}".format(pressure_pl)))
        row.append(float("{:.2f}".format(pressure_car)))
        row.append(float("{:.2f}".format(height_pl)))
        row.append(float("{:.2f}".format(height_car)))
        row.append(float("{:.2f}".format(height_diff)))
        row.append(float("{:.2f}".format(speed)))
        row.append(float("{:.2f}".format(tempe)))
        row.append(float("{:.2f}".format(b_voltage)))
        row.append(latitude_pl)
        row.append(longitude_pl)
        row.append(float("{:.2f}".format(altitude_pl)))
    #    row.append(latitude_car)
    #    row.append(longitude_car)
    #    row.append(float("{:.2f}".format(altitude_car)))
        row.append(status)
        row.append(float("{:.2f}".format(yaw)))
        row.append(float("{:.2f}".format(roll)))
        row.append(float("{:.2f}".format(pitch)))
    #    row.append(return_number)
    #    row.append(video_status)
    #    row.append(weather_forecast)
        # print(row)
        
        # update csv and telemetry table
        with open(self.widget.session_directory + cns.TELEMETRY_FILE_NAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        self.widget.addRow(row)

        # update graphs
        self.widget.graphs.update_pl(latitude_pl, longitude_pl)
        self.widget.graphs.update_car(pitch, roll, yaw)
        self.widget.graphs.update_sp_tmp_v(abs(speed), tempe, b_voltage)
        self.widget.graphs.update_pressure(pressure_pl, pressure_car)
        self.widget.graphs.update_height(height_pl, height_car)
    #    self.widget.graphs.update_altitude(altitude_pl, altitude_car)

        # update pitch-roll-yaw
        new_pitch = (pitch/90) * 45
        new_roll = (roll/90) * 45
        # new_yaw = (yaw/90) * 45
        self.widget.transform.Identity()
        self.widget.transform.RotateX(new_pitch - 45)
        self.widget.transform.RotateY(new_roll)
        # self.widget.transform.RotateZ(new_yaw)
        self.widget.transformFilter.SetTransform(self.widget.transform)
        self.widget.transform.Update()
        self.widget.mapper.StaticOn()
        self.widget.transformFilter.Update()
        self.widget.ren.RemoveCuller(self.widget.ren.GetCullers().GetLastItem())
        self.widget.actor.SetUserTransform(self.widget.transform)
        self.widget.mapper.SetInputConnection(self.widget.transformFilter.GetOutputPort())
        self.widget.vtkWidget.update()
        self.widget.setPRY(float("{:.2f}".format(pitch)), float("{:.2f}".format(roll)), float("{:.2f}".format(yaw)))

        # update map, height diff, status and video status
    #    self.widget.updateLatLon(latitude_pl, longitude_pl, latitude_car, longitude_car)
        self.widget.setHeightDiff(float("{:.2f}".format(height_diff)))
        self.widget.setStatus(status)     
    #    self.widget.setVideoStatus(video_status)
