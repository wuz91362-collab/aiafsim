This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: **/*.md, doc/
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
acoustic_demo.txt
acoustic_demo2.txt
```

# Files

## File: acoustic_demo.txt
```
# ****************************************************************************
# CUI
#
# The Advanced Framework for Simulation, Integration, and Modeling (AFSIM)
#
# The use, dissemination or disclosure of data in this file is subject to
# limitation or restriction. See accompanying README and LICENSE for details.
# ****************************************************************************

acoustic_signature ACOUSTIC_SIGNATURE # MADE UP NUMBERS
   data_reference_range 10 feet
   state default
   spectrum_data
        freq    31.5 hz   noise_pressure 20.3 dB_20uPa
        freq    40.0 hz   noise_pressure 20.3 dB_20uPa
        freq    50.0 hz   noise_pressure 20.3 dB_20uPa
        freq    63.0 hz   noise_pressure 20.3 dB_20uPa
        freq    80.0 hz   noise_pressure 20.3 dB_20uPa
        freq    100.0 hz  noise_pressure 20.3 dB_20uPa
        freq    200.0 hz  noise_pressure 20.3 dB_20uPa
        freq    400.0 hz  noise_pressure 20.3 dB_20uPa
        freq    800.0 hz  noise_pressure 20.3 dB_20uPa
        freq    900.0 hz  noise_pressure 20.3 dB_20uPa
        freq   1000.0 hz  noise_pressure 20.3 dB_20uPa
        freq   2000.0 hz  noise_pressure 78.3 dB_20uPa
        freq   2500.0 hz  noise_pressure 30.3 dB_20uPa
        freq   3000.0 hz  noise_pressure 20.3 dB_20uPa
        freq   4000.0 hz  noise_pressure 20.3 dB_20uPa
        freq   5000.0 hz  noise_pressure 20.3 dB_20uPa
        freq   6000.0 hz  noise_pressure 20.3 dB_20uPa
   end_spectrum_data
end_acoustic_signature

platform_type    ACOUSTIC_TARGET       WSF_PLATFORM
  icon c-130
  mover WSF_AIR_MOVER end_mover
  acoustic_signature ACOUSTIC_SIGNATURE
end_platform_type

######################################################
#antenna_pattern ACOUSTIC_SENSOR_PATTERN
#   constant 0 db
#end_antenna_pattern

sensor ACOUSTIC_BASE WSF_ACOUSTIC_SENSOR
   #debug
   on

   acoustic_type human

   frame_time 1 sec
   scan_mode both

   azimuth_scan_limits -180 deg 180 deg
   elevation_scan_limits 0 deg 90 deg

    detection_threshold 0.0 # do not adjust for human hearing

   hits_to_establish_track 2 3
   hits_to_maintain_track 1 2

   reports_bearing
   reports_elevation
   reports_signal_to_noise
end_sensor
####

sensor JUNGLE_DAY_ACOUSTIC_SENSOR ACOUSTIC_BASE
   background_noise jungle_day
   on
end_sensor
platform_type JUNGLE_DAY_ACOUSTIC_PLATFORM WSF_PLATFORM
   icon target
   sensor jungle_day JUNGLE_DAY_ACOUSTIC_SENSOR end_sensor
end_platform_type

####
sensor JUNGLE_NIGHT_ACOUSTIC_SENSOR ACOUSTIC_BASE
   background_noise jungle_night
   on
end_sensor
platform_type JUNGLE_NIGHT_ACOUSTIC_PLATFORM WSF_PLATFORM
   icon target
   sensor jungle_night JUNGLE_NIGHT_ACOUSTIC_SENSOR end_sensor
end_platform_type

####
sensor INDUSTRIAL_ACOUSTIC_SENSOR ACOUSTIC_BASE
   background_noise industrial
   on
end_sensor
platform_type INDUSTRIAL_ACOUSTIC_PLATFORM WSF_PLATFORM
   icon target
   sensor industrial INDUSTRIAL_ACOUSTIC_SENSOR end_sensor
end_platform_type

####
sensor RURAL_ACOUSTIC_SENSOR ACOUSTIC_BASE
   background_noise rural
   on
end_sensor
platform_type RURAL_ACOUSTIC_PLATFORM WSF_PLATFORM
   icon target
   sensor rural RURAL_ACOUSTIC_SENSOR end_sensor
end_platform_type

####
sensor RESIDENTIAL_ACOUSTIC_SENSOR ACOUSTIC_BASE
   background_noise residential
   on
end_sensor
platform_type RESIDENTIAL_ACOUSTIC_PLATFORM WSF_PLATFORM
   icon target
   sensor residential RESIDENTIAL_ACOUSTIC_SENSOR end_sensor
end_platform_type

########################################################################################
platform jungle_day JUNGLE_DAY_ACOUSTIC_PLATFORM
  position 30.1n 30e altitude 1 m agl
  side red
end_platform

platform jungle_night JUNGLE_NIGHT_ACOUSTIC_PLATFORM
  position 30.2n 30e altitude 1 m agl
  side red
end_platform


platform industrial INDUSTRIAL_ACOUSTIC_PLATFORM
  position 30.3n 30e altitude 1 m agl
  side red
end_platform


platform rural RURAL_ACOUSTIC_PLATFORM
  position 30.4n 30e altitude 1 m agl
  side red
end_platform


platform residential RESIDENTIAL_ACOUSTIC_PLATFORM
  position 30.5n 30e altitude 1 m agl
  side red
end_platform

platform player-1 ACOUSTIC_TARGET
  position 29:30:57.34n 30e altitude 1500.00 ft
  side blue
  route
    position 29:30:57.34n 30e altitude 1500.00 ft
    speed 100 kts
    position 30:40:37.43n 30e altitude 1500.00 ft
  end_route
end_platform

platform player-2 ACOUSTIC_TARGET
  side blue
  heading 360 deg
  route
    position 29:30:56.33n 29:54:21.23e altitude 1500.00 ft
    speed 100 kts
    position 30:40:36.42n 29:54:21.23e altitude 1500.00 ft
  end_route
end_platform

platform target3 ACOUSTIC_TARGET
  position 29:30:56.56n 29:48:25.33e altitude 1500.00 ft
  side blue
  route
    position 29:30:56.56n 29:48:25.33e altitude 1500.00 ft speed 100 kts
    position 30:40:36.65n 29:48:25.33e altitude 1500.00 ft speed 100 kts
  end_route
end_platform

platform target4 ACOUSTIC_TARGET
  position 29:31:00.00n 29:40:00.00e altitude 1500.00 ft
  side blue
  route
    position 29:31n 29:40e altitude 1500.00 ft speed 100 kts
    position 30:40:19.29n 29:40e altitude 1500.00 ft speed 100 kts
  end_route
end_platform

#############################################################
event_pipe
   file output/acoustic_demo.aer
end_event_pipe

event_output
   file output/acoustic_demo.evt
   disable all
   enable SENSOR_DETECTION_ATTEMPT
   enable SENSOR_TRACK_INITIATED
   enable SENSOR_TRACK_UPDATED
   enable SENSOR_TRACK_DROPPED
end_event_output

end_time 70 min
```

## File: acoustic_demo2.txt
```
# ****************************************************************************
# CUI
#
# The Advanced Framework for Simulation, Integration, and Modeling (AFSIM)
#
# The use, dissemination or disclosure of data in this file is subject to
# limitation or restriction. See accompanying README and LICENSE for details.
# ****************************************************************************
# TARGET platform types and signature

acoustic_signature ACOUSTIC_SIGNATURE1 # MADE UP NUMBERS
   data_reference_range 10 feet
   state default
   spectrum_data
        freq    31.5 hz   noise_pressure 20.3 dB_20uPa
        freq    40.0 hz   noise_pressure 20.3 dB_20uPa
        freq    50.0 hz   noise_pressure 20.3 dB_20uPa
        freq    63.0 hz   noise_pressure 20.3 dB_20uPa
        freq    80.0 hz   noise_pressure 20.3 dB_20uPa
        freq    100.0 hz  noise_pressure 20.3 dB_20uPa
        freq    200.0 hz  noise_pressure 20.3 dB_20uPa
        freq    400.0 hz  noise_pressure 20.3 dB_20uPa
        freq    800.0 hz  noise_pressure 20.3 dB_20uPa
        freq    900.0 hz  noise_pressure 20.3 dB_20uPa
        freq   1000.0 hz  noise_pressure 40.3 dB_20uPa
        freq   2000.0 hz  noise_pressure 58.3 dB_20uPa
        freq   2500.0 hz  noise_pressure 30.3 dB_20uPa
        freq   3000.0 hz  noise_pressure 20.3 dB_20uPa
   end_spectrum_data
end_acoustic_signature

acoustic_signature ACOUSTIC_SIGNATURE2 # MADE UP NUMBERS
   data_reference_range 10 feet
   state default
   spectrum_data
        freq    31.5 hz   noise_pressure 20.3 dB_20uPa
        freq    40.0 hz   noise_pressure 20.3 dB_20uPa
        freq    50.0 hz   noise_pressure 20.3 dB_20uPa
        freq    63.0 hz   noise_pressure 20.3 dB_20uPa
        freq    80.0 hz   noise_pressure 20.3 dB_20uPa
        freq    100.0 hz  noise_pressure 20.3 dB_20uPa
        freq    200.0 hz  noise_pressure 20.3 dB_20uPa
        freq    400.0 hz  noise_pressure 20.3 dB_20uPa
        freq    800.0 hz  noise_pressure 20.3 dB_20uPa
        freq    900.0 hz  noise_pressure 20.3 dB_20uPa
        freq   1000.0 hz  noise_pressure 40.3 dB_20uPa
        freq   2000.0 hz  noise_pressure 68.3 dB_20uPa
        freq   2500.0 hz  noise_pressure 30.3 dB_20uPa
        freq   3000.0 hz  noise_pressure 20.3 dB_20uPa
   end_spectrum_data
end_acoustic_signature

acoustic_signature ACOUSTIC_SIGNATURE3 # MADE UP NUMBERS
   data_reference_range 10 feet
   state default
   spectrum_data
        freq    31.5 hz   noise_pressure 20.3 dB_20uPa
        freq    40.0 hz   noise_pressure 20.3 dB_20uPa
        freq    50.0 hz   noise_pressure 20.3 dB_20uPa
        freq    63.0 hz   noise_pressure 20.3 dB_20uPa
        freq    80.0 hz   noise_pressure 20.3 dB_20uPa
        freq    100.0 hz  noise_pressure 20.3 dB_20uPa
        freq    200.0 hz  noise_pressure 20.3 dB_20uPa
        freq    400.0 hz  noise_pressure 20.3 dB_20uPa
        freq    800.0 hz  noise_pressure 20.3 dB_20uPa
        freq    900.0 hz  noise_pressure 20.3 dB_20uPa
        freq   1000.0 hz  noise_pressure 40.3 dB_20uPa
        freq   2000.0 hz  noise_pressure 78.3 dB_20uPa
        freq   2500.0 hz  noise_pressure 30.3 dB_20uPa
        freq   3000.0 hz  noise_pressure 20.3 dB_20uPa
   end_spectrum_data
end_acoustic_signature

acoustic_signature ACOUSTIC_SIGNATURE4 # MADE UP NUMBERS
   data_reference_range 10 feet
   state default
   spectrum_data
        freq    31.5 hz   noise_pressure 20.3 dB_20uPa
        freq    40.0 hz   noise_pressure 20.3 dB_20uPa
        freq    50.0 hz   noise_pressure 20.3 dB_20uPa
        freq    63.0 hz   noise_pressure 20.3 dB_20uPa
        freq    80.0 hz   noise_pressure 20.3 dB_20uPa
        freq    100.0 hz  noise_pressure 20.3 dB_20uPa
        freq    200.0 hz  noise_pressure 20.3 dB_20uPa
        freq    400.0 hz  noise_pressure 20.3 dB_20uPa
        freq    800.0 hz  noise_pressure 20.3 dB_20uPa
        freq    900.0 hz  noise_pressure 20.3 dB_20uPa
        freq   1000.0 hz  noise_pressure 40.3 dB_20uPa
        freq   2000.0 hz  noise_pressure 88.3 dB_20uPa
        freq   2500.0 hz  noise_pressure 30.3 dB_20uPa
        freq   3000.0 hz  noise_pressure 20.3 dB_20uPa
   end_spectrum_data
end_acoustic_signature

acoustic_signature ACOUSTIC_SIGNATURE5 # MADE UP NUMBERS
   data_reference_range 10 feet
   state default
   spectrum_data
        freq    31.5 hz   noise_pressure 20.3 dB_20uPa
        freq    40.0 hz   noise_pressure 20.3 dB_20uPa
        freq    50.0 hz   noise_pressure 20.3 dB_20uPa
        freq    63.0 hz   noise_pressure 20.3 dB_20uPa
        freq    80.0 hz   noise_pressure 20.3 dB_20uPa
        freq    100.0 hz  noise_pressure 20.3 dB_20uPa
        freq    200.0 hz  noise_pressure 20.3 dB_20uPa
        freq    400.0 hz  noise_pressure 20.3 dB_20uPa
        freq    800.0 hz  noise_pressure 20.3 dB_20uPa
        freq    900.0 hz  noise_pressure 20.3 dB_20uPa
        freq   1000.0 hz  noise_pressure 40.3 dB_20uPa
        freq   2000.0 hz  noise_pressure 98.3 dB_20uPa
        freq   2500.0 hz  noise_pressure 30.3 dB_20uPa
        freq   3000.0 hz  noise_pressure 20.3 dB_20uPa
   end_spectrum_data
end_acoustic_signature

platform_type ACOUSTIC_TARGET1 WSF_PLATFORM
  icon c-130
  mover WSF_AIR_MOVER end_mover
  acoustic_signature ACOUSTIC_SIGNATURE1
end_platform_type

platform_type ACOUSTIC_TARGET2 WSF_PLATFORM
  icon c-130
  mover WSF_AIR_MOVER end_mover
  acoustic_signature ACOUSTIC_SIGNATURE2
end_platform_type

platform_type ACOUSTIC_TARGET3 WSF_PLATFORM
  icon c-130
  mover WSF_AIR_MOVER end_mover
  acoustic_signature ACOUSTIC_SIGNATURE3
end_platform_type

platform_type ACOUSTIC_TARGET4 WSF_PLATFORM
  icon c-130
  mover WSF_AIR_MOVER end_mover
  acoustic_signature ACOUSTIC_SIGNATURE4
end_platform_type

platform_type ACOUSTIC_TARGET5 WSF_PLATFORM
  icon c-130
  mover WSF_AIR_MOVER end_mover
  acoustic_signature ACOUSTIC_SIGNATURE5
end_platform_type

######################################################
# Sensor type and sensor platform type

sensor ACOUSTIC_BASE WSF_ACOUSTIC_SENSOR
#   debug
   ignore_same_side
   acoustic_type human
   detection_threshold 0.0 # do not adjust for human hearing
   on
   frame_time 0.5 sec
   scan_mode both
   azimuth_scan_limits -180 deg 180 deg
   elevation_scan_limits 0 deg 90 deg
   hits_to_establish_track 2 3
   hits_to_maintain_track 1 2
   reports_bearing
   reports_elevation
   reports_signal_to_noise
end_sensor
####

acoustic_signature BOGUS # MADE UP NUMBERS
   data_reference_range 10 feet
   state default
   spectrum_data
        freq    31.5 hz   noise_pressure 20.3 dB_20uPa
   end_spectrum_data
end_acoustic_signature

sensor JUNGLE_DAY_ACOUSTIC_SENSOR ACOUSTIC_BASE
   background_noise jungle_day
   on
end_sensor
platform_type JUNGLE_DAY_ACOUSTIC_PLATFORM WSF_PLATFORM
   icon target
   sensor jungle_day JUNGLE_DAY_ACOUSTIC_SENSOR end_sensor
   acoustic_signature BOGUS
end_platform_type

####
sensor JUNGLE_NIGHT_ACOUSTIC_SENSOR ACOUSTIC_BASE
   background_noise jungle_night
   on
end_sensor
platform_type JUNGLE_NIGHT_ACOUSTIC_PLATFORM WSF_PLATFORM
   icon target
   sensor jungle_night JUNGLE_NIGHT_ACOUSTIC_SENSOR end_sensor
   acoustic_signature BOGUS
end_platform_type

####
sensor INDUSTRIAL_ACOUSTIC_SENSOR ACOUSTIC_BASE
   background_noise industrial
   on
end_sensor
platform_type INDUSTRIAL_ACOUSTIC_PLATFORM WSF_PLATFORM
   icon target
   sensor industrial INDUSTRIAL_ACOUSTIC_SENSOR end_sensor
   acoustic_signature BOGUS
end_platform_type

####
sensor RURAL_ACOUSTIC_SENSOR ACOUSTIC_BASE
   background_noise rural
   on
end_sensor
platform_type RURAL_ACOUSTIC_PLATFORM WSF_PLATFORM
   icon target
   sensor rural RURAL_ACOUSTIC_SENSOR end_sensor
   acoustic_signature BOGUS
end_platform_type

####
sensor RESIDENTIAL_ACOUSTIC_SENSOR ACOUSTIC_BASE
   background_noise residential
   on
end_sensor
platform_type RESIDENTIAL_ACOUSTIC_PLATFORM WSF_PLATFORM
   icon target
   sensor residential RESIDENTIAL_ACOUSTIC_SENSOR end_sensor
   acoustic_signature BOGUS
end_platform_type

########################################################################################
platform jungle_day_sensor JUNGLE_DAY_ACOUSTIC_PLATFORM
  position 0n 0e altitude 1 m agl
  side red
end_platform


platform jungle_night_sensor JUNGLE_NIGHT_ACOUSTIC_PLATFORM
  position 0n 0e altitude 1 m agl
  side red
end_platform


platform industrial_sensor INDUSTRIAL_ACOUSTIC_PLATFORM
  position 0n 0e altitude 1 m agl
  side red
end_platform


platform rural_sensor RURAL_ACOUSTIC_PLATFORM
  position 0n 0e altitude 1 m agl
  side red
end_platform


platform residential_sensor RESIDENTIAL_ACOUSTIC_PLATFORM
  position 0n 0e altitude 1 m agl
  side red
end_platform

#############################################################
event_pipe
   file output/acoustic_demo2.aer
end_event_pipe

event_output
   file output/acoustic_demo2.evt
   disable all
#   enable SENSOR_DETECTION_ATTEMPT
   enable SENSOR_TRACK_INITIATED
   enable SENSOR_TRACK_DROPPED
end_event_output

end_time 70 min

platform target1 ACOUSTIC_TARGET1
  side blue
  route
    position 00:32s 00:00e altitude 600.00 ft
    speed 100 kts
    position 00:10n 00:00:00.00w altitude 600.00 ft
  end_route
  heading 360 deg
end_platform

platform target2 ACOUSTIC_TARGET2
  side blue
  route
    position 00:32s 00:00e altitude 600.00 ft
    speed 100 kts
    position 00:10n 00:00:00.00w altitude 600.00 ft
  end_route
  heading 360 deg
end_platform

platform target3 ACOUSTIC_TARGET3
  side blue
  route
    position 00:32s 00:00e altitude 600.00 ft
    speed 100 kts
    position 00:10n 00:00:00.00w altitude 600.00 ft
  end_route
  heading 360 deg
end_platform

platform target4 ACOUSTIC_TARGET4
  side blue
  route
    position 00:32s 00:00e altitude 600.00 ft
    speed 100 kts
    position 00:10n 00:00:00.00w altitude 600.00 ft
  end_route
  heading 360 deg
end_platform

platform target5 ACOUSTIC_TARGET5
  side blue
  route
    position 00:32s 00:00e altitude 600.00 ft
    speed 100 kts
    position 00:10n 00:00:00.00w altitude 600.00 ft
  end_route
  heading 360 deg
end_platform

script void SensorDetectionAttempt(WsfPlatform aPlatform, WsfSensor aSensor, WsfPlatform aTarget, WsfSensorInteraction aResult)
   if(aResult.Detected())
   {
      writeln(TIME_NOW, ", ", aSensor.Name(), " ,detected, ", aTarget.Name(), " ,at slantrange, " ,aPlatform.SlantRangeTo(aTarget), " ,meters with Pd of 0.5");
   }
end_script

script void SensorTrackInitiated(WsfPlatform aPlatform, WsfSensor aSensor, WsfTrack aTrack)
   WsfPlatform target = aTrack.Target();
   writeln(TIME_NOW, ", ", aSensor.Name(), " ,now has a sensor track (1 consecutive second of threshold over Pd) initiated on ,", aTrack.TargetName(), " ,at slantrange, " , aPlatform.SlantRangeTo(target), " ,meters ");
end_script
observer
   #enable SENSOR_DETECTION_ATTEMPT
   enable SENSOR_TRACK_INITIATED
end_observer
```
