# ECB Packet Structure Documentation

## Request Packet Structure

![Request Diagram](request_packet_structure.png)

| Name | Size | Bit Offsets | Description |
|------|------|--------------|-------------|
| reqVld | 1 bit | 44 | Describes whether the request being sent is valid or not |
| SID | 8 bits | 43-36 | Sensor ID that describes the type of the target sensor |
| cmdType | 4 bits | 35-32 | Command Type of the request to the sensor |
| CtlData | 32 bits | 31-0 | Data that is to be sent to the sensor to perform the desired action |
## Response Packet Structure

![Response Diagram](response_packet_structure.png)

| Name | Size | Bit Offsets | Description |
|------|------|--------------|-------------|
| respVld | 1 bit | 40 | Describes whether the response being sent is valid or not |
| SID | 8 bits | 39-32 | Sensor ID that describes the type of the target sensor |
| respData | 32 bits | 31-0 | Data that is to be sent from the sensor to the control hub |
