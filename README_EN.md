# QuecDuino Entry-Level Sensor Experiment Kit

### **roduct Introduction**

![](media/俯视图.jpg)

This is an entry-level experiment kit built by deeply integrating the EG800Z series QuecDuino development board with over twenty types of sensors and actuators.

The QuecDuino Entry-Level Sensor Experiment Kit is a one-stop development platform tailored for beginners, makers, and the education sector. It perfectly inherits the ease-of-use DNA of Arduino open-source hardware and innovatively integrates Quectel's leading cellular network technology, enabling your IoT ideas to become reality without tedious configuration.

**Product Features**

- **IoT Development**: Unlike the traditional Arduino Uno, this kit has built-in network communication capabilities, allowing your code to connect directly to the Internet without relying on a PC or additional Wi-Fi modules.
- **Zero Barrier for Python**: Leveraging the simplicity of Python, beginners can skip complex register configurations and focus directly on IoT logic and business implementation.
- **Industrial-Grade Stability**: Adopts Quectel industrial-grade modules, supporting a wide operating temperature range of -35°C to 85°C — suitable not only for learning but also for industrial prototype validation.
- **Rich Sensor Selection**: Dozens of sensor peripherals are available for users to learn with, providing a wide range of hardware combinations that perfectly replicate real-world IoT development requirements.

> !! This repository contains experiment cases developed on the QuecPython platform for use with the QuecDuino Entry-Level Sensor Experiment Kit.
>
> For more information on QuecPython platform development, please visit the [QuecPython Documentation Center](vscode-file://vscode-app/d:/Microsoft VS Code/974500e64f/resources/app/out/vs/code/electron-browser/workbench/workbench.html).

### **Example List**

| No.  | Module                                                       |
| ---- | ------------------------------------------------------------ |
| 01   | [LED Module](example/01-led/README.md)                       |
| 02   | [Single Button Module](example/02-key_interrupt/README.md)   |
| 03   | [RGB LED Module](example/03-rgb_led/README.md)               |
| 04   | [Microphone (MIC) Module](example/04-mic/README.md)          |
| 05   | [Buzzer Module](example/05-buzzer/README.md)                 |
| 06   | [Water Level Detection Module](example/06-water_level_detect/README.md) |
| 07   | [Reed Switch Module (KY-025)](example/07-magnetic reed switch(KY-025)/README.md) |
| 08   | [Obstacle Detection Module (KY-032)](example/08-Obstacle Detection Module(KY-032)/README.md) |
| 09   | [Mini Reed Switch (KY-021)](example/09 - Mini Magnetic (KY-021)/README.md) |
| 10   | [Photoresistor Module (KY-018)](example/10-photoresistor(KY-018)/README.md) |
| 11   | [Flame Detection Module (KY-026)](example/11-flame_detect(KY-026)/README.md) |
| 12   | [Magic Light Cup Module (KY-027)](example/12Magic Aura Module (KY-027)/README.md) |
| 13   | [Tilt Switch Module (KY-020)](example/13-Inclination switch module(KY-20)/README.md) |
| 14   | [Ultrasonic Module (HC-SR04)](example/14-Ultrasonic module(HC-SR04)/README.md) |
| 15   | [Human Touch Module (KY-036)](example/15-Human body touch module(KY-036)/README.md) |
| 16   | [Digital Tube Module (JY005)](example/16-Digital tube module(JY005)/README.md) |
| 17   | [Laser Transmitter Module (KY-008)](example/17-Laser emission module(KY-008)/README.md) |
| 18   | [Mercury Switch Module (KY-017)](example/18-Mercury switch module(KY-017)/README.md) |
| 19   | [Temperature & Humidity Sensor (AHT20)](example/19-temperature and humidity sensor(AHT20)/README.md) |
| 20   | [Analog Piezoelectric Vibration Sensor](example/20-Simulated Piezoelectric Ceramic Vibration Sensor/README.md) |

# EG800Z Duino Development Board — Firmware Flashing & Usage Guide

## Tool Downloads

Download the firmware flashing tool and development debugging tool from the links below.

- Firmware Flashing Tool: [QFlash](vscode-file://vscode-app/d:/Microsoft VS Code/974500e64f/resources/app/out/vs/code/electron-browser/workbench/workbench.html)
- Development Debugging Tool: [QPYcom](vscode-file://vscode-app/d:/Microsoft VS Code/974500e64f/resources/app/out/vs/code/electron-browser/workbench/workbench.html)

## Firmware Flashing Guide

### Step 1 — Open QFlash and Load Firmware

> !! Obtain `QPY_OCPU_EG800Z_CNLA_FW.zip` from the `firmware` folder of this repository and extract it.

![](media/1.png)

### Step 2 — Select Firmware File

Select the `at_command.hbinpkg` file from the firmware package. Click **OK** and the firmware will be imported automatically.

![](media/2.png)

### Step 3 — Enter Download Mode

Short-circuit the **BOOT** pin using a jumper wire to enter download mode. Open Device Manager, restart the device, and locate **Quectel QDLoader Port** under "Ports (COM & LPT)". Note the COM port number.

![](media/3.png)

### Step 4 — Start Firmware Download

In QFlash, select the corresponding COM port and click **"Start"** to begin downloading. Wait for the progress bar to complete and display **"PASS"**.

![](media/4.png)

### 5.Download process monitoring

![](media/5.png)

### 6.download completes

![](media/6.png)

## Using the QPYcom Tool

> !! **REPL** stands for **Read-Eval-Print-Loop**. You can use the REPL interface to debug QuecPython programs interactively. It is the primary debugging method provided by QPYcom for the QuecPython platform.
>
> !! QuecPython Quick Start: [https://developer.quectel.com/doc/quecpython/Getting_started/zh/index.html](vscode-file://vscode-app/d:/Microsoft VS Code/974500e64f/resources/app/out/vs/code/electron-browser/workbench/workbench.html)
>
> !! More QPYcom usage: [https://developer.quectel.com/doc/quecpython/Application_guide/zh/dev-tools/QPYcom/index.html](vscode-file://vscode-app/d:/Microsoft VS Code/974500e64f/resources/app/out/vs/code/electron-browser/workbench/workbench.html)

### Debugging via REPL

After launching **QPYcom**, select the correct serial port (baud rate does not need to be specified) and open it to begin Python command-line interaction.

- **Step 1 — Open the Interactive Interface**

  Select **Quectel USB REPL Port** and switch to the "Interactive" tab.

- **Step 2 — Open Serial Port**

  Click **"Open Serial Port"**, then type `print('hello world')` in the interactive window and press Enter. You should see:

  ```python
  >>> print('hello world')
  
   hello world
  ```

  ![](media/qpycom.png)

### Script Download and Execution

> !! All example scripts provided in this repository can be downloaded to the module's `usr` directory and executed.

As shown in the following figure, directly download the local file to the module's usr directory by dragging and dropping.

![](media/QPYcom_drag.jpg)

**Download Workflow:**

- **Step 1 — Open REPL Serial Port**

  Select the module's interactive port and click **"Open Serial Port"**.

- **Step 2 — Upload via Toolbar Button** *(optional)*

  Use the **"+"** and **"-"** buttons on the right side of the File tab to upload or delete files.

- **Step 3 — Upload via Drag and Drop** *(optional)*

  Drag local files (or folders) from the left panel directly into the module's directory on the right panel.

- **Step 4 — Monitor Download Progress**

  The status bar displays the file name and download progress during the transfer.

- **Step 5 — Run the Script**

  Right-click the script file in the right panel and select **Execute**.