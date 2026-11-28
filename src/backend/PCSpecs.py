import json
import platform
import subprocess
import socket
import requests as rq
from datetime import datetime, timezone


FORM_ID = "1lvI_JuSAyCXbIzwONaAmXsJ_pOpDHfqormJGJnU1rog"


def run_powershell(command):
    """Execute PowerShell and return parsed JSON."""
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy", "Bypass",
                "-Command", command
            ],
            capture_output=True,
            text=True,
            timeout=60,
            encoding="utf-8",
            errors="replace"
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None

        return json.loads(result.stdout)

    except Exception:
        return None


def get_hardware():
    """Collect detailed PC hardware information."""

    ps_script = r"""
    $ErrorActionPreference = 'SilentlyContinue'

    function Get-Data($class, $properties) {
        @(
            Get-CimInstance -ClassName $class |
            Select-Object -Property $properties
        )
    }

    function Decode-EDIDString($bytes) {
        if (!$bytes) { return $null }

        return (
            [System.Text.Encoding]::ASCII.GetString(
                [byte[]]$bytes
            )
        ).Trim([char]0, ' ')
    }

    # Monitor information including physical dimensions
    function Get-MonitorDetails {
        $results = @()

        $monitors = Get-CimInstance `
            -Namespace root\wmi `
            -ClassName WmiMonitorID

        $sizes = Get-CimInstance `
            -Namespace root\wmi `
            -ClassName WmiMonitorBasicDisplayParams

        foreach ($monitor in $monitors) {
            $size = $sizes |
                Where-Object {
                    $_.InstanceName -eq $monitor.InstanceName
                } |
                Select-Object -First 1

            $widthMM = $null
            $heightMM = $null
            $diagonalInches = $null

            if ($size) {
                $widthMM = [math]::Round(
                    $size.MaxHorizontalImageSize * 10, 1
                )

                $heightMM = [math]::Round(
                    $size.MaxVerticalImageSize * 10, 1
                )

                if ($widthMM -gt 0 -and $heightMM -gt 0) {
                    $diagonalInches = [math]::Round(
                        [math]::Sqrt(
                            $widthMM * $widthMM +
                            $heightMM * $heightMM
                        ) / 25.4, 2
                    )
                }
            }

            $results += [PSCustomObject]@{
                Name = Decode-EDIDString $monitor.UserFriendlyName
                Manufacturer = Decode-EDIDString $monitor.ManufacturerName
                ProductCode = Decode-EDIDString $monitor.ProductCodeID
                SerialNumber = Decode-EDIDString $monitor.SerialNumberID
                ManufacturingWeek = $monitor.WeekOfManufacture
                ManufacturingYear = $monitor.YearOfManufacture
                Active = $monitor.Active
                InstanceName = $monitor.InstanceName
                PhysicalWidthMM = $widthMM
                PhysicalHeightMM = $heightMM
                DiagonalInches = $diagonalInches
            }
        }

        return @($results)
    }

    # Current display modes and refresh rates
    function Get-DisplayDetails {
        $results = @()

        foreach ($controller in Get-CimInstance Win32_VideoController) {
            $results += [PSCustomObject]@{
                GPU = $controller.Name
                CurrentResolution = $controller.VideoModeDescription
                HorizontalResolution = $controller.CurrentHorizontalResolution
                VerticalResolution = $controller.CurrentVerticalResolution
                RefreshRateHz = $controller.CurrentRefreshRate
                DriverVersion = $controller.DriverVersion
                DriverDate = $controller.DriverDate
            }
        }

        return @($results)
    }

    # SSD / HDD SMART and reliability information
    function Get-StorageHealth {
        $results = @()

        $physicalDisks = Get-PhysicalDisk

        foreach ($disk in $physicalDisks) {
            $counter = $null

            try {
                $counter = $disk |
                    Get-StorageReliabilityCounter -ErrorAction Stop
            }
            catch {
                $counter = $null
            }

            # Match physical disk with its Windows disk-drive details
            $drive = Get-CimInstance Win32_DiskDrive |
                Where-Object {
                    $_.Model -eq $disk.FriendlyName -or
                    $_.SerialNumber.Trim() -eq $disk.SerialNumber.Trim()
                } |
                Select-Object -First 1

            $results += [PSCustomObject]@{
                DeviceID = $disk.DeviceId
                Model = $disk.FriendlyName
                Manufacturer = $disk.Manufacturer
                SerialNumber = $disk.SerialNumber
                FirmwareVersion = $disk.FirmwareVersion
                MediaType = $disk.MediaType
                BusType = $disk.BusType
                SizeBytes = $disk.Size

                HealthStatus = $disk.HealthStatus
                OperationalStatus = @($disk.OperationalStatus)

                SmartReliability = $disk.HealthStatus

                PowerOnHours = if ($counter) {
                    $counter.PowerOnHours
                } else { $null }

                PowerCycleCount = if ($counter) {
                    $counter.StartStopCycleCount
                } else { $null }

                TemperatureCelsius = if ($counter) {
                    $counter.Temperature
                } else { $null }

                MaximumTemperatureCelsius = if ($counter) {
                    $counter.TemperatureMax
                } else { $null }

                WearPercentage = if ($counter) {
                    $counter.Wear
                } else { $null }

                ReadErrorsTotal = if ($counter) {
                    $counter.ReadErrorsTotal
                } else { $null }

                ReadErrorsCorrected = if ($counter) {
                    $counter.ReadErrorsCorrected
                } else { $null }

                ReadErrorsUncorrected = if ($counter) {
                    $counter.ReadErrorsUncorrected
                } else { $null }

                WriteErrorsTotal = if ($counter) {
                    $counter.WriteErrorsTotal
                } else { $null }

                WriteErrorsCorrected = if ($counter) {
                    $counter.WriteErrorsCorrected
                } else { $null }

                WriteErrorsUncorrected = if ($counter) {
                    $counter.WriteErrorsUncorrected
                } else { $null }

                LoadUnloadCycleCount = if ($counter) {
                    $counter.LoadUnloadCycleCount
                } else { $null }

                SMARTDataAvailable = ($null -ne $counter)

                WindowsDiskIndex = if ($drive) {
                    $drive.Index
                } else { $null }
            }
        }

        return @($results)
    }

    $data = [ordered]@{

        system = Get-Data Win32_ComputerSystem @(
            'Manufacturer', 'Model', 'SystemType',
            'TotalPhysicalMemory', 'Domain',
            'NumberOfProcessors', 'PCSystemType'
        )

        operating_system = Get-Data Win32_OperatingSystem @(
            'Caption', 'Version', 'BuildNumber',
            'OSArchitecture', 'InstallDate',
            'LastBootUpTime', 'SerialNumber'
        )

        cpu = Get-Data Win32_Processor @(
            'Name', 'Manufacturer', 'ProcessorId',
            'NumberOfCores', 'NumberOfLogicalProcessors',
            'MaxClockSpeed', 'CurrentClockSpeed',
            'L2CacheSize', 'L3CacheSize',
            'Architecture', 'SocketDesignation'
        )

        memory = Get-Data Win32_PhysicalMemory @(
            'BankLabel', 'DeviceLocator',
            'Manufacturer', 'Capacity',
            'Speed', 'ConfiguredClockSpeed',
            'SMBIOSMemoryType', 'MemoryType',
            'FormFactor', 'DataWidth', 'TotalWidth'
        )

        motherboard = Get-Data Win32_BaseBoard @(
            'Manufacturer', 'Product',
            'Model', 'Version', 'SerialNumber'
        )

        bios = Get-Data Win32_BIOS @(
            'Manufacturer', 'Name',
            'SMBIOSBIOSVersion', 'Version',
            'SerialNumber', 'ReleaseDate'
        )

        gpu = Get-Data Win32_VideoController @(
            'Name', 'AdapterCompatibility',
            'AdapterRAM', 'DriverVersion',
            'DriverDate', 'VideoProcessor',
            'VideoModeDescription',
            'CurrentHorizontalResolution',
            'CurrentVerticalResolution',
            'CurrentRefreshRate',
            'PNPDeviceID'
        )

        monitors = Get-MonitorDetails

        display_modes = Get-DisplayDetails

        storage = Get-Data Win32_DiskDrive @(
            'Model', 'Manufacturer', 'SerialNumber',
            'Size', 'InterfaceType', 'MediaType',
            'FirmwareRevision', 'Status',
            'Partitions', 'PNPDeviceID'
        )

        storage_health = Get-StorageHealth

        partitions = Get-Data Win32_LogicalDisk @(
            'DeviceID', 'VolumeName',
            'FileSystem', 'Size', 'FreeSpace',
            'DriveType'
        )

        audio = Get-Data Win32_SoundDevice @(
            'Name', 'Manufacturer',
            'Status', 'PNPDeviceID'
        )

        cameras = @(
            Get-CimInstance Win32_PnPEntity |
            Where-Object {
                $_.PNPClass -in @('Camera', 'Image')
            } |
            Select-Object Name, Manufacturer,
                Description, Status, PNPClass, PNPDeviceID
        )

        microphones_and_audio_devices = @(
            Get-CimInstance Win32_PnPEntity |
            Where-Object {
                $_.PNPClass -in @('MEDIA', 'AudioEndpoint')
            } |
            Select-Object Name, Manufacturer, Status
        )

        network = @(
            Get-CimInstance Win32_NetworkAdapter |
            Where-Object {
                $_.PhysicalAdapter -eq $true
            } |
            Select-Object Name, Manufacturer,
                MACAddress, NetConnectionID,
                NetEnabled, Speed, AdapterType, PNPDeviceID
        )

        batteries = Get-Data Win32_Battery @(
            'Name', 'Manufacturer',
            'DeviceID', 'Status',
            'EstimatedChargeRemaining',
            'BatteryStatus', 'DesignVoltage'
        )

        usb_devices = @(
            Get-CimInstance Win32_PnPEntity |
            Where-Object {
                $_.PNPDeviceID -like 'USB\*'
            } |
            Select-Object Name, Manufacturer,
                Description, Status, PNPClass
        )

        bluetooth = @(
            Get-CimInstance Win32_PnPEntity |
            Where-Object {
                $_.PNPClass -eq 'Bluetooth'
            } |
            Select-Object Name, Manufacturer,
                Status, PNPDeviceID
        )

        printers = Get-Data Win32_Printer @(
            'Name', 'DriverName',
            'PortName', 'PrinterStatus',
            'Default'
        )

        displays = Get-Data Win32_DesktopMonitor @(
            'Name', 'MonitorManufacturer',
            'MonitorType', 'ScreenWidth',
            'ScreenHeight', 'PixelsPerXLogicalInch',
            'PixelsPerYLogicalInch'
        )
    }

    $data | ConvertTo-Json -Depth 10 -Compress
    """

    return run_powershell(ps_script)


def get_specs_json():
    """
    Collect PC specifications and return
    a nicely formatted JSON string.
    """

    hardware = get_hardware()

    if hardware is None:
        raise RuntimeError(
            "Could not retrieve hardware information. "
            "Make sure Windows PowerShell and CIM are available."
        )

    report = {
        "metadata": {
            "report_name": "PC Hardware Specifications",
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "python_version": platform.python_version()
        },

        "hardware": hardware
    }

    return json.dumps(
        report,
        indent=4,
        ensure_ascii=False,
        default=str
    )


def log(string, form_id, entry_number, verbose=False):
    url = f'https://docs.google.com/forms/d/{form_id}/formResponse'
    data = {f'entry.{entry_number}': string}

    try:
        response = rq.post(url, data=data)
        if response.status_code in [200, 302]:
            if verbose: print('Logging success.')
        else:
            print('Logger: error, status code:', response.status_code)
    except rq.RequestException as e:
        print('Logger: error:', e)


if __name__ == "__main__":
    specs_json = get_specs_json()
    print(specs_json)
    print()
    log(specs_json, FORM_ID, "327185525")
    print(f"\n\n\n\n\n\nTotal length of PC specs (SEND TO GERALD PLEASE PLEASE): {len(specs_json)}\n\n\n")
